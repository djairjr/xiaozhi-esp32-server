# Deployment architecture diagram
![Please refer to the full module installation architecture diagram](../docs/images/deploy2.png)
# Method 1: Docker runs the full module
Starting from `0.8.2` version, the docker image released by this project only supports `x86 architecture`. If you need to deploy it on a CPU with `arm64 architecture`, you can follow [this tutorial] (docker-build.md) to compile the `arm64 image` locally.

## 1. Install docker

If docker is not installed on your computer, you can follow the tutorial here to install it: [docker installation](https://www.runoob.com/docker/ubuntu-docker-install.html)

There are two ways to install full modules in docker. You can [use lazy script](./Deployment_all.md#11-lazy script) (author [@VanillaNahida](https://github.com/VanillaNahida))
The script will automatically download the required files and configuration files for you. You can also use [Manual Deployment] (./Deployment_all.md#12-Manual Deployment) to build it from scratch.



### 1.1 Lazy script
Deployment is easy, you can refer to [Video Tutorial](https://www.bilibili.com/video/BV17bbvzHExd/), the text version of the tutorial is as follows:
> [!NOTE]  
> For the time being, it only supports one-click deployment of Ubuntu servers. We have not tried it on other systems and may have some strange bugs.

Use the SSH tool to connect to the server and execute the following script with root privileges
```bash
sudo bash -c "$(wget -qO- https://ghfast.top/https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/main/docker-setup.sh)"
```

The script automatically completes the following operations:
> 1. Install Docker
> 2. Configure mirror source
> 3. Download/Pull the image
> 4. Download the speech recognition model file
> 5. Boot configuration server
>

After completing the simple configuration, refer to the three most important things mentioned in [4. Run the program] (#4. Run the program) and [5. Restart xiaozhi-esp32-server] (#5. Restart xiaozhi-esp32-server). You can use it after completing the three configurations.

### 1.2 Manual deployment

#### 1.2.1 Create directory

After installation, you need to find a directory for the configuration file for this project. For example, we can create a new folder called `xiaozhi-server`.

After creating the directory, you need to create the `data` folder and the `models` folder under `xiaozhi-server`, and the `SenseVoiceSmall` folder under `models`.

The final directory structure looks like this:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.2.2 Download speech recognition model file

The speech recognition model of this project uses the `SenseVoiceSmall` model by default to convert speech to text. Because the model is large, it needs to be downloaded independently. After downloading, put `model.pt`
The file is placed in `models/SenseVoiceSmall`
directory. Choose one of the two download routes below.

- Line 1: Download Alibaba Magic Platform [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Line 2: Baidu network disk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) Extraction code:
  `qvna`


#### 1.2.3 Download configuration file

You need to download two configuration files: `docker-compose_all.yaml` and `config_from_api.yaml`. These two files need to be downloaded from the project repository.

##### 1.2.3.1 Download docker-compose_all.yaml

Open [this link](../main/xiaozhi-server/docker-compose_all.yml) with a browser.

Find the `RAW` button on the right side of the page. Next to the `RAW` button, find the download icon. Click the download button to download the `docker-compose_all.yml` file. Download the file to your
`xiaozhi-server`.

Or directly execute `wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/docker-compose_all.yml` to download.

After downloading, return to this tutorial and continue.

##### 1.2.3.2 Download config_from_api.yaml

Open [this link](../main/xiaozhi-server/config_from_api.yaml) with a browser.

Find the `RAW` button on the right side of the page. Next to the `RAW` button, find the download icon. Click the download button to download the `config_from_api.yaml` file. Download the file to your
In the `data` folder under `xiaozhi-server`, then rename the `config_from_api.yaml` file to `.config.yaml`.

Or directly execute `wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/config_from_api.yaml` to download and save.

After downloading the configuration file, we confirm that the files in the entire `xiaozhi-server` are as follows:

```
xiaozhi-server
  ├─ docker-compose_all.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

If your file directory structure is also the above, continue below. If not, take a closer look to see if you missed anything.

## 2. Back up data

If you have successfully run the smart console before and if your key information is saved on it, please copy the important data from the smart console first. Because during the upgrade process, the original data may be overwritten.

## 3. Clear historical versions of images and containers
Next, open the command line tool, use the `terminal` or `command line` tool to enter your `xiaozhi-server`, and execute the following command

```
docker compose -f docker-compose_all.yml down

docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server

docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web

docker stop xiaozhi-esp32-server-db
docker rm xiaozhi-esp32-server-db

docker stop xiaozhi-esp32-server-redis
docker rm xiaozhi-esp32-server-redis

docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

## 4. Run the program
Execute the following command to start the new version container

```
docker compose -f docker-compose_all.yml up -d
```

After execution, execute the following command again to view the log information.

```
docker logs -f xiaozhi-esp32-server-web
```

When you see the output log, it means that your `Smart Console` has started successfully.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

Please note that only the `Intelligent Console` can run at this moment. If an error is reported on port 8000 `xiaozhi-esp32-server`, ignore it for now.

At this time, you need to use a browser, open the `Smart Console`, link: http://127.0.0.1:8002, and register the first user. The first user is the super administrator, and subsequent users are ordinary users. Ordinary users can only bind devices and configure agents; super administrators can perform model management, user management, parameter configuration and other functions.

There are three important things to do next:

### The first important thing

Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find the first data in the list, the parameter code is `server.secret`, and copy it to `Parameter Value`.

`server.secret` needs to be explained. This `parameter value` is very important because it allows our `Server` to connect to `manager-api`. `server.secret` is a secret that is automatically and randomly generated every time the manager module is deployed from scratch.

After copying the `parameter value`, open the `.config.yaml` file in the `data` directory under `xiaozhi-server`. At this point your configuration file should look like this:

```
manager-api:
  url:  http://127.0.0.1:8002/xiaozhi
secret: your server.secret value
```
1. Copy the `parameter value` of `server.secret` that you just copied from `Intelligent Console` to the `secret` in the `.config.yaml` file.

2. Because you are deploying with docker, change `url` to the following `http://xiaozhi-esp32-server-web:8002/xiaozhi`

3. Because you are deploying with docker, change `url` to the following `http://xiaozhi-esp32-server-web:8002/xiaozhi`

4. Because you are deploying with docker, change `url` to the following `http://xiaozhi-esp32-server-web:8002/xiaozhi`

Similar effect
```
manager-api:
  url: http://xiaozhi-esp32-server-web:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

After saving, continue to do the second important thing

### The second important thing

Use the super administrator account to log in to the smart console, find `Model Configuration` in the top menu, then click `Large Language Model` in the left column, find the first piece of data `Wisdom Spectrum AI`, and click the `Modify` button.
After the modification box pops up, fill in the key of `Zhipu AI` you registered into `API Key`. Then click Save.

## 5. Restart xiaozhi-esp32-server

Next open the command line tool and use the `Terminal` or `Command Line` tool to enter
```
docker restart xiaozhi-esp32-server
docker logs -f xiaozhi-esp32-server
```
If you can see logs similar to the following, it is a sign that the server has started successfully.

```
25-02-23 12:01:09[core.websocket_server] - INFO - The Websocket address is ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.websocket_server] - INFO - =======The above address is the websocket protocol address, please do not access it with a browser========
25-02-23 12:01:09[core.websocket_server] - INFO - If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
25-02-23 12:01:09[core.websocket_server] - INFO - =======================================================
```

Since you are deploying a full module, you have two important interfaces that need to be written to esp32.

OTA interface:
```
http://IP of your host LAN:8002/xiaozhi/ota/
```

Websocket interface:
```
ws://your host’s ip:8000/xiaozhi/v1/
```

### The third important thing

Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find that the parameter code is `server.websocket`, and enter your `Websocket interface`.

Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find the number code `server.ota`, and enter your `OTA interface`.

Next, you can start operating your esp32 device. You can compile the esp32 firmware yourself or configure and use the firmware version 1.6.1 or above compiled by Brother Xi. Choose one of the two

1. [Compile your own esp32 firmware](firmware-build.md).

2. [Configuring a custom server based on the firmware compiled by Brother Xia] (firmware-setting.md).


# Method 2: Run the entire module from local source code

## 1. Install MySQL database

If MySQL has been installed on this machine, you can directly create a database named `xiaozhi_esp32_server` in the database.

```sql
CREATE DATABASE xiaozhi_esp32_server CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If you don't have MySQL yet, you can install mysql through docker

```
docker run --name xiaozhi-esp32-server-db -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -e MYSQL_DATABASE=xiaozhi_esp32_server -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" -e TZ=Asia/Shanghai -d mysql:latest
```

## 2. Install redis

If you don't have Redis yet, you can install redis through docker

```
docker run --name xiaozhi-esp32-server-redis -d -p 6379:6379 redis
```

## 3. Run the manager-api program

3.1 Install JDK21 and set JDK environment variables

3.2 Install Maven and set Maven environment variables

3.3 Use Vscode programming tool to install Java environment related plug-ins

3.4 Use the Vscode programming tool to load the manager-api module

Configure database connection information in `src/main/resources/application-dev.yml`

```
spring:
  datasource:
    username: root
    password: 123456
```
Configure Redis connection information in `src/main/resources/application-dev.yml`
```
spring:
    data:
      redis:
        host: localhost
        port: 6379
        password:
        database: 0
```

3.5 Run the main program

This project is a SpringBoot project, and the startup method is:
Open `Application.java` and run the `Main` method to start

```
Path address:
src/main/java/xiaozhi/AdminApplication.java
```

When you see the output log, it means that your `manager-api` started successfully.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

## 4. Run the manager-web program

4.1 Install nodejs

4.2 Use the Vscode programming tool to load the manager-web module

Terminal command enters the manager-web directory

```
npm install
```
then start
```
npm run serve
```

Please note that if the interface of your manager-api is not `http://localhost:8002`, please modify it during development.
Path in `main/manager-web/.env.development`

After running successfully, you need to use the browser to open the `Intelligent Console`, link: http://127.0.0.1:8001, and register the first user. The first user is the super administrator, and subsequent users are ordinary users. Ordinary users can only bind devices and configure agents; super administrators can perform model management, user management, parameter configuration and other functions.


Important: After successful registration, use the super administrator account to log in to the smart console, find `Model Configuration` in the top menu, then click `Large Language Model` in the left column, find the first piece of data `Wisdom Spectrum AI`, and click the `Modify` button.
After the modification box pops up, fill in the key of `Zhipu AI` you registered into `API Key`. Then click Save.

Important: After successful registration, use the super administrator account to log in to the smart console, find `Model Configuration` in the top menu, then click `Large Language Model` in the left column, find the first piece of data `Wisdom Spectrum AI`, and click the `Modify` button.
After the modification box pops up, fill in the key of `Zhipu AI` you registered into `API Key`. Then click Save.

Important: After successful registration, use the super administrator account to log in to the smart console, find `Model Configuration` in the top menu, then click `Large Language Model` in the left column, find the first piece of data `Wisdom Spectrum AI`, and click the `Modify` button.
After the modification box pops up, fill in the key of `Zhipu AI` you registered into `API Key`. Then click Save.

## 5. Install Python environment

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

## 6. Install the dependencies of this project

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

### 7. Download the speech recognition model file

The speech recognition model of this project uses the `SenseVoiceSmall` model by default to convert speech to text. Because the model is large, it needs to be downloaded independently. After downloading, put `model.pt`
The file is placed in `models/SenseVoiceSmall`
directory. Choose one of the two download routes below.

- Line 1: Download Alibaba Magic Platform [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Line 2: Baidu network disk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) Extraction code:
  `qvna`

## 8.Configure project file

Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find the first data in the list, the parameter code is `server.secret`, and copy it to `Parameter Value`.

`server.secret` needs to be explained. This `parameter value` is very important because it allows our `Server` to connect to `manager-api`. `server.secret` is a secret that is automatically and randomly generated every time the manager module is deployed from scratch.

If your `xiaozhi-server` directory does not have `data`, you need to create the `data` directory.
If there is no `.config.yaml` file under your `data`, you can copy the `config_from_api.yaml` file in the `xiaozhi-server` directory to `data` and rename it to `.config.yaml`

After copying the `parameter value`, open the `.config.yaml` file in the `data` directory under `xiaozhi-server`. At this point your configuration file should look like this:

```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
secret: your server.secret value
```

Copy the `parameter value` of `server.secret` that you just copied from `Intelligent Console` to the `secret` in the `.config.yaml` file.

Similar effect
```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

## 5. Run the project

```
# Make sure to execute in the xiaozhi-server directory
conda activate xiaozhi-esp32-server
python app.py
```

If you can see a log similar to the following, it is a sign that the project service has been successfully started.

```
25-02-23 12:01:09[core.websocket_server] - INFO - Server is running at ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.websocket_server] - INFO - =======The above address is the websocket protocol address, please do not access it with a browser========
25-02-23 12:01:09[core.websocket_server] - INFO - If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
25-02-23 12:01:09[core.websocket_server] - INFO - =======================================================
```

Since you are deploying a full module, you have two important interfaces.

OTA interface:
```
http://IP of your computer LAN:8002/xiaozhi/ota/
```

Websocket interface:
```
ws://IP of your computer LAN:8000/xiaozhi/v1/
```

Please be sure to write the above two interface addresses into the smart console: they will affect the websocket address issuance and automatic upgrade functions.

1. Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find the parameter code is `server.websocket`, and enter your `Websocket interface`.

2. Use the super administrator account to log in to the smart console, find `Parameter Management` in the top menu, find the number code `server.ota`, and enter your `OTA interface`.


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
