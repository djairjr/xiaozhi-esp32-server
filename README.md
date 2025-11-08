[![Banners](docs/images/banner1.png)](https://github.com/xinnan-tech/xiaozhi-esp32-server)

<h1 align="center">Xiaozhi backend service xiaozhi-esp32-server</h1>

<p align="center">
This project is based on the theory and technology of human-computer symbiosis intelligence to develop intelligent terminal software and hardware systems<br/>It is an open source intelligent hardware project
<a href="https://github.com/78/xiaozhi-esp32">xiaozhi-esp32</a> provides back-end services<br/>
According to <a href="https://ccnphfhqs21z.feishu.cn/wiki/M0XiwldO9iJwHikpXD5cEx71nKh">Xiaozhi communication protocol</a>, it is implemented using Python, Java and Vue<br/>
Support MQTT+UDP protocol, Websocket protocol, MCP access point, voiceprint recognition
</p>

<p align="center">
<a href="./README_en.md">English</a>
· <a href="./docs/FAQ.md">FAQ</a>
· <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/issues">Feedback issues</a>
· <a href="./README.md#%E9%83%A8%E7%BD%B2%E6%96%87%E6%A1%A3">Deployment Document</a>
· <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/releases">Update log</a>
</p>
<p align="center">
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/releases">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/v/release/xinnan-tech/xiaozhi-esp32-server?logo=docker" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/graphs/contributors">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/xinnan-tech/xiaozhi-esp32-server?logo=github" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/xinnan-tech/xiaozhi-esp32-server?color=0088ff" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/pulls">
    <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/xinnan-tech/xiaozhi-esp32-server?color=0088ff" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/LICENSE">
    <img alt="GitHub pull requests" src="https://img.shields.io/badge/license-MIT-white?labelColor=black" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server">
    <img alt="stars" src="https://img.shields.io/github/stars/xinnan-tech/xiaozhi-esp32-server?color=ffcb47&labelColor=black" />
  </a>
</p>

<p align="center">
Spearheaded by Professor Siyuan Liu's Team (South China University of Technology)
</br>
Research and development led by Professor Liu Siyuan's team (South China University of Technology)
</br>
<img src="./docs/images/hnlg.jpg" alt="South China University of Technology" width="50%">
</p>

---

## Applicable people 👥

This project needs to be used with ESP32 hardware device. If you have purchased ESP32 related hardware and successfully connected the back-end service deployed by Xiage, and want to build your own independently
`xiaozhi-esp32` backend service, then this project is very suitable for you.

Want to see the effect? Please click on the video 🎥

<table>
  <tr>
    <td>
        <a href="https://www.bilibili.com/video/BV1FMFyejExX" target="_blank">
         <picture>
<img alt="Response speed experience" src="docs/images/demo9.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1vchQzaEse" target="_blank">
         <picture>
<img alt="Secrets for Speed ​​Optimization" src="docs/images/demo6.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1C1tCzUEZh" target="_blank">
         <picture>
<img alt="Complex Medical Scenario" src="docs/images/demo1.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1zUW5zJEkq" target="_blank">
         <picture>
<img alt="MQTT command issuance" src="docs/images/demo4.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1Exu3zqEDe" target="_blank">
         <picture>
<img alt="Voiceprint Recognition" src="docs/images/demo14.png" />
         </picture>
        </a>
    </td>
  </tr>
  <tr>
    <td>
        <a href="https://www.bilibili.com/video/BV1pNXWYGEx1" target="_blank">
         <picture>
<img alt="Control home appliance switches" src="docs/images/demo5.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1ZQKUzYExM" target="_blank">
         <picture>
<img alt="MCP Access Point" src="docs/images/demo13.png" />
         </picture>
        </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1TJ7WzzEo6" target="_blank">
         <picture>
<img alt="Multiple command tasks" src="docs/images/demo11.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1VC96Y5EMH" target="_blank">
         <picture>
<img alt="Play music" src="docs/images/demo7.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1Z8XuYZEAS" target="_blank">
         <picture>
<img alt="Weather plug-in" src="docs/images/demo8.png" />
         </picture>
        </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://www.bilibili.com/video/BV12J7WzBEaH" target="_blank">
         <picture>
<img alt="Real-time interruption" src="docs/images/demo10.png" />
         </picture>
        </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1Co76z7EvK" target="_blank">
         <picture>
<img alt="Take photos to identify items" src="docs/images/demo12.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV1CDKWemEU6" target="_blank">
         <picture>
<img alt="Custom sound" src="docs/images/demo2.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV12yA2egEaC" target="_blank">
         <picture>
<img alt="Communicate in Cantonese" src="docs/images/demo3.png" />
         </picture>
        </a>
    </td>
    <td>
        <a href="https://www.bilibili.com/video/BV17LXWYvENb" target="_blank">
         <picture>
<img alt="Broadcast news" src="docs/images/demo0.png" />
         </picture>
        </a>
    </td>
  </tr>
</table>

---

## WARNING ⚠️

1. This project is open source software. There is no commercial partnership between this software and any third-party API service provider (including but not limited to speech recognition, large model, speech synthesis and other platforms), and no guarantee of any kind is provided for its service quality or financial security.
Users are advised to give priority to service providers that hold relevant business licenses and read their service agreements and privacy policies carefully. This software does not host any account keys, does not participate in fund flows, and does not bear the risk of loss of recharge funds.

2. The functions of this project are not perfect and have not passed the network security evaluation. Please do not use it in a production environment. If you deploy and study this project in a public network environment, be sure to take necessary protection.

---

## Deployment documentation

![Banners](docs/images/banner2.png)

This project provides two deployment methods, please choose according to your specific needs:

#### 🚀 Deployment method selection
| Deployment methods | Features | Applicable scenarios | Deployment documents | Configuration requirements | Video tutorials |
|---------|------|---------|---------|---------|---------|
| **The most simplified installation** | Intelligent dialogue, IOT, MCP, visual perception | Low configuration environment, data is stored in configuration files, no database required | [①Docker version](./docs/Deployment.md#%E6%96%B9%E5%BC%8F%E4%B8%80docker%E5%8F%AA%E8%BF%90%E8%A1%8Cserver) / [②Source code deployment](./docs/Deployment.md#%E6%96%B9%E5%BC%8F%E4%BA%8C%E6%9C%AC%E5%9C%B0%E6%BA%90%E7%A0%81%E5%8F%AA%E8%BF%90%E8%A1%8Cserver)| If you use `FunASR`, you need 2 cores and 4G. If you use full API, you need 2 cores and 2G | - |
| **Full module installation** | Intelligent dialogue, IOT, MCP access point, voiceprint recognition, visual perception, OTA, intelligent console | Complete functional experience, data is stored in the database |[①Docker version](./docs/Deployment_all.md#%E6%96%B9%E5%BC%8F%E4%B8%80docker%E8%BF%90%E8%A1%8C%E5%85%A8%E6%A8%A1%E5%9D%97) / [②Source code deployment](./docs/Deployment_all.md#%E6%96%B9%E5%BC%8F%E4%BA%8C%E6%9C%AC%E 5%9C%B0%E6%BA%90%E7%A0%81%E8%BF%90%E8%A1%8C%E5%85%A8%E6%A8%A1%E5%9D%97) / [③Source code deployment automatic update tutorial](./docs/dev-ops-integration.md) | If you use `FunASR`, you need 4 cores 8G, if you use full API, you need 2 cores 4G| [Local source code startup video tutorial](https://www.bilibili.com/video/BV1wBJhz4Ewe) |

For frequently asked questions and related tutorials, please refer to [this link](./docs/FAQ.md)

> 💡 Tip: The following is the test platform after deployment according to the latest code. You can burn the test if necessary. The concurrency is 6, and the data will be cleared every day.

```
Smart console address: https://2662r3426b.vicp.fun
Intelligent console (h5 version): https://2662r3426b.vicp.fun/h5/index.html

Service test tool: https://2662r3426b.vicp.fun/test/
OTA interface address: https://2662r3426b.vicp.fun/xiaozhi/ota/
Websocket interface address: wss://2662r3426b.vicp.fun/xiaozhi/v1/
```

#### 🚩 Configuration instructions and recommendations
> [!Note]
> This project provides two configuration options:
> 
> 1. `Free entry' configuration: suitable for individual family use, all components are free plans, no additional payment is required.
> 
> 2. `Streaming Configuration`: Suitable for demonstrations, training, more than 2 concurrent scenarios, etc., using streaming processing technology, faster response and better experience.
> 
> Starting from the `0.5.2` version, the project supports streaming configuration. Compared with the earlier version, the response speed is increased by about `2.5 seconds`, significantly improving the user experience.

| Module name | Free entry-level setup | Streaming configuration |
|:---:|:---:|:---:|
| ASR (speech recognition) | FunASR (local) | 👍FunASR (local GPU mode) |
| LLM (large model) | ChatGLMLLM (zhipu glm-4-flash) | 👍AliLLM(qwen3-235b-a22b-instruct-2507) or 👍DoubaoLLM(doubao-1-5-pro-32k-250115) |
| VLLM (visual large model) | ChatGLMVLLM (zhipu glm-4v-flash) | 👍QwenVLVLLM (Qianwen qwen2.5-vl-3b-instructh) |
| TTS (speech synthesis) | ✅LinkeraiTTS (Lingxi streaming) | 👍HuoshanDoubleStreamTTS (volcano dual-stream speech synthesis) or 👍AliyunStreamTTS (Alibaba Cloud streaming speech synthesis) |
| Intent (intent recognition) | function_call (function call) | function_call (function call) |
| Memory (memory function) | mem_local_short (local short-term memory) | mem_local_short (local short-term memory) |

If you are concerned about the time consumption of each component, please refer to [Xiaozhi's component performance test report](https://github.com/xinnan-tech/xiaozhi-performance-research), and you can actually test it in your environment according to the test methods in the report.

#### 🔧 Test Tools
This project provides the following testing tools to help you verify your system and select the appropriate model:

| Tool name | Location | How to use | Function description |
|:---:|:---|:---:|:---:|
| Audio interactive testing tool | main》xiaozhi-server》test》test_page.html | Use Google Chrome to open directly | Test the audio playback and reception functions and verify whether the Python side audio processing is normal |
| Model response testing tool | main》xiaozhi-server》performance_tester.py | Execute `python performance_tester.py` | Test the response speed of the three core modules of ASR (speech recognition), LLM (large model), VLLM (visual model), and TTS (speech synthesis) |

> 💡 Tip: When testing model speed, only models configured with keys will be tested.

---
## Feature List ✨
### Implemented ✅
![Please refer to the full module installation architecture diagram](docs/images/deploy2.png)
| Function module | Description |
|:---:|:---|
| Core architecture | Based on [MQTT+UDP gateway](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/mqtt-gateway-integration.md), WebSocket, HTTP server, providing a complete console management and authentication system |
| Voice interaction | Supports streaming ASR (speech recognition), streaming TTS (speech synthesis), VAD (voice activity detection), and supports multi-language recognition and speech processing |
| Voiceprint recognition | Supports multi-user voiceprint registration, management and recognition, processes in parallel with ASR, identifies the speaker's identity in real time and passes it to LLM for personalized response |
| Intelligent dialogue | Supports multiple LLMs (large language models) to achieve intelligent dialogue |
| Visual perception | Supports multiple VLLMs (visual large models) to achieve multi-modal interaction |
| Intent recognition | Supports LLM intent recognition, Function Call function invocation, and provides plug-in intent processing mechanism |
| Memory system | Supports local short-term memory, mem0ai interface memory, and has memory summary function |
| Tool call | Supports client IOT protocol, client MCP protocol, server MCP protocol, MCP access point protocol, and custom tool functions |
| Command delivery | Relying on the MQTT protocol, it supports issuing MCP commands from the smart console to the ESP32 device |
| Management backend | Provides a Web management interface to support user management, system configuration and device management; the interface supports simplified Chinese, traditional Chinese, and English display |
| Testing tools | Provides performance testing tools, visual model testing tools and audio interaction testing tools |
| Deployment support | Supports Docker deployment and local deployment, providing complete configuration file management |
| Plug-in system | Supports function plug-in extension, custom plug-in development and plug-in hot loading |

### Under development 🚧

To learn about the specific development plan progress, [please click here](https://github.com/users/xinnan-tech/projects/3). For frequently asked questions and related tutorials, please refer to [this link](./docs/FAQ.md)

If you are a software developer, here is an ["Open Letter to Developers"](docs/contributor_open_letter.md), welcome to join!

---

## Product Ecology 👬
Xiaozhi is an ecosystem. When you use this product, you can also look at other [excellent projects] in this ecosystem (https://github.com/78/xiaozhi-esp32?tab=readme-ov-file#%E7%9B%B8%E5%85%B3%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE)

---

## List of platforms/components supported by this project 📋
### LLM language model

| How to use | Supported platform | Free platform |
|:---:|:---:|:---:|
| openai interface call | Alibaba Bailian, Volcano Engine Beanbag, Deep Search, Zhipu ChatGLM, Gemini | Zhipu ChatGLM, Gemini |
| ollama interface call | Ollama | - |
| dify interface call | Dify | - |
| fastgpt interface call | Fastgpt | - |
| coze interface call | Coze | - |
| xinference interface call | Xinference | - |
| homeassistant interface call | HomeAssistant | - |

In fact, any LLM that supports openai interface calls can be accessed and used.

---

### VLLM vision model

| How to use | Supported platform | Free platform |
|:---:|:---:|:---:|
| openai interface call | Alibaba Bailian, Zhipu ChatGLMVLLM | Zhipu ChatGLMVLLM |

In fact, any VLLM that supports openai interface calls can be accessed and used.

---

### TTS speech synthesis

| How to use | Supported platform | Free platform |
|:---:|:---:|:---:|
| Interface call | EdgeTTS, Volcano Engine Beanbao TTS, Tencent Cloud, Alibaba Cloud TTS, Alibaba Cloud Streaming TTS, CosyVoiceSiliconflow, TTS302AI, CozeCnTTS, GizwitsTTS, ACGNTTS, OpenAITTS, Coincidence Streaming TTS, MinimaxTTS, Volcano Dual Stream TTS | CosyVoiceSiliconflow TTS, EdgeTTS, CosyVoiceSiliconflow (part) |
| Local Services | FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3, Index-TTS, PaddleSpeech | Index-TTS, PaddleSpeech, FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3 |

---

### VAD Voice Activity Detection

| Type | Platform name | Usage | Charging model | Remarks |
|:---:|:---------:|:----:|:----:|:--:|
| VAD | SileroVAD | Local use | Free | |

---

### ASR Speech Recognition

| How to use | Supported platform | Free platform |
|:---:|:---:|:---:|
| Local use | FunASR, SherpaASR | FunASR, SherpaASR |
| Interface call | DoubaoASR, Doubao streaming ASR, FunASRServer, TencentASR, AliyunASR, Aliyun streaming ASR, Baidu ASR, OpenAI ASR | FunASRServer |

---

### Voiceprint voiceprint recognition

| How to use | Supported platform | Free platform |
|:---:|:---:|:---:|
| Local use | 3D-Speaker | 3D-Speaker |

---

### Memory memory storage

| Type | Platform name | Usage | Charging model | Remarks |
|:------:|:---------------:|:----:|:---------:|:--:|
| Memory | mem0ai | Interface call | 1000 times/month quota | |
| Memory | mem_local_short | 本地总结 |    免费     |    |
| Memory | nomem | No memory mode | Free | |

---

### Intent intent recognition

| Type | Platform name | Usage | Charging model | Remarks |
|:------:|:-------------:|:----:|:-------:|:---------------------:|
| Intent | intent_llm | Interface call | Charge based on LLM | Identify intent through large model, strong versatility |
| Intent | function_call | Interface call | Charged according to LLM | Complete the intention through large model function call, fast and good effect |
| Intent | nointent | No intent mode | Free | No intent recognition is performed, and the conversation result is returned directly |

---

## Acknowledgments 🙏

| Logo | Project/Company | Description |
|:---:|:---:|:---|
| <img src="./docs/images/logo_bailing.png" width="160"> | [Bailing Voice Conversation Robot](https://github.com/wwbin2017/bailing) | This project is inspired by [Bailing Voice Conversation Robot](https://github.com/wwbin2017/bailing) and implemented on the basis of it |
| <img src="./docs/images/logo_tenclass.png" width="160"> | [Shifangronghai](https://www.tenclass.com/) | Thanks to [Shifangronghai](https://www.tenclass.com/) for formulating standard communication protocols, multi-device compatibility solutions and high-concurrency scenario practice demonstrations for Xiaozhi Ecology; providing full-link technical document support for this project |
| <img src="./docs/images/logo_xuanfeng.png" width="160"> | [Xuanfeng Technology](https://github.com/Eric0308) | Thanks to [Xuanfeng Technology](https://github.com/Eric0308) for contributing the implementation code of the function calling framework, MCP communication protocol and plug-in calling mechanism. Through the standardized instruction scheduling system and dynamic expansion capabilities, it has significantly improved the interaction efficiency and functional scalability of front-end devices (IoT) |
| <img src="./docs/images/logo_junsen.png" width="160"> | [huangjunsen](https://github.com/huangjunsen0406) | Thanks to [huangjunsen](https://github.com/huangjunsen0406) Contributed to the `Smart Console Mobile' module, which enables efficient control and real-time interaction of cross-platform mobile devices, greatly improving the operational convenience and management efficiency of the system in mobile scenarios |
| <img src="./docs/images/logo_huiyuan.png" width="160"> | [Huiyuan Design](http://ui.kwd988.net/) | Thanks to [Huiyuan Design](http://ui.kwd988.net/) for providing professional visual solutions for this project, using its practical design experience in serving over a thousand companies to empower the user experience of this project's products |
| <img src="./docs/images/logo_qinren.png" width="160"> | [Xi'an Qinren Information Technology](https://www.029app.com/) | Thanks to [Xi'an Qinren Information Technology](https://www.029app.com/) for deepening the visual system of this project and ensuring the consistency and scalability of the overall design style in multi-scenario applications |
| <img src="./docs/images/logo_contributors.png" width="160"> | [Code Contributors](https://github.com/xinnan-tech/xiaozhi-esp32-server/graphs/contributors) | Thanks to [all code contributors](https://github.com/xinnan-tech/xiaozhi-esp32-server/graphs/contributors) contributors, your efforts have made the project more robust and powerful. |


<a href="https://star-history.com/#xinnan-tech/xiaozhi-esp32-server&Date">

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date" />
 </picture>
</a>