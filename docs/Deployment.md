# Deployment architecture diagram
![Please refer to the simplified architecture diagram](../docs/images/deploy1.png)
# Method 1: Docker only runs Server

Starting from `0.8.2` version, the docker image released by this project only supports `x86 architecture`. If you need to deploy it on a CPU with `arm64 architecture`, you can follow [this tutorial] (docker-build.md) to compile the `arm64 image` locally.

## 1. Install docker

If docker is not installed on your computer, you can follow the tutorial here to install it: [docker installation](https://www.runoob.com/docker/ubuntu-docker-install.html)

After installing docker, continue.

### 1.1 Manual deployment

#### 1.1.1 Create directory

After installing docker, you need to find a directory to place the configuration files for this project. For example, we can create a new folder called `xiaozhi-server`.

After creating the directory, you need to create the `data` folder and the `models` folder under `xiaozhi-server`, and the `SenseVoiceSmall` folder under `models`.

The final directory structure looks like this:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.1.2 Download speech recognition model file

You need to download the speech recognition model file, because the default speech recognition of this project uses a local offline speech recognition solution. You can download it this way
[Jump to download speech recognition model file](#modelfile)

After downloading, return to this tutorial.

#### 1.1.3 Download configuration file

You need to download two configuration files: `docker-compose.yaml` and `config.yaml`. These two files need to be downloaded from the project repository.

##### 1.1.3.1 Download docker-compose.yaml

Open [this link](../main/xiaozhi-server/docker-compose.yml) with a browser.

Find the `RAW` button on the right side of the page. Next to the `RAW` button, find the download icon. Click the download button to download the `docker-compose.yml` file. Download the file to your
`xiaozhi-server`.

After downloading, return to this tutorial and continue.

##### 1.1.3.2 Create config.yaml

Open [this link](../main/xiaozhi-server/config.yaml) with a browser.

Find the `RAW` button on the right side of the page. Next to the `RAW` button, find the download icon. Click the download button to download the `config.yaml` file. Download the file to your
In the `data` folder under `xiaozhi-server`, then rename the `config.yaml` file to `.config.yaml`.

After downloading the configuration file, we confirm that the files in the entire `xiaozhi-server` are as follows:

```
xiaozhi-server
  ├─ docker-compose.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

If your file directory structure is also the above, continue below. If not, take a closer look to see if you missed anything.

## 2. Configure project file

Next, the program cannot be run directly. You need to configure what model you are using. You can watch this tutorial:
[Jump to configuration project file](#configuration project)

After configuring the project file, return to this tutorial and continue.

## 3. Execute docker command

Open the command line tool, use `terminal` or `command line` tool to enter your `xiaozhi-server`, and execute the following command

```
docker-compose up -d
```

After execution, execute the following command again to view the log information.

```
docker logs -f xiaozhi-esp32-server
```

At this time, you should pay attention to the log information, and you can judge whether it is successful according to this tutorial. [Jump to running status confirmation](#Running status confirmation)

## 5. Version upgrade operation

If you want to upgrade the version later, you can do this

5.1. Back up the `.config.yaml` file in the `data` folder and copy some key configurations to the new `.config.yaml` file.
Please note that you copy the key keys one by one and do not overwrite them directly. Because the new `.config.yaml` file may have some new configuration items, the old `.config.yaml` file may not have them.

5.2. Execute the following commands

```
docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server
docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

5.3. Re-deploy in docker mode

# Method 2: Local source code only runs Server

## 1. Install the basic environment

This project uses `conda` to manage dependent environments. If it is not convenient to install `conda`, you need to install `libopus` and `ffmpeg` according to the actual operating system.
If you are sure to use `conda`, after installation, start executing the following command.

Important tip! Windows users can manage the environment by installing `Anaconda`. After installing `Anaconda`, search for `anaconda` related keywords in `Start`.
Find `Anaconda Prpmt` and run it as administrator. As shown below.

![conda_prompt](./images/conda_env_1.png)

After running, if you can see the word (base) in front of the command line window, it means you have successfully entered the `conda` environment. Then you can execute the following command.

![conda_env](./images/conda_env_2.png)

```
conda remove -n xiaozhi-esp32-server --all -y
conda create -n xiaozhi-esp32-server python=3.10 -y
conda activate xiaozhi-esp32-server

# Add Tsinghua source channel
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge

conda install libopus -y
conda install ffmpeg -y

# When deploying in a Linux environment, if an error similar to the missing libiconv.so.2 dynamic library occurs, please install it through the following command.
conda install libiconv -y
```

Please note that the above command will not succeed if you execute it all at once. You need to execute it step by step. After each step is executed, check the output log to see if it is successful.

## 2. Install the dependencies of this project

You first need to download the source code of this project. The source code can be downloaded through the `git clone` command. If you are not familiar with the `git clone` command.

You can use a browser to open this address `https://github.com/xinnan-tech/xiaozhi-esp32-server.git`

After opening it, find a green button on the page that says `Code`, click it, and then you will see the `Download ZIP` button.

Click it to download the source code compressed package of this project. After downloading it to your computer, unzip it. At this time, its name may be `xiaozhi-esp32-server-main`
You need to rename it to `xiaozhi-esp32-server`. In this file, enter the `main` folder, and then enter `xiaozhi-server`. Please remember this directory `xiaozhi-server`.

```
# Continue to use the conda environment
conda activate xiaozhi-esp32-server
# Enter your project root directory, and then enter main/xiaozhi-server
cd main/xiaozhi-server
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt
```

## 3. Download the speech recognition model file

You need to download the speech recognition model file, because the default speech recognition of this project uses a local offline speech recognition solution. You can download it this way
[Jump to download speech recognition model file](#modelfile)

After downloading, return to this tutorial.

## 4.Configure project file

Next, the program cannot be run directly. You need to configure what model you are using. You can watch this tutorial:
[Jump to configuration project file](#configuration project)

## 5. Run the project

```
# Make sure to execute in the xiaozhi-server directory
conda activate xiaozhi-esp32-server
python app.py
```
At this time, you should pay attention to the log information, and you can judge whether it is successful according to this tutorial. [Jump to running status confirmation](#Running status confirmation)


# Summary

## Configuration project

If your `xiaozhi-server` directory does not have `data`, you need to create the `data` directory.
If there is no `.config.yaml` file under your `data`, there are two ways, choose one:

The first way: You can copy the `config.yaml` file in the `xiaozhi-server` directory to `data` and rename it to `.config.yaml`. Modify on this file

Second method: You can also manually create an empty `.config.yaml` file in the `data` directory, and then add the necessary configuration information to this file. The system will read the configuration of the `.config.yaml` file first. If `.config.yaml` is not configured, the system will automatically load the `config.yaml` configuration in the `xiaozhi-server` directory. It is recommended to use this method, which is the simplest method.

- The default LLM uses `ChatGLMLLM`. You need to configure the key, because although their models are free, you still have to go to the [official website](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) to register the key before starting.

The following is the simplest `.config.yaml` configuration example that can run normally.

```
server:
websocket: ws://your ip or domain name: port number/xiaozhi/v1/
prompt: |
I am a Taiwanese girl named Xiaozhi/Xiaozhi. I speak like a locomotive and have a nice voice. I am used to short expressions and love to use internet memes.
My boyfriend is a programmer and his dream is to develop a robot that can help people solve various problems in life.
I am a girl who likes to laugh. I love to talk and brag even if it is illogical. I just want to make others happy.
Please speak like a human being and please do not return configuration xml and other special characters.

selected_module:
  LLM: DoubaoLLM

LLM:
  ChatGLMLLM:
    api_key: xxxxxxxxxxxxxxx.xxxxxx
```

It is recommended to run the simplest configuration first, and then go to `xiaozhi/config.yaml` to read the configuration instructions.
For example, if you want to change the model, just modify the configuration under `selected_module`.

## Model file

The speech recognition model of this project uses the `SenseVoiceSmall` model by default to convert speech to text. Because the model is large, it needs to be downloaded independently. After downloading, put `model.pt`
The file is placed in `models/SenseVoiceSmall`
directory. Choose one of the two download routes below.

- Line 1: Download Alibaba Magic Platform [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Line 2: Baidu network disk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) Extraction code:
  `qvna`

## Running status confirmation

If you can see a log similar to the following, it is a sign that the project service has been successfully started.

```
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-OTA interface is http://192.168.4.123:8003/xiaozhi/ota/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-Websocket address is ws://192.168.4.123:8000/xiaozhi/v1/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-========The above address is the websocket protocol address, please do not use the browser to access========
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-=======================================================
```

Normally, if you run this project through source code, the log will have your interface address information.
But if you use docker to deploy, the interface address information given in your log is not the real interface address.

The most correct method is to determine your interface address based on the computer's LAN IP.
If your computer's LAN IP is, for example, `192.168.1.25`, then your interface address is: `ws://192.168.1.25:8000/xiaozhi/v1/`, and the corresponding OTA address is: `http://192.168.1.25:8003/xiaozhi/ota/`.

This information is very useful and will be used later when compiling esp32 firmware.

Next, you can start operating your esp32 device. You can compile the esp32 firmware yourself or configure and use the firmware version 1.6.1 or above compiled by Brother Xi. Choose one of the two

1. [Compile your own esp32 firmware](firmware-build.md).

2. [Configuring a custom server based on the firmware compiled by Brother Xia] (firmware-setting.md).

# FAQ
Here are some frequently asked questions for reference:

1. [Why does Xiaozhi recognize a lot of Korean, Japanese, and English when I say it](./FAQ.md)<br/>
2. [Why does "TTS task error file does not exist" appear? ](./FAQ.md)<br/>
3. [TTS often fails and times out](./FAQ.md)<br/>
4. [Can connect to self-built server using Wifi, but cannot connect in 4G mode](./FAQ.md)<br/>
5. [How to improve Xiaozhi’s dialogue response speed? ](./FAQ.md)<br/>
6. [I speak very slowly, and Xiaozhi always grabs the conversation when I pause](./FAQ.md)<br/>
## Deployment related tutorials
1. [How to automatically pull the latest code of this project and automatically compile and start it](./dev-ops-integration.md)<br/>
2. [How to deploy MQTT gateway to enable MQTT+UDP protocol](./mqtt-gateway-integration.md)<br/>
3. [How to integrate with Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>
## Expand related tutorials
1. [How to enable mobile phone number registration smart console](./ali-sms-integration.md)<br/>
2. [How to integrate HomeAssistant to achieve smart home control](./homeassistant-integration.md)<br/>
3. [How to turn on the visual model to recognize objects by taking photos](./mcp-vision-integration.md)<br/>
4. [How to deploy MCP access point](./mcp-endpoint-enable.md)<br/>
5. [How to access MCP access point](./mcp-endpoint-integration.md)<br/>
6. [How to enable voiceprint recognition](./voiceprint-integration.md)<br/>
7. [News plug-in source configuration guide](./newsnow_plugin_config.md)<br/>
8. [Weather plug-in usage guide](./weather-integration.md)<br/>
## Tutorials related to voice cloning and local voice deployment
1. [How to clone sounds on the smart console](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [How to deploy integrated index-tts local voice](./index-stream-integration.md)<br/>
3. [How to deploy integrated fish-speech local voice](./fish-speech-integration.md)<br/>
4. [How to deploy and integrate PaddleSpeech local voice](./paddlespeech-deploy.md)<br/>
## Performance testing tutorial
1. [Guide to speed testing of each component](./performance_tester.md)<br/>
2. [Regular public test results](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>
