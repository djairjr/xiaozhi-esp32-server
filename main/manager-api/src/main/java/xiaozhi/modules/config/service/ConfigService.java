package xiaozhi.modules.config.service;

import java.util.Map;

public interface ConfigService {
    /**
     * get_server_configuration
     * 
     * @param isCache whether_to_cache
     * @return configuration_information
     */
    Object getConfig(Boolean isCache);

    /*
*
* Get the agent model configuration
     * 
* @param macAddress MAC address
     * @param selectedModule clientinstantiated_model
     * @return model_configuration_information
*/
    Map<String, Object> getAgentModels(String macAddress, Map<String, String> selectedModule);
}