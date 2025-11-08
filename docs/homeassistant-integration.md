# Xiaozhi ESP32-Open Source Server and HomeAssistant Integration Guide

[TOC]

-----

## Introduction

This document will guide you on how to integrate your ESP32 device with HomeAssistant.

## Prerequisites

- `HomeAssistant` installed and configured
- The model I chose this time is: free ChatGLM, which supports functioncall function calling

## Operations before starting (necessary)

### 1. Obtain the network address information of HA

Please access the network address of your Home Assistant. For example, the address of my HA is 192.168.4.7 and the port is the default 8123. Then open it in the browser

```
http://192.168.4.7:8123
```

> Manually query the IP address of HA** (only if Xiaozhi esp32-server and HA are deployed on the same network device [such as the same wifi])**:
>
> 1. Enter Home Assistant (front end).
>
> 2. 点击左下角 **设置（Settings）** → **系统（System）** → **网络（Network）**。
>
> 3. Slide to the bottom `Home Assistant website` area, in `local network`, click the `eye` button, you can see the currently used IP address (such as `192.168.1.10`) and network interface. Click `copy link(copy link)` to copy directly.
>
>    ![image-20250504051716417](images/image-ha-integration-01.png)

Or, you have set up the OAuth address of Home Assistant that can be accessed directly. You can also access it directly in the browser.

```
http://homeassistant.local:8123
```

### 2. Log in to `Home Assistant` to get the development key

Log in to `HomeAssistant`, click on `avatar in the lower left corner -> Personal`, switch to the `Security` navigation bar, swipe to the bottom of `Long Term Access Token` to generate api_key, and copy and save it. Subsequent methods need to use this api key and it only appears once (small tip: You can save the generated QR code image, and you can scan the QR code later to extract the api key).

## Method 1: HA calling function jointly built by Xiaozhi community

### Function description

- If you need to add new devices later, this method requires you to manually restart the `xiaozhi-esp32-server` to update the device information** (Important**).

- You need to ensure that you have integrated `Xiaomi Home` in HomeAssistant and imported Mijia devices into `HomeAssistant`.

- You need to ensure that the `xiaozhi-esp32-server intelligent console` can be used normally.

- My `xiaozhi-esp32-server intelligent console` and `HomeAssistant` are deployed on another port of the same machine, and the version is `0.3.10`

  ```
  http://192.168.4.7:8002
  ```


### Configuration steps

#### 1. Log in to `HomeAssistant` to organize the list of devices that need to be controlled

Log in to `HomeAssistant`, click `Settings` in the lower left corner, then enter `Devices and Services`, and then click `Entities` at the top.

Then search for your relevant control switch in the entity. After the results come out, click on one of the results in the list, and a switch interface will appear.

In the switch interface, we try to click the switch to see if the development will turn on/off with our click. If it works, it means the network is functioning normally.

Then find the settings button on the switch panel. After clicking it, you can view the `entity identifier` of this switch.

We open a notepad and organize a piece of data in this format:

Location + comma + device name + comma + `entity identifier` + semicolon

For example, I am in the company, I have a toy lamp, its identifier is switch.cuco_cn_460494544_cp1_on_p_2_1, then write this piece of data

```
company, toy lamp, switch.cuco_cn_460494544_cp1_on_p_2_1;
```

Of course, I may have to operate two lights in the end. My final result is:

```
company, toy lamp, switch.cuco_cn_460494544_cp1_on_p_2_1;
company, desk lamp, switch.iot_cn_831898993_socn1_on_p_2_1;
```

This character, which we call the "device list character", needs to be saved and will be useful later.

#### 2. Log in to `Smart Console`

![image-20250504051716417](images/image-ha-integration-06.png)

Use the administrator account to log in to the `Intelligent Console`. In `Agent Management`, find your agent and click `Configure Role`.

Set intent recognition to `function call` or `LLM intent recognition`. At this time you will see an `editing function` on the right. Click the `Edit Function` button, and the `Function Management` box will pop up.

In the `Function Management` box, you need to check `HomeAssistant Device Status Query` and `HomeAssistant Device Status Modification`.

After checking, click `HomeAssistant Device Status Query` in `Selected Functions`, and then configure your `HomeAssistant` address, key, and device list characters in `Parameter Configuration`.

After editing, click `Save Configuration`. At this time, the `Function Management` box will be hidden. Then you can click to save the agent configuration.

After successful saving, the device operation can be awakened.

#### 3. Wake up the device for control

Try telling esp32, "Turn on the XXX light"

## Method 2: Xiaozhi uses Home Assistant’s voice assistant as an LLM tool

### Function description

- This method has a serious shortcoming - **This method cannot use the function_call plug-in function of Xiaozhi's open source ecosystem**, because using Home Assistant as Xiaozhi's LLM tool will transfer the intent recognition capability to Home Assistant. But **this method allows you to experience the native Home Assistant operating functions, and Xiaozhi’s chat ability remains unchanged**. If you really mind, you can use [Method 3] (##Method 3: Use Home Assistant’s MCP service (recommended)), which is also supported by Home Assistant, to experience the functions of Home Assistant to the maximum extent.

### Configuration steps:

#### 1. Configure the large model voice assistant of Home Assistant.

**You need to configure the Home Assistant voice assistant or large model tool in advance. **

#### 2. Get the Agent ID of Home Assistant’s language assistant.

1. Enter the Home Assistant page. Click on `Developer Assistant` on the left.
2. In the opened `Developer Assistant`, click the `Action` tab (as shown in Operation 1). In the option bar `Action` on the page, find or enter `conversation.process (conversation-processing)` and select `Conversation: Process` (as shown in Operation 2).

![image-20250504043539343](images/image-ha-integration-02.png)

3. Check the `agent` option on the page, and select the name of the voice assistant you configured in step 1 in the `conversation agent` that becomes always bright, as shown in the picture. The one I configured here is `ZhipuAi` and select it.

![image-20250504043854760](images/image-ha-integration-03.png)

4. After selecting, click `Enter YAML mode` at the bottom left of the form.

![image-20250504043951126](images/image-ha-integration-04.png)

5. Copy the value of agent-id. For example, mine is `01JP2DYMBDF7F4ZA2DMCF2AGX2` in the picture (for reference only).

![image-20250504044046466](images/image-ha-integration-05.png)

6. Switch to the `config.yaml` file of Xiaozhi open source server `xiaozhi-esp32-server`, in the LLM configuration, find Home Assistant, set your Home Assistant's network address, API key and the agent_id you just queried.
7. Modify the `LLM` of the `selected_module` attribute in the `config.yaml` file to `HomeAssistant` and `Intent` to `nointent`.
8. Restart the Xiaozhi open source server `xiaozhi-esp32-server` to use it normally.

## Method 3: Use Home Assistant’s MCP service (recommended)

### Function description

- You need to integrate and install HA integration in Home Assistant in advance - [Model Context Protocol Server](https://www.home-assistant.io/integrations/mcp_server/).

- This method and method 2 are both solutions officially provided by HA. Different from method 2, you can normally use the open source co-built plug-in of Xiaozhi open source server `xiaozhi-esp32-server`, and you are allowed to use any large LLM model that supports the function_call function at will.

### Configuration steps

#### 1. Install Home Assistant’s MCP service integration.

Integrated official website - [Model Context Protocol Server](https://www.home-assistant.io/integrations/mcp_server/). .

Or follow the manual steps below.

> - Go to **[Settings > Devices & Services.](https://my.home-assistant.io/redirect/integrations)** on the Home Assistant page.
>
> - In the lower right corner, select the **[Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp_server)** button.
>
> - Select Model Context Protocol Server from the list.
>
> - Follow the on-screen instructions to complete setup.

#### 2. Configure Xiaozhi open source server MCP configuration information


Enter the `data` directory and find the `.mcp_server_settings.json` file.

If there is no `.mcp_server_settings.json` file in your `data` directory,
- Please copy the `mcp_server_settings.json` file in the root directory of the `xiaozhi-server` folder to the `data` directory and rename it to `.mcp_server_settings.json`
- Or [download this file](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/main/xiaozhi-server/mcp_server_settings.json), download it to the `data` directory, and rename it to `.mcp_server_settings.json`


Modify the content of this part in `"mcpServers"`:

```json
"Home Assistant": {
      "command": "mcp-proxy",
      "args": [
        "http://YOUR_HA_HOST/mcp_server/sse"
      ],
      "env": {
        "API_ACCESS_TOKEN": "YOUR_API_ACCESS_TOKEN"
      }
},
```

Notice:

1. **Replacement configuration:**
- Replace `YOUR_HA_HOST` in `args` with your HA service address. If your service address already contains the words https/http (for example, `http://192.168.1.101:8123`), you only need to fill in `192.168.1.101:8123`.
- Replace `YOUR_API_ACCESS_TOKEN` in `API_ACCESS_TOKEN` in `env` with the development key api key you obtained previously.
2. **If you add the configuration within the brackets of `"mcpServers"` and there is no new `mcpServers` configuration, you need to remove the last comma `,`**, otherwise the parsing may fail.

**The final effect is as follows (reference is as follows)**:

```json
 "mcpServers": {
    "Home Assistant": {
      "command": "mcp-proxy",
      "args": [
        "http://192.168.1.101:8123/mcp_server/sse"
      ],
      "env": {
        "API_ACCESS_TOKEN": "abcd.efghi.jkl"
      }
    }
  }
```

#### 3. Configure the system configuration of Xiaozhi open source server

1. **Choose any large LLM model that supports function_call as Xiaozhi’s LLM chat assistant (but do not choose Home Assistant as the LLM tool)**. The model I chose this time is: free ChatGLM, which supports function call function calls, but sometimes the call is not stable. If you are pursuing stability, it is recommended to set the LLM to: DoubaoLLM, and the specific model_name used is: doubao-1-5-pro-32k-250115.

2. Switch to the `config.yaml` file of Xiaozhi open source server `xiaozhi-esp32-server`, set your LLM large model configuration, and adjust the `Intent` configured in `selected_module` to `function_call`.

3. Restart the Xiaozhi open source server `xiaozhi-esp32-server` to use it normally.