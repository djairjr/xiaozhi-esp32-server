#MCP Access Point User Guide

This tutorial uses the open-source mcp calculator function of Xiago as an example to introduce how to connect your own customized mcp service to your own access point.

The premise of this tutorial is that your `xiaozhi-server` has enabled the mcp access point function. If you have not enabled it yet, you can enable it first according to [this tutorial](./mcp-endpoint-enable.md).

# How to connect a simple mcp function to the agent, such as the calculator function

### If you deploy a full module
If you are deploying a full module, you can enter the intelligent console, agent management, click `Configure Role`, and there is an `Edit Function` button to the right of `Intent Recognition`.

Click this button. In the pop-up page, at the bottom, there will be an `MCP access point`. Normally, the `MCP access point address` of this agent will be displayed. Next, we will extend the function of a calculator based on MCP technology to this agent.

This `MCP access point address` is very important, you will use it later.

### If you are deploying a single module
If you are deploying a single module and you have configured the MCP access point address in the configuration file, then normally, when the single module deployment is started, the following log will be output.
```
250705[__main__]-INFO-Initialization component: vad successful SileroVAD
250705[__main__]-INFO-Initialization component: asr successful FunASRServer
250705[__main__]-INFO-OTA interface is http://192.168.1.25:8002/xiaozhi/ota/
250705[__main__]-INFO-Visual analysis interface is http://192.168.1.25:8002/mcp/vision/explain
250705[__main__]-INFO-mcp access point is ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
250705[__main__]-INFO-Websocket address is ws://192.168.1.25:8000/xiaozhi/v1/
250705[__main__]-INFO-========The above address is the websocket protocol address, please do not use a browser to access it========
250705[__main__]-INFO-If you want to test websocket, please use Google Chrome to open test_page.html in the test directory
250705[__main__]-INFO-=============================================================
```

As above, in the output `mcp access point is`, `ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc` is your `MCP access point address`.

This `MCP access point address` is very important, you will use it later.

## The first step is to download the Xia Ge MCP calculator project code

Open the [calculator project](https://github.com/78/mcp-calculator) written by Brother Xia in the browser.

After opening it, find a green button on the page that says `Code`, click it, and then you will see the `Download ZIP` button.

Click it to download the source code compressed package of this project. After downloading it to your computer, unzip it. At this time, its name may be `mcp-calculator-main`
You need to rename it to `mcp-calculator`. Next, we use the command line to enter the project directory and install the dependencies.


```bash
# Enter the project directory
cd mcp-calculator

conda remove -n mcp-calculator --all -y
conda create -n mcp-calculator python=3.10 -y
conda activate mcp-calculator

pip install -r requirements.txt
```

## Step 2 Start

Before starting, copy the address of the MCP access point from the intelligent body of your smart console.

For example, the mcp address of my agent is
```
ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
```

Start typing commands

```bash
export MCP_ENDPOINT=ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
```

After inputting, start the program

```bash
python mcp_pipe.py calculator.py
```

### If you are deploying smart console
If you are deploying the smart console, after starting it, you can enter the smart console again, click Refresh MCP access status, and you will see your extended function list.

### If you are deploying a single module
If you deploy a single module, when the device is connected, a similar log will be output, indicating success.

```
250705 -INFO-Initializing MCP access point: wss://2662r3426b.vicp.fun/mcp_e
250705 - INFO - Send MCP access point initialization message
250705 -INFO-MCP access point connected successfully
250705 -INFO-MCP access point initialization successful
250705-INFO-Unified Tool Processor initialization completed
250705 -INFO-MCP access point server information: name=Calculator, version=1.9.4
250705-INFO-MCP Access Point Number of tools supported: 1
250705 -INFO - All MCP access point tools acquired, client ready
250705-INFO-Tool cache flushed
250705 -INFO - List of currently supported functions: [ 'get_time', 'get_lunar', 'play_music', 'get_weather', 'handle_exit_intent', 'calculator']
```
If `'calculator'` is included, the device will be able to recognize and call the calculator tool based on the intent.