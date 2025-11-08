#FAQ ❓

### 1. Why does Xiaozhi recognize a lot of Korean, Japanese, and English when I say it? 🇰🇷

Suggestion: Check if `models/SenseVoiceSmall` already has `model.pt`
file, if you don’t have it, download it, check here [Download speech recognition model file] (Deployment.md# model file)

### 2. Why does "TTS task error file does not exist" appear? 📁

Suggestion: Check whether you installed the libopus and ffmpeg libraries correctly using `conda`.

If it is not installed, install it

```
conda install conda-forge::libopus
conda install conda-forge::ffmpeg
```

### 3. TTS often fails and times out ⏰

Suggestion: If `EdgeTTS` fails frequently, please first check whether a proxy (ladder) is used. If used, please try to close the proxy and try again;
If you are using the beanbag TTS of the Volcano engine, it is recommended to use the paid version when it often fails, because the test version only supports 2 concurrencies.

### 4. You can connect to the self-built server using Wifi, but the 4G mode cannot connect 🔐

Reason: Xia Ge’s firmware requires a secure connection in 4G mode.

Solution: There are currently two ways to solve it. Choose any one:

1. Change the code. Refer to this video to solve the problem https://www.bilibili.com/video/BV18MfTYoE85

2. Use nginx to configure the ssl certificate. Reference tutorial https://icnt94i5ctj4.feishu.cn/docx/GnYOdMNJOoRCljx1ctecsj9cnRe

### 5. How to improve Xiaozhi’s dialogue response speed? ⚡

The default configuration of this project is a low-cost solution. It is recommended that beginners use the default free model first to solve the problem of "running fast" and then optimize "running fast".
If you need to improve the response speed, you can try replacing each component. Starting from version 0.5.2, the project supports streaming configuration. Compared with earlier versions, the response speed is increased by about 2.5 seconds, significantly improving the user experience.

| Module name | Free entry-level setup | Streaming configuration |
|:---:|:---:|:---:|
| ASR (speech recognition) | FunASR (local) | 👍FunASR (local GPU mode) |
| LLM (large model) | ChatGLMLLM (zhipu glm-4-flash) | 👍AliLLM(qwen3-235b-a22b-instruct-2507) or 👍DoubaoLLM(doubao-1-5-pro-32k-250115) |
| VLLM (visual large model) | ChatGLMVLLM (zhipu glm-4v-flash) | 👍QwenVLVLLM (Qianwen qwen2.5-vl-3b-instructh) |
| TTS (speech synthesis) | ✅LinkeraiTTS (Lingxi streaming) | 👍HuoshanDoubleStreamTTS (volcano dual-stream speech synthesis) or 👍AliyunStreamTTS (Alibaba Cloud streaming speech synthesis) |
| Intent (intent recognition) | function_call (function call) | function_call (function call) |
| Memory (memory function) | mem_local_short (local short-term memory) | mem_local_short (local short-term memory) |

If you are concerned about the time consumption of each component, please refer to [Xiaozhi's component performance test report](https://github.com/xinnan-tech/xiaozhi-performance-research), and you can actually test it in your environment according to the test methods in the report.

### 6. I speak very slowly, and Xiaozhi always grabs the words when I pause 🗣️

Suggestion: Find the following section in the configuration file and increase the value of `min_silence_duration_ms` (for example, change it to `1000`):

```yaml
VAD:
  SileroVAD:
    threshold: 0.5
    model_dir: models/snakers4_silero-vad
min_silence_duration_ms: 700 # If there is a long pause in speaking, you can increase this value
```

### 7. Deployment related tutorials
1. [How to perform the most simplified deployment](./Deployment.md)<br/>
2. [How to deploy all modules](./Deployment_all.md)<br/>
3. [How to deploy MQTT gateway to enable MQTT+UDP protocol](./mqtt-gateway-integration.md)<br/>
4. [How to automatically pull the latest code of this project and automatically compile and start it](./dev-ops-integration.md)<br/>
5. [How to integrate with Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>

### 9. Tutorials related to compiling firmware
1. [How to compile Xiaozhi firmware by yourself](./firmware-build.md)<br/>
2. [How to modify the OTA address based on the firmware compiled by Brother Xia](./firmware-setting.md)<br/>

### 10. Expand related tutorials
1. [How to enable mobile phone number registration smart console](./ali-sms-integration.md)<br/>
2. [How to integrate HomeAssistant to achieve smart home control](./homeassistant-integration.md)<br/>
3. [How to turn on the visual model to recognize objects by taking photos](./mcp-vision-integration.md)<br/>
4. [How to deploy MCP access point](./mcp-endpoint-enable.md)<br/>
5. [How to access MCP access point](./mcp-endpoint-integration.md)<br/>
6. [How to obtain device information using MCP method](./mcp-get-device-info.md)<br/>
7. [How to enable voiceprint recognition](./voiceprint-integration.md)<br/>
8. [News plug-in source configuration guide](./newsnow_plugin_config.md)<br/>

### 11. Tutorials related to voice cloning and local voice deployment
1. [How to clone sounds on the smart console](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [How to deploy integrated index-tts local voice](./index-stream-integration.md)<br/>
3. [How to deploy integrated fish-speech local voice](./fish-speech-integration.md)<br/>
4. [How to deploy and integrate PaddleSpeech local voice](./paddlespeech-deploy.md)<br/>

### 12. Performance testing tutorial
1. [Guide to speed testing of each component](./performance_tester.md)<br/>
2. [Regular public test results](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>

### 13. For more questions, please contact us for feedback 💬

You can submit your issues at [issues](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues).