# MCP Access Point Deployment User Guide

This tutorial contains 3 parts
- 1. How to deploy the MCP access point service
- 2. How to configure the MCP access point when deploying all modules?
- 3. How to configure the MCP access point when deploying a single module?

# 1. How to deploy the MCP access point service

## The first step is to download the mcp access point project source code

Open the browser [mcp access point project address](https://github.com/xinnan-tech/mcp-endpoint-server)

After opening it, find a green button on the page that says `Code`, click it, and then you will see the `Download ZIP` button.

Click it to download the source code compressed package of this project. After downloading it to your computer, unzip it. At this time, its name may be `mcp-endpoint-server-main`
You need to rename it to `mcp-endpoint-server`.

## The second step is to start the program
This project is a very simple one and it is recommended to use docker to run it. However, if you don’t want to use docker to run, you can refer to [this page](https://github.com/xinnan-tech/mcp-endpoint-server/blob/main/README_dev.md) to run using the source code. Here is how docker runs

```
# Enter the source code root directory of this project
cd mcp-endpoint-server

# Clear cache
docker compose -f docker-compose.yml down
docker stop mcp-endpoint-server
docker rm mcp-endpoint-server
docker rmi ghcr.nju.edu.cn/xinnan-tech/mcp-endpoint-server:latest

# Start docker container
docker compose -f docker-compose.yml up -d
# View log
docker logs -f mcp-endpoint-server
```

At this time, the log will output something similar to the following:
```
250705 INFO-======The following addresses are the smart console/single module MCP access point addresses====
250705 INFO-Intelligent console MCP parameter configuration: http://172.22.0.2:8004/mcp_endpoint/health?key=abc
250705 INFO-Single module deployment MCP access point: ws://172.22.0.2:8004/mcp_endpoint/mcp/?token=def
250705 INFO-=====Please choose to use according to the specific deployment, do not disclose it to anyone======
```

Please copy the two interface addresses:

Since you are deploying with docker, you must not use the above address directly!

Since you are deploying with docker, you must not use the above address directly!

Since you are deploying with docker, you must not use the above address directly!

You first copy the address and put it in a draft. You need to know what the LAN IP of your computer is. For example, my computer’s LAN IP is `192.168.1.25`, then
It turns out that my interface address
```
Intelligent console MCP parameter configuration: http://172.22.0.2:8004/mcp_endpoint/health?key=abc
Single module deployment MCP access point: ws://172.22.0.2:8004/mcp_endpoint/mcp/?token=def
```
It will be changed to
```
Intelligent console MCP parameter configuration: http://192.168.1.25:8004/mcp_endpoint/health?key=abc
Single module deployment MCP access point: ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=def
```

After modification, please use the browser to directly access the `Intelligent Console MCP Parameter Configuration`. When code similar to this appears in the browser, it means success.
```
{"result":{"status":"success","connections":{"tool_connections":0,"robot_connections":0,"total_connections":0}},"error":null,"id":null,"jsonrpc":"2.0"}
```

Please keep the above two `interface addresses`, they will be used in the next step.

# 2. How to configure the MCP access point when deploying the whole module?

If you are deploying all modules, use the administrator account to log in to the smart console, click on the 'Parameter Dictionary' at the top, and select the 'Parameter Management' function.

Then search for the parameter `server.mcp_endpoint`. At this time, its value should be the `null` value.
Click the Modify button and paste the `Intelligent Console MCP Parameter Configuration` obtained in the previous step into the `Parameter Value`. Then save.

If it can be saved successfully, it means everything is going well, and you can go to the agent to check the effect. If it fails, it means that the smart console cannot access the mcp access point. It is most likely due to the network firewall, or the correct LAN IP is not filled in.

# 3. How to configure the MCP access point when deploying a single module?

If you are deploying a single module, find your configuration file `data/.config.yaml`.
Search for `mcp_endpoint` in the configuration file. If it is not found, you can add `mcp_endpoint` configuration. Similar to what I am
```
server:
websocket: ws://your ip or domain name: port number/xiaozhi/v1/
  http_port: 8002
log:
  log_level: INFO

# There may be more configuration here..

mcp_endpoint: your access point websocket address
```
At this time, please paste the `Single module deployment MCP access point` obtained in `How to deploy the MCP access point service` into `mcp_endpoint`. something like this

```
server:
websocket: ws://your ip or domain name: port number/xiaozhi/v1/
  http_port: 8002
log:
  log_level: INFO

# There may be more configuration here

mcp_endpoint: ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=def
```

After configuration, starting a single module will output the following log.
```
250705[__main__]-INFO-Initialization component: vad successful SileroVAD
250705[__main__]-INFO-Initialization component: asr successful FunASRServer
250705[__main__]-INFO-OTA interface is http://192.168.1.25:8002/xiaozhi/ota/
250705[__main__]-INFO-Visual analysis interface is http://192.168.1.25:8002/mcp/vision/explain
250705[__main__]-INFO-mcp access point is ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
250705[__main__]-INFO-Websocket address is ws://192.168.1.25:8000/xiaozhi/v1/
250705[__main__]-INFO-========The above address is the websocket protocol address, please do not use a browser to access it========
250705[__main__]-INFO-如想测试websocket请用谷歌浏览器打开test目录下的test_page.html
250705[__main__]-INFO-=============================================================
```

As above, if you can output something like `mcp access point is` in `ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc`, it means the configuration is successful.

