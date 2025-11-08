import type { AgentFunction, PluginDefinition } from '@/api/agent/types'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePluginStore = defineStore(
  'plugin',
  () => {
    // all_available_plugins
    const allFunctions = ref<PluginDefinition[]>([])

    // the_plugin_configuration_of_the_current_agent
    const currentFunctions = ref<AgentFunction[]>([])

    // the_currently_edited_agent_id
    const currentAgentId = ref('')

    // set_up_all_available_plugins
    const setAllFunctions = (functions: PluginDefinition[]) => {
      allFunctions.value = functions
    }

    // set_the_plugin_configuration_of_the_current_agent
    const setCurrentFunctions = (functions: AgentFunction[]) => {
      currentFunctions.value = functions
    }

    // set_current_agent_id
    const setCurrentAgentId = (agentId: string) => {
      currentAgentId.value = agentId
    }

    // update_plugin_configuration（called_when_saving）
    const updateFunctions = (functions: AgentFunction[]) => {
      currentFunctions.value = functions
    }

    // clear_data
    const clear = () => {
      allFunctions.value = []
      currentFunctions.value = []
      currentAgentId.value = ''
    }

    return {
      allFunctions,
      currentFunctions,
      currentAgentId,
      setAllFunctions,
      setCurrentFunctions,
      setCurrentAgentId,
      updateFunctions,
      clear,
    }
  },
  {
    persist: false, // not_persistent，reload_every_time_you_enter_the_page
  },
)
