package xiaozhi.modules.device.controller;

import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.redis.RedisKeys;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.common.user.UserDetail;
import xiaozhi.common.utils.Result;
import xiaozhi.modules.device.dto.DeviceManualAddDTO;
import xiaozhi.modules.device.dto.DeviceRegisterDTO;
import xiaozhi.modules.device.dto.DeviceUnBindDTO;
import xiaozhi.modules.device.dto.DeviceUpdateDTO;
import xiaozhi.modules.device.entity.DeviceEntity;
import xiaozhi.modules.device.service.DeviceService;
import xiaozhi.modules.security.user.SecurityUser;
import xiaozhi.modules.sys.service.SysParamsService;

@Tag(name = "Device management")
@RestController
@RequestMapping("/device")
public class DeviceController {
    private final DeviceService deviceService;
    private final RedisUtils redisUtils;
    private final SysParamsService sysParamsService;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public DeviceController(DeviceService deviceService, RedisUtils redisUtils, SysParamsService sysParamsService,
            RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.deviceService = deviceService;
        this.redisUtils = redisUtils;
        this.sysParamsService = sysParamsService;
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    @PostMapping("/bind/{agentId}/{deviceCode}")
    @Operation(summary = "Bind device")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> bindDevice(@PathVariable String agentId, @PathVariable String deviceCode) {
        deviceService.deviceActivation(agentId, deviceCode);
        return new Result<>();
    }

    @PostMapping("/register")
    @Operation(summary = "Register device")
    public Result<String> registerDevice(@RequestBody DeviceRegisterDTO deviceRegisterDTO) {
        String macAddress = deviceRegisterDTO.getMacAddress();
        if (StringUtils.isBlank(macAddress)) {
            return new Result<String>().error(ErrorCode.NOT_NULL, "mac address cannot be empty");
        }
        // generate_sixdigit_verification_code
        String code = String.valueOf(Math.random()).substring(2, 8);
        String key = RedisKeys.getDeviceCaptchaKey(code);
        String existsMac = null;
        do {
            existsMac = (String) redisUtils.get(key);
        } while (StringUtils.isNotBlank(existsMac));

        redisUtils.set(key, macAddress);
        return new Result<String>().ok(code);
    }

    @GetMapping("/bind/{agentId}")
    @Operation(summary = "Get bound devices")
    @RequiresPermissions("sys:role:normal")
    public Result<List<DeviceEntity>> getUserDevices(@PathVariable String agentId) {
        UserDetail user = SecurityUser.getUser();
        List<DeviceEntity> devices = deviceService.getUserDevices(user.getId(), agentId);
        return new Result<List<DeviceEntity>>().ok(devices);
    }

    @PostMapping("/bind/{agentId}")
    @Operation(summary = "Device online interface")
    @RequiresPermissions("sys:role:normal")
    public Result<String> forwardToMqttGateway(@PathVariable String agentId, @RequestBody String requestBody) {
        try {
            // get_mqtt_gateway_address_from_system_parameters
            String mqttGatewayUrl = sysParamsService.getValue("server.mqtt_manager_api", true);
            if (StringUtils.isBlank(mqttGatewayUrl) || "null".equals(mqttGatewayUrl)) {
                return new Result<>();
            }

            // get_the_current_users_device_list
            UserDetail user = SecurityUser.getUser();
            List<DeviceEntity> devices = deviceService.getUserDevices(user.getId(), agentId);

            // build_deviceids_array
            java.util.List<String> deviceIds = new java.util.ArrayList<>();
            for (DeviceEntity device : devices) {
                String macAddress = device.getMacAddress() != null ? device.getMacAddress() : "unknown";
                String groupId = device.getBoard() != null ? device.getBoard() : "GID_default";

                // replace_colon_with_underscore
                groupId = groupId.replace(":", "_");
                macAddress = macAddress.replace(":", "_");

                // build_mqtt_client_id_format：groupId@@@macAddress@@@macAddress
                String mqttClientId = groupId + "@@@" + macAddress + "@@@" + macAddress;
                deviceIds.add(mqttClientId);
            }

            // build_the_complete_url
            String url = "http://" + mqttGatewayUrl + "/api/devices/status";

            // set_request_header
            HttpHeaders headers = new HttpHeaders();
            headers.set("Content-Type", "application/json");

            // generate_bearer_token
            String token = generateBearerToken();
            if (token == null) {
                return new Result<String>().error("Token generation failed");
            }
            headers.set("Authorization", "Bearer " + token);

            // build_request_body_json
            String jsonBody = "{\"clientIds\":" + objectMapper.writeValueAsString(deviceIds) + "}";
            HttpEntity<String> requestEntity = new HttpEntity<>(jsonBody, headers);

            // send_post_request
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class);

            // return_response
            return new Result<String>().ok(response.getBody());
        } catch (Exception e) {
            return new Result<String>().error("Forward request failed:" + e.getMessage());
        }
    }

    private String generateBearerToken() {
        try {
            // get_current_date，the_format_is_yyyy-MM-dd
            String dateStr = java.time.LocalDate.now()
                    .format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd"));

            // get_mqtt_signing_key
            String signatureKey = sysParamsService.getValue("server.mqtt_signature_key", false);
            if (StringUtils.isBlank(signatureKey)) {
                return null;
            }

            // concatenate_date_string_with_mqtt_signature_key
            String tokenContent = dateStr + signatureKey;

            // perform_sha256_hash_calculation_on_the_concatenated_strings
            String token = org.apache.commons.codec.digest.DigestUtils.sha256Hex(tokenContent);

            return token;
        } catch (Exception e) {
            return null;
        }
    }

    @PostMapping("/unbind")
    @Operation(summary = "Unbind device")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> unbindDevice(@RequestBody DeviceUnBindDTO unDeviveBind) {
        UserDetail user = SecurityUser.getUser();
        deviceService.unbindDevice(user.getId(), unDeviveBind.getDeviceId());
        return new Result<Void>();
    }

    @PutMapping("/update/{id}")
    @Operation(summary = "Update device information")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> updateDeviceInfo(@PathVariable String id, @Valid @RequestBody DeviceUpdateDTO deviceUpdateDTO) {
        DeviceEntity entity = deviceService.selectById(id);
        if (entity == null) {
            return new Result<Void>().error("Device does not exist");
        }
        UserDetail user = SecurityUser.getUser();
        if (!entity.getUserId().equals(user.getId())) {
            return new Result<Void>().error("Device does not exist");
        }
        BeanUtils.copyProperties(deviceUpdateDTO, entity);
        deviceService.updateById(entity);
        return new Result<Void>();
    }

    @PostMapping("/manual-add")
    @Operation(summary = "Add device manually")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> manualAddDevice(@RequestBody @Valid DeviceManualAddDTO dto) {
        UserDetail user = SecurityUser.getUser();
        deviceService.manualAddDevice(user.getId(), dto);
        return new Result<>();
    }
}