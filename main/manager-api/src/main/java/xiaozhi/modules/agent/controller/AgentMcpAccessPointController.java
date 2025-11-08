package xiaozhi.modules.agent.controller;

import java.util.List;

import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import xiaozhi.common.user.UserDetail;
import xiaozhi.common.utils.Result;
import xiaozhi.modules.agent.service.AgentMcpAccessPointService;
import xiaozhi.modules.agent.service.AgentService;
import xiaozhi.modules.security.user.SecurityUser;

@Tag(name = "Intelligent Mcp access point management")
@RequiredArgsConstructor
@RestController
@RequestMapping("/agent/mcp")
public class AgentMcpAccessPointController {
    private final AgentMcpAccessPointService agentMcpAccessPointService;
    private final AgentService agentService;

    /**
     * get_the_agents_mcp_access_point_address
     * 
     * @param audioId agent_id
     * @return return_error_reminder_or_mcp_access_point_address
     */
    @Operation(summary = "Get the agent's Mcp access point address")
    @GetMapping("/address/{agentId}")
    @RequiresPermissions("sys:role:normal")
    public Result<String> getAgentMcpAccessAddress(@PathVariable("agentId") String agentId) {
        // get_current_user
        UserDetail user = SecurityUser.getUser();

        // check_permissions
        if (!agentService.checkAgentPermission(agentId, user.getId())) {
            return new Result<String>().error("You do not have permission to view the MCP access point address of this agent.");
        }
        String agentMcpAccessAddress = agentMcpAccessPointService.getAgentMcpAccessAddress(agentId);
        if (agentMcpAccessAddress == null) {
            return new Result<String>().ok("Please contact the administrator to enter parameter management to configure the mcp access point address.");
        }
        return new Result<String>().ok(agentMcpAccessAddress);
    }

    @Operation(summary = "Get the agent's Mcp tool list")
    @GetMapping("/tools/{agentId}")
    @RequiresPermissions("sys:role:normal")
    public Result<List<String>> getAgentMcpToolsList(@PathVariable("agentId") String agentId) {
        // get_current_user
        UserDetail user = SecurityUser.getUser();

        // check_permissions
        if (!agentService.checkAgentPermission(agentId, user.getId())) {
            return new Result<List<String>>().error("Do not have permission to view the MCP tool list of this agent");
        }
        List<String> agentMcpToolsList = agentMcpAccessPointService.getAgentMcpToolsList(agentId);
        return new Result<List<String>>().ok(agentMcpToolsList);
    }
}
