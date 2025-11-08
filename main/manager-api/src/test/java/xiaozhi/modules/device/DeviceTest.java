package xiaozhi.modules.device;

import java.util.HashMap;
import java.util.UUID;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.modules.sys.dto.SysUserDTO;
import xiaozhi.modules.sys.service.SysUserService;

@Slf4j
@SpringBootTest
@ActiveProfiles("dev")
@DisplayName("Equipment testing")
public class DeviceTest {

    @Autowired
    private RedisUtils redisUtils;
    @Autowired
    private SysUserService sysUserService;

    @Test
    public void testSaveUser() {
        SysUserDTO userDTO = new SysUserDTO();
        userDTO.setUsername("test");
        userDTO.setPassword(UUID.randomUUID().toString());
        sysUserService.save(userDTO);
    }

    @Test
    @DisplayName("Test writing device information")
    public void testWriteDeviceInfo() {
        log.info("Start testing writing device information...");
        // simulate_device_mac_address
        String macAddress = "00:11:22:33:44:66";
        // simulated_device_verification_code
        String deviceCode = "123456";

        HashMap<String, Object> map = new HashMap<>();
        map.put("mac_address", macAddress);
        map.put("activation_code", deviceCode);
        map.put("board", "Hardware model");
        map.put("app_version", "0.3.13");

        String safeDeviceId = macAddress.replace(":", "_").toLowerCase();
        String cacheDeviceKey = String.format("ota:activation:data:%s", safeDeviceId);
        redisUtils.set(cacheDeviceKey, map, 300);

        String redisKey = "ota:activation:code:" + deviceCode;
        log.info("Redis Key: {}", redisKey);

        // write_device_information_to_redis
        redisUtils.set(redisKey, macAddress, 300);
        log.info("Device information has been written to Redis");

        // verify_whether_the_write_is_successful
        String savedMacAddress = (String) redisUtils.get(redisKey);
        log.info("MAC address read from Redis: {}", savedMacAddress);

        // verify_using_assertions
        Assertions.assertNotNull(savedMacAddress, "MAC address read from Redis should not be empty");
        Assertions.assertEquals(macAddress, savedMacAddress, "The saved MAC address does not match the original MAC address");

        log.info("Test completed");
    }
}