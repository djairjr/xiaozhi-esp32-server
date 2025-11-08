#Visual model usage guide
This tutorial is divided into two parts:
- Part 1: Run xiaozhi-server on a single module to open the visual model
- Part 2: How to open the visual model when the whole module is running

Before opening the visual model, you need to prepare three things:
- You need to prepare a device with a camera, and this device is already in Brother Xiabao's warehouse and has the function of calling the camera. For example, `Lichuang Practical ESP32-S3 Development Board`
- Upgrade your device firmware version to 1.6.6 or above
- You have successfully passed the basic dialogue module

## Single module runs xiaozhi-server to open the visual model

### The first step is to confirm the network
Because the visual model will start port 8003 by default.

If you are running docker, please confirm whether your `docker-compose.yml` has the `8003` port. If not, update the latest `docker-compose.yml` file.

If you are running from source code, confirm whether the firewall allows port `8003`

### The second step is to choose your visual model
Open your `data/.config.yaml` file and set your `selected_module.VLLM` settings to a certain visual model. Currently we already support the visual model of the `openai` type interface. `ChatGLMVLLM` is one of the models compatible with `openai`.

```
selected_module:
  VAD: ..
  ASR: ..
  LLM: ..
  VLLM: ChatGLMVLLM
  TTS: ..
  Memory: ..
  Intent: ..
```

Suppose we use `ChatGLMVLLM` as the visual model, then we need to log in to the [Big Model AI] (https://bigmodel.cn/usercenter/proj-mgmt/apikeys) website and apply for a key. If you have applied for a key before, you can reuse it.

In your configuration file, add this configuration. If you already have this configuration, set your api_key.

```
VLLM:
  ChatGLMVLLM:
api_key: your api_key
```

### The third step is to start the xiaozhi-server service
If you are source code, enter the command to start
```
python app.py
```
If you are running docker, restart the container
```
docker restart xiaozhi-esp32-server
```

After startup, the following log content will be output.

```
2025-06-01 **** - OTA interface is http://192.168.4.7:8003/xiaozhi/ota/
2025-06-01 **** - The visual analysis interface is http://192.168.4.7:8003/mcp/vision/explain
2025-06-01 **** - The Websocket address is ws://192.168.4.7:8000/xiaozhi/v1/
2025-06-01 **** - =======The above address is the websocket protocol address, please do not access it with a browser========
2025-06-01 **** - If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
2025-06-01 **** - =============================================================
```

After startup, use a browser to open the `Visual Analysis Interface` connection in the log. See what's output? If you are on Linux and do not have a browser, you can execute this command:
```
curl -i your visual analysis interface
```

Normally it would display like this
```
The MCP Vision interface is running normally, and the visual explanation interface address is: http://xxxx:8003/mcp/vision/explain
```

Please note that if you deploy on the public network or docker, you must change this configuration in your `data/.config.yaml`
```
server:
vision_explain: http://your ip or domain name: port number/mcp/vision/explain
```

Why? Because the visual interpretation interface needs to be delivered to the device, if your address is a LAN address or a docker internal address, the device cannot access it.

Assuming that your public network address is `111.111.111.111`, then `vision_explain` should be configured like this

```
server:
  vision_explain: http://111.111.111.111:8003/mcp/vision/explain
```

If your MCP Vision interface is running normally and you also try to use a browser to access the `Visual Interpretation Interface Address` issued by normal opening, please continue to the next step.

### Step 4: Enable device wake-up

Say to the device "Please turn on the camera and tell me what you see"

Pay attention to the log output of xiaozhi-server to see if there are any errors.


## How to open the visual model when the whole module is running

### The first step is to confirm the network
Because the visual model will start port 8003 by default.

If you are running docker, please confirm whether your `docker-compose_all.yml` is mapped to the `8003` port. If not, update the latest `docker-compose_all.yml` file.

If you are running from source code, confirm whether the firewall allows port `8003`

### Step 2 Confirm your configuration file

Open your `data/.config.yaml` file and confirm whether the structure of your configuration file is the same as `data/config_from_api.yaml`. If it is different, or if something is missing, please fill it in.

### Step 3 Configure the visual model key

Then we need to log in to the [Zhipu AI] (https://bigmodel.cn/usercenter/proj-mgmt/apikeys) website first and apply for a key. If you have applied for a key before, you can reuse it.

Log in to the `Intelligent Console`, click `Model Configuration` on the top menu, click `Visual Language Model` in the left column, find `VLLM_ChatGLMVLLM`, click the modify button, in the pop-up box, enter your key in `API Key`, and click Save.

After saving successfully, go to the agent you need to test, click Configure Role, and in the opened content, check whether the Visual Large Language Model (VLLM) has selected the visual model just now. Click Save.

### Step 3: Start the xiaozhi-server module
If you are source code, enter the command to start
```
python app.py
```
If you are running docker, restart the container
```
docker restart xiaozhi-esp32-server
```

After startup, the following log content will be output.

```
2025-06-01 **** - The visual analysis interface is http://192.168.4.7:8003/mcp/vision/explain
2025-06-01 **** - The Websocket address is ws://192.168.4.7:8000/xiaozhi/v1/
2025-06-01 **** - =======The above address is the websocket protocol address, please do not access it with a browser========
2025-06-01 **** - If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
2025-06-01 **** - =============================================================
```

After startup, use a browser to open the `Visual Analysis Interface` connection in the log. See what's output? If you are on Linux and do not have a browser, you can execute this command:
```
curl -i your visual analysis interface
```

Normally it would display like this
```
The MCP Vision interface is running normally, and the visual explanation interface address is: http://xxxx:8003/mcp/vision/explain
```

Please note that if you deploy on the public network or docker, you must change this configuration in your `data/.config.yaml`
```
server:
vision_explain: http://your ip or domain name: port number/mcp/vision/explain
```

Why? Because the visual interpretation interface needs to be delivered to the device, if your address is a LAN address or a docker internal address, the device cannot access it.

Assuming that your public network address is `111.111.111.111`, then `vision_explain` should be configured like this

```
server:
  vision_explain: http://111.111.111.111:8003/mcp/vision/explain
```

If your MCP Vision interface is running normally and you also try to use a browser to access the `Visual Interpretation Interface Address` issued by normal opening, please continue to the next step.

### Step 4: Enable device wake-up

Say to the device "Please turn on the camera and tell me what you see"

Pay attention to the log output of xiaozhi-server to see if there are any errors.
