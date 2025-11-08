# Voiceprint recognition activation guide

This tutorial contains 3 parts
- 1. How to deploy the voiceprint recognition service
- 2. How to configure the voiceprint recognition interface when deploying the entire module?
- 3. How to configure voiceprint recognition in the most simplified deployment

# 1. How to deploy the voiceprint recognition service

## The first step is to download the voiceprint recognition project source code

Open the browser [voiceprint recognition project address](https://github.com/xinnan-tech/voiceprint-api)

After opening it, find a green button on the page that says `Code`, click it, and then you will see the `Download ZIP` button.

Click it to download the source code compressed package of this project. After downloading it to your computer, unzip it. At this time, its name may be `voiceprint-api-main`
You need to rename it to `voiceprint-api`.

## The second step is to create database and tables

Voiceprint recognition relies on the `mysql` database. If you have deployed `Intelligent Console` before, it means that you have already installed `mysql`. You can share it.

You can try using the `telnet` command on the host machine to see if you can access the `3306` port of `mysql` normally.
```
telnet 127.0.0.1 3306
```
If you can access port 3306, please ignore the following content and go directly to step three.

If you cannot access it, you need to recall how your `mysql` was installed.

If your mysql is installed by using the installation package yourself, it means that your `mysql` has been network isolated. You may first solve the problem of accessing the `3306` port of `mysql`.

If your `mysql` is installed through `docker-compose_all.yml` of this project. You need to find the `docker-compose_all.yml` file where you created the database and modify the following content

Before modification
```
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    expose:
      - "3306:3306"
```

After modification
```
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    ports:
      - "3306:3306"
```

Note that the `expose` under `xiaozhi-esp32-server-db` is changed to `ports`. After modification, you need to restart. The following is the command to restart mysql:

```
# Enter the folder where your docker-compose_all.yml is located, for example, mine is xiaozhi-server
cd xiaozhi-server
docker compose -f docker-compose_all.yml down
docker compose -f docker-compose.yml up -d
```

After starting, use the `telnet` command on the host machine to see if you can access the `3306` port of `mysql` normally.
```
telnet 127.0.0.1 3306
```
Normally you can access it this way.

## The third step is to create database and tables
If your host can access the mysql database normally, then create a database named `voiceprint_db` and the `voiceprints` table on mysql.

```
CREATE DATABASE voiceprint_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE voiceprint_db;

CREATE TABLE voiceprints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    speaker_id VARCHAR(255) NOT NULL UNIQUE,
    feature_vector LONGBLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_speaker_id (speaker_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Step 4, configure database connection

Enter the `voiceprint-api` folder and create a folder named `data`.

Copy `voiceprint.yaml` in the root directory of `voiceprint-api` to the `data` folder and rename it to `.voiceprint.yaml`

Next, you need to focus on configuring the database connection in `.voiceprint.yaml`.

```
mysql:
  host: "127.0.0.1"
  port: 3306
  user: "root"
  password: "your_password"
  database: "voiceprint_db"
```

Notice! Since your voiceprint recognition service is deployed using docker, `host` needs to be filled in with the LAN IP of the machine where your `mysql is located`.

Notice! Since your voiceprint recognition service is deployed using docker, `host` needs to be filled in with the LAN IP of the machine where your `mysql is located`.

Notice! Since your voiceprint recognition service is deployed using docker, `host` needs to be filled in with the LAN IP of the machine where your `mysql is located`.

## Step 5, start the program
This project is a very simple one and it is recommended to use docker to run it. However, if you don’t want to use docker to run, you can refer to [this page](https://github.com/xinnan-tech/voiceprint-api/blob/main/README.md) to run using the source code. Here is how docker runs

```
# Enter the source code root directory of this project
cd voiceprint-api

# Clear cache
docker compose -f docker-compose.yml down
docker stop voiceprint-api
docker rm voiceprint-api
docker rmi ghcr.nju.edu.cn/xinnan-tech/voiceprint-api:latest

# Start docker container
docker compose -f docker-compose.yml up -d
# View log
docker logs -f voiceprint-api
```

At this time, the log will output something similar to the following:
```
250711 INFO-🚀 Start: Production environment service starts (Uvicorn), listening address: 0.0.0.0:8005
250711 INFO-============================================================
250711 INFO-Voiceprint interface address: http://127.0.0.1:8005/voiceprint/health?key=abcd
250711 INFO-============================================================
```

Please copy the voiceprint interface address:

Since you are deploying with docker, you must not use the above address directly!

Since you are deploying with docker, you must not use the above address directly!

Since you are deploying with docker, you must not use the above address directly!

You first copy the address and put it in a draft. You need to know what the LAN IP of your computer is. For example, my computer’s LAN IP is `192.168.1.25`, then
It turns out that my interface address
```
http://127.0.0.1:8005/voiceprint/health?key=abcd

```
It will be changed to
```
http://192.168.1.25:8005/voiceprint/health?key=abcd
```

After modification, please use the browser to directly access the `voiceprint interface address`. When code similar to this appears in the browser, it means success.
```
{"total_voiceprints":0,"status":"healthy"}
```

Please keep the modified `voiceprint interface address`, which will be used in the next step.

# 2. How to configure voiceprint recognition when deploying the entire module?

## The first step is to configure the interface
If you are deploying all modules, use the administrator account to log in to the smart console, click on the 'Parameter Dictionary' at the top, and select the 'Parameter Management' function.

Then search for the parameter `server.voice_print`. At this time, its value should be the `null` value.
Click the Modify button and paste the `Voiceprint Interface Address` obtained in the previous step into the `Parameter Value`. Then save.

If it can be saved successfully, it means everything is going well, and you can go to the agent to check the effect. If it fails, it means that the smart console cannot access voiceprint recognition. It is most likely due to the network firewall, or the correct LAN IP is not filled in.

## Step 2 Set the agent memory mode

Enter the role configuration of your agent, set the memory to `local short-term memory`, and be sure to turn on `report text + voice`.

## Step 3 Chat with your agent

Power up your device and chat with him using a normal speaking speed and tone.

## Step 4: Set voiceprint

In the intelligent console, on the `Agent Management` page, in the panel of the agent, there is a `Voiceprint Recognition` button, click it. There is a `Add button` at the bottom. You can register the voiceprint of what someone says.
In the pop-up box, it is recommended to fill in the attribute "Description", which can be the person's occupation, personality, and hobbies. It is convenient for the agent to analyze and understand the speaker.

## Step 3 Chat with your agent

Power up your device and ask it, do you know who I am? If he can answer it, it means that the voiceprint recognition function is normal.

# 3. How to configure voiceprint recognition in the most simplified deployment?

## The first step is to configure the interface
Open the `xiaozhi-server/data/.config.yaml` file (if there is no need to create it), then add/modify the following content:

```
# Voiceprint recognition configuration
voiceprint:
# Voiceprint interface address
url: your voiceprint interface address
# Speaker configuration: speaker_id, name, description
  speakers:
- "test1, Zhang San, Zhang San is a programmer"
- "test2, Li Si, Li Si is a product manager"
- "test3, Wang Wu, Wang Wu is a designer"
```

Paste the `voiceprint interface address` obtained in the previous step into `url`. Then save.

The `speakers` parameter is added as required. Here you need to pay attention to the `speaker_id` parameter, which will be used later to register the voiceprint.

## Step 2 Register voiceprint
If you have started the voiceprint service, you can view the API documentation by visiting `http://localhost:8005/voiceprint/docs` in your local browser. Here we only explain how to use the API for registering voiceprint.

The API address for registering voiceprint is `http://localhost:8005/voiceprint/register`, and the request method is POST.

The request header needs to contain Bearer Token authentication. The token is the part after `?key=` in the `voiceprint interface address`. For example, if my voiceprint registration address is `http://127.0.0.1:8005/voiceprint/health?key=abcd`, then my token is `abcd`.

The request body contains the speaker ID (speaker_id) and the WAV audio file (file). The request example is as follows:

```
curl -X POST \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "speaker_id=your_speaker_id_here" \
  -F "file=@/path/to/your/file" \
  http://localhost:8005/voiceprint/register
```

The `file` here is the audio file of the speaker to be registered, and the `speaker_id` needs to be consistent with the `speaker_id` of the first step of configuring the interface. For example, if I need to register Zhang San's voiceprint, and the `speaker_id' of Zhang San filled in `.config.yaml` is `test1`, then when I register Zhang San's voiceprint, the `speaker_id` filled in the request body is `test1`, and the `file` filled in is the audio file of what Zhang San said.

## Step 3: Start the service

Start Xiaozhi server and voiceprint service, and you can use it normally.
