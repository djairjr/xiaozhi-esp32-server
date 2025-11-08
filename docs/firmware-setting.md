# Configure a custom server based on the firmware compiled by Xiago

## Step 1 Confirm version
Burn the compiled version of Xiaozhi [firmware version 1.6.1 or above] (https://github.com/78/xiaozhi-esp32/releases)

## Step 2 Prepare your ota address
If you follow the tutorial and use full module deployment, there should be an ota address.

At this moment, please use your browser to open your ota address, for example my ota address
```
https://2662r3426b.vicp.fun/xiaozhi/ota/
```

If "OTA interface is running normally, number of websocket clusters: X" is displayed. Then go down.

If "OTA interface is not running properly" is displayed, it is probably because you have not configured the `Websocket` address in the `Intelligent Console`. Then:

- 1. Use the super administrator to log in to the smart console

- 2. Click `Parameter Management` on the top menu

- 3. Find the `server.websocket` item in the list and enter your `Websocket` address. For example, mine is

```
wss://2662r3426b.vicp.fun/xiaozhi/v1/
```

After configuring, use your browser to refresh your ota interface address to see if it is normal. If it is still not normal, check again whether Websocket starts normally and whether the Websocket address is configured.

## Step 3 Enter network distribution mode
Enter the machine's network configuration mode, click "Advanced Options" at the top of the page, enter the `ota` address of your server, and click Save. Restart device
![Please refer to-OTA address setting](../docs/images/firmware-setting-ota.png)

## Step 4 Wake up Xiaozhi and check the log output

Wake up Xiaozhi and see if the log is output normally.


## FAQ
Here are some frequently asked questions for reference:

[1. Why did Xiaozhi recognize a lot of Korean, Japanese, and English when I spoke](./FAQ.md)

[2. Why does "TTS task error file does not exist" appear? ](./FAQ.md)

[3. TTS often fails and times out](./FAQ.md)

[4. You can connect to the self-built server using Wifi, but cannot connect in 4G mode](./FAQ.md)

[5. How to improve Xiaozhi’s dialogue response speed? ](./FAQ.md)

[6. I speak very slowly, and Xiaozhi always grabs the conversation when I pause](./FAQ.md)

[7. I want to control lights, air conditioners, remote on/off and other operations through Xiaozhi](./FAQ.md)
