package xiaozhi.modules.agent.controller;

import java.io.IOException;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.apache.commons.lang3.StringUtils;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import xiaozhi.common.constant.Constant;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.exception.RenException;
import xiaozhi.common.page.PageData;
import xiaozhi.common.redis.RedisKeys;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.common.user.UserDetail;
import xiaozhi.common.utils.DateUtils;
import xiaozhi.common.utils.MessageUtils;
import xiaozhi.common.utils.Result;
import xiaozhi.modules.agent.dto.AgentChatHistoryDTO;
import xiaozhi.modules.agent.dto.AgentChatHistoryReportDTO;
import xiaozhi.modules.agent.dto.AgentChatSessionDTO;
import xiaozhi.modules.agent.service.AgentChatHistoryService;
import xiaozhi.modules.agent.service.AgentService;
import xiaozhi.modules.agent.service.biz.AgentChatHistoryBizService;
import xiaozhi.modules.security.user.SecurityUser;

@Tag(name = "Agent chat history management")
@RequiredArgsConstructor
@RestController
@RequestMapping("/agent/chat-history")
public class AgentChatHistoryController {
    private final AgentChatHistoryBizService agentChatHistoryBizService;
    private final AgentChatHistoryService agentChatHistoryService;
    private final AgentService agentService;
    private final RedisUtils redisUtils;

    /**
     * xiaozhi_service_chat_reporting_request
     * <p>
     * xiaozhi_service_chat_reporting_request，contains_base64_encoded_audio_data_and_related_information。
     *
     * @param request request_object_containing_uploaded_files_and_related_information
     */
    @Operation(summary = "Xiaozhi Service Chat Reporting Request")
    @PostMapping("/report")
    public Result<Boolean> uploadFile(@Valid @RequestBody AgentChatHistoryReportDTO request) {
        Boolean result = agentChatHistoryBizService.report(request);
        return new Result<Boolean>().ok(result);
    }

    /*
*
     * get_chat_history_download_link
     * 
     * @param agentId   agent_id
     * @param sessionId session_id
* @return UUID as download identifier
*/
    @Operation(summary = "Get chat history download link")
    @RequiresPermissions("sys:role:normal")
    @PostMapping("/getDownloadUrl/{agentId}/{sessionId}")
    public Result<String> getDownloadUrl(@PathVariable("agentId") String agentId,
            @PathVariable("sessionId") String sessionId) {
        // get_current_user
        UserDetail user = SecurityUser.getUser();
        // check_permissions
        if (!agentService.checkAgentPermission(agentId, user.getId())) {
            throw new RenException(ErrorCode.CHAT_HISTORY_NO_PERMISSION);
        }

        // generate_uuid
        String uuid = UUID.randomUUID().toString();
        // store_agentid_and_sessionid_in_redis，the_format_is_agentid:sessionId
        redisUtils.set(RedisKeys.getChatHistoryKey(uuid), agentId + ":" + sessionId);

        return new Result<String>().ok(uuid);
    }

    /*
*
     * download_the_chat_transcript_of_this_session
     * 
     * @param uuid     download_logo
* @param response HTTP response
*/
    @Operation(summary = "Download the chat transcript of this session")
    @GetMapping("/download/{uuid}/current")
    public void downloadCurrentSession(@PathVariable("uuid") String uuid,
            HttpServletResponse response) {
        // get_agentid_and_sessionid_from_redis
        String agentSessionInfo = (String) redisUtils.get(RedisKeys.getChatHistoryKey(uuid));
        if (StringUtils.isBlank(agentSessionInfo)) {
            throw new RenException(ErrorCode.DOWNLOAD_LINK_EXPIRED);
        }

        try {
            // parse_agentid_and_sessionid
            String[] parts = agentSessionInfo.split(":");
            if (parts.length != 2) {
                throw new RenException(ErrorCode.DOWNLOAD_LINK_INVALID);
            }
            String agentId = parts[0];
            String sessionId = parts[1];

            // execute_download
            downloadChatHistory(agentId, List.of(sessionId), response);
        } finally {
            // delete_uuid_after_download_is_complete，prevent_theft
            redisUtils.delete(RedisKeys.getChatHistoryKey(uuid));
        }
    }

    /*
*
     * download_the_chat_records_of_this_conversation_and_the_previous_20_conversations
     * 
     * @param uuid     download_logo
* @param response HTTP response
*/
    @Operation(summary = "Download the chat records of this conversation and the previous 20 conversations")
    @GetMapping("/download/{uuid}/previous")
    public void downloadCurrentSessionWithPrevious(@PathVariable("uuid") String uuid,
            HttpServletResponse response) {
        // get_agentid_and_sessionid_from_redis
        String agentSessionInfo = (String) redisUtils.get(RedisKeys.getChatHistoryKey(uuid));
        if (StringUtils.isBlank(agentSessionInfo)) {
            throw new RenException("The download link has expired or is invalid");
        }

        try {
            // parse_agentid_and_sessionid
            String[] parts = agentSessionInfo.split(":");
            if (parts.length != 2) {
                throw new RenException("Download link is invalid");
            }
            String agentId = parts[0];
            String sessionId = parts[1];

            // get_a_list_of_all_sessions
            Map<String, Object> params = Map.of(
                    "agentId", agentId,
                    Constant.PAGE, 1,
                    Constant.LIMIT, 1000 // get_enough_sessions
            );
            PageData<AgentChatSessionDTO> sessionPage = agentChatHistoryService.getSessionListByAgentId(params);
            List<AgentChatSessionDTO> allSessions = sessionPage.getList();

            // find_where_the_current_session_is_in_the_list
            int currentIndex = -1;
            for (int i = 0; i < allSessions.size(); i++) {
                if (allSessions.get(i).getSessionId().equals(sessionId)) {
                    currentIndex = i;
                    break;
                }
            }

            // if_the_current_session_is_found，collect_current_session_and_previous_20_session_ids
            List<String> sessionIdsToDownload = new ArrayList<>();
            if (currentIndex != -1) {
                // start_from_current_session，backward（behind_the_array）get_up_to_20_conversations（includes_current_session）
                int endIndex = Math.min(allSessions.size() - 1, currentIndex + 20); // make_sure_not_to_cross_the_line
                for (int i = currentIndex; i <= endIndex; i++) {
                    sessionIdsToDownload.add(allSessions.get(i).getSessionId());
                }
            }

            // if_the_current_session_is_not_found，download_at_least_the_current_session
            if (sessionIdsToDownload.isEmpty()) {
                sessionIdsToDownload.add(sessionId);
            }
            downloadChatHistory(agentId, sessionIdsToDownload, response);
        } finally {
            // delete_uuid_after_download_is_complete，prevent_theft
            redisUtils.delete(RedisKeys.getChatHistoryKey(uuid));
        }
    }

    /*
*
     * download_the_chat_history_of_a_specified_session
     * 
     * @param agentId    agent_id
     * @param sessionIds list_of_session_ids
* @param response HTTP response
*/
    private void downloadChatHistory(String agentId, List<String> sessionIds, HttpServletResponse response) {
        try {
            // set_response_headers
            response.setContentType("text/plain;charset=UTF-8");
            String fileName = URLEncoder.encode("history.txt", StandardCharsets.UTF_8.toString());
            response.setHeader("Content-Disposition", "attachment;filename=" + fileName);

            // get_the_chat_history_and_write_to_the_response_stream
            try (OutputStream out = response.getOutputStream()) {
                // generate_chat_transcripts_for_each_conversation
                for (String sessionId : sessionIds) {
                    // get_all_chat_history_of_this_conversation
                    List<AgentChatHistoryDTO> chatHistoryList = agentChatHistoryService
                            .getChatHistoryBySessionId(agentId, sessionId);

                    // get_the_creation_time_of_the_first_message_from_the_chat_history_as_the_session_time
                    if (!chatHistoryList.isEmpty()) {
                        Date firstMessageTime = chatHistoryList.get(0).getCreatedAt();
                        String sessionTimeStr = DateUtils.format(firstMessageTime, DateUtils.DATE_TIME_PATTERN);
                        out.write((sessionTimeStr + "\n").getBytes(StandardCharsets.UTF_8));
                    }

                    for (AgentChatHistoryDTO message : chatHistoryList) {
                        String role = message.getChatType() == 1 ? MessageUtils.getMessage(ErrorCode.CHAT_ROLE_USER)
                                : MessageUtils.getMessage(ErrorCode.CHAT_ROLE_AGENT);
                        String direction = message.getChatType() == 1 ? ">>" : "<<";
                        Date messageTime = message.getCreatedAt();
                        String messageTimeStr = DateUtils.format(messageTime, DateUtils.DATE_TIME_PATTERN);
                        String content = message.getContent();

                        String line = "[" + role + "]-[" + messageTimeStr + "]" + direction + ":" + content + "\n";
                        out.write(line.getBytes(StandardCharsets.UTF_8));
                    }

                    // add_blank_lines_to_separate_sessions
                    if (sessionIds.indexOf(sessionId) < sessionIds.size() - 1) {
                        out.write("\n".getBytes(StandardCharsets.UTF_8));
                    }
                }

                out.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
