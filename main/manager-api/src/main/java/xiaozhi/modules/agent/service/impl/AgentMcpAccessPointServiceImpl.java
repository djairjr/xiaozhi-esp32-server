package xiaozhi.modules.agent.service.impl;

import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.constant.Constant;
import xiaozhi.common.utils.AESUtils;
import xiaozhi.common.utils.HashEncryptionUtil;
import xiaozhi.common.utils.JsonUtils;
import xiaozhi.modules.agent.Enums.XiaoZhiMcpJsonRpcJson;
import xiaozhi.modules.agent.service.AgentMcpAccessPointService;
import xiaozhi.modules.sys.service.SysParamsService;
import xiaozhi.modules.sys.utils.WebSocketClientManager;

@AllArgsConstructor
@Service
@Slf4j
public class AgentMcpAccessPointServiceImpl implements AgentMcpAccessPointService {
    private SysParamsService sysParamsService;

    @Override
    public String getAgentMcpAccessAddress(String id) {
        // get_the_address_of_mcp
        String url = sysParamsService.getValue(Constant.SERVER_MCP_ENDPOINT, true);
        if (StringUtils.isBlank(url) || "null".equals(url)) {
            return null;
        }
        URI uri = getURI(url);
        // get_the_url_prefix_of_the_agent_mcp
        String agentMcpUrl = getAgentMcpUrl(uri);
        // get_key
        String key = getSecretKey(uri);
        // get_encrypted_token
        String encryptToken = encryptToken(id, key);
        // url_encoding_the_token
        String encodedToken = URLEncoder.encode(encryptToken, StandardCharsets.UTF_8);
        // returns_the_format_of_the_agent_mcp_path
        agentMcpUrl = "%s/mcp/?token=%s".formatted(agentMcpUrl, encodedToken);
        return agentMcpUrl;
    }

    @Override
    public List<String> getAgentMcpToolsList(String id) {
        String wsUrl = getAgentMcpAccessAddress(id);
        if (StringUtils.isBlank(wsUrl)) {
            return List.of();
        }

        // will /mcp replace_with /call
        wsUrl = wsUrl.replace("/mcp/", "/call/");

        try {
            // create WebSocket connect，increase_timeout_to_15_seconds
            try (WebSocketClientManager client = WebSocketClientManager.build(
                    new WebSocketClientManager.Builder()
                            .uri(wsUrl)
                            .bufferSize(1024 * 1024)
                            .connectTimeout(8, TimeUnit.SECONDS)
                            .maxSessionDuration(10, TimeUnit.SECONDS))) {

                // step_1: send_initialization_message_and_wait_for_response
                log.info("Send MCP initialization message, agent_id: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getInitializeJson());

                // wait_for_initialization_response (id=1) - remove_fixed_delay，change_to_responsedriven
                List<String> initResponses = client.listenerWithoutClose(response -> {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(1).equals(jsonMap.get("id"))) {
                            // check_if_there_is_a_result_field，indicates_successful_initialization
                            return jsonMap.containsKey("result") && !jsonMap.containsKey("error");
                        }
                        return false;
                    } catch (Exception e) {
                        log.warn("Failed to parse initialization response: {}", response, e);
                        return false;
                    }
                });

                // verify_initialization_response
                boolean initSucceeded = false;
                for (String response : initResponses) {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(1).equals(jsonMap.get("id"))) {
                            if (jsonMap.containsKey("result")) {
                                log.info("MCP initialization successful, agent_id: {}", id);
                                initSucceeded = true;
                                break;
                            } else if (jsonMap.containsKey("error")) {
                                log.error("MCP initialization failed, agent_id: {}, mistake: {}", id, jsonMap.get("error"));
                                return List.of();
                            }
                        }
                    } catch (Exception e) {
                        log.warn("Failed to handle initialization response: {}", response, e);
                    }
                }

                if (!initSucceeded) {
                    log.error("No valid MCP initialization response received, agent_id: {}", id);
                    return List.of();
                }

                // step_2: send_initialization_completion_notification - sent_only_after_receiving_initialize_response
                log.info("Send MCP initialization completion notification, agent_id: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getNotificationsInitializedJson());
                // step_3: send_tool_list_request - send_now，no_additional_delay_required
                log.info("Send MCP tool list request, agent_id: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getToolsListJson());

                // waiting_for_tool_list_response (id=2)
                List<String> toolsResponses = client.listener(response -> {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        return jsonMap != null && Integer.valueOf(2).equals(jsonMap.get("id"));
                    } catch (Exception e) {
                        log.warn("Parsing tool list response failed: {}", response, e);
                        return false;
                    }
                });

                // handling_tool_list_responses
                for (String response : toolsResponses) {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(2).equals(jsonMap.get("id"))) {
                            // check_if_there_is_a_result_field
                            Object resultObj = jsonMap.get("result");
                            if (resultObj instanceof Map) {
                                Map<String, Object> resultMap = (Map<String, Object>) resultObj;
                                Object toolsObj = resultMap.get("tools");
                                if (toolsObj instanceof List) {
                                    List<Map<String, Object>> toolsList = (List<Map<String, Object>>) toolsObj;
                                    // extraction_tool_name_list
                                    List<String> result = toolsList.stream()
                                            .map(tool -> (String) tool.get("name"))
                                            .filter(name -> name != null)
                                            .collect(Collectors.toList());
                                    log.info("Successfully obtained MCP tool list, agent_id: {}, number_of_tools: {}", id, result.size());
                                    return result;
                                }
                            } else if (jsonMap.containsKey("error")) {
                                log.error("Failed to obtain tool list, agent_id: {}, mistake: {}", id, jsonMap.get("error"));
                                return List.of();
                            }
                        }
                    } catch (Exception e) {
                        log.warn("Failed to process tool list response: {}", response, e);
                    }
                }

                log.warn("No valid tool list response found, agent_id: {}", id);
                return List.of();

            }
        } catch (Exception e) {
            log.error("Get the agent MCP tool_list_failed, agent_id: {}, error_reason: {}", id, e.getMessage());
            return List.of();
        }
    }

    /*
*
     * get_uri_object
     * 
     * @param url path
* @return URI object
*/
    private static URI getURI(String url) {
        try {
            return new URI(url);
        } catch (URISyntaxException e) {
            log.error("Incorrect path format path: {},\nError message: {}", url, e.getMessage());
            throw new RuntimeException("There is an error in the mcp address. Please enter parameter management to modify the mcp access point address.");
        }
    }

    /*
*
     * get_key
     *
* @param uri mcp address
     * @return key
*/
    private static String getSecretKey(URI uri) {
        // get_parameters
        String query = uri.getQuery();
        // get_aes_encryption_key
        String str = "key=";
        return query.substring(query.indexOf(str) + str.length());
    }

    /*
*
     * get_the_agent_mcp_access_point_url
     *
* @param uri mcp address
     * @return agent_mcp_access_point_url
*/
    private String getAgentMcpUrl(URI uri) {
        // get_agreement
        String wsScheme = (uri.getScheme().equals("https")) ? "wss" : "ws";
        // get_host，port，path
        String path = uri.getSchemeSpecificPart();
        // get_the_last_one/path_before
        path = path.substring(0, path.lastIndexOf("/"));
        return wsScheme + ":" + path;
    }

    /**
     * get_the_encrypted_token_of_the_agent_id
     *
     * @param agentId agent_id
     * @param key     encryption_key
     * @return encrypted_token
     */
    private static String encryptToken(String agentId, String key) {
        // use_md5_to_encrypt_the_agent_id
        String md5 = HashEncryptionUtil.Md5hexDigest(agentId);
        // aes requires encrypted text
        String json = "{\"agentId\": \"%s\"}".formatted(md5);
        // encrypted_into_token_value
        return AESUtils.encrypt(key, json);
    }
}