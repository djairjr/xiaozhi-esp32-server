# esp32 firmware compilation

## Step 1 Prepare your ota address

If you are using version 0.3.12 of this project, whether it is a simple server deployment or a full module deployment, there will be an ota address.

Since the OTA address setting methods for simple server deployment and full module deployment are different, please choose the following specific method:

### If you are using simple Server deployment
At this moment, please use your browser to open your ota address, for example my ota address
```
http://192.168.1.25:8003/xiaozhi/ota/
```
If it displays "OTA interface is running normally, the websocket address sent to the device is: ws://xxx:8000/xiaozhi/v1/

You can use the `test_page.html` that comes with the project to test whether you can connect to the websocket address output by the ota page.

If it cannot be accessed, you need to modify the address of `server.websocket` in the configuration file `.config.yaml`, restart and then test again until `test_page.html` can be accessed normally.

After success, please proceed to step 2.

### If you are using full module deployment
At this moment, please use your browser to open your ota address, for example my ota address
```
http://192.168.1.25:8002/xiaozhi/ota/
```

If "OTA interface is running normally, number of websocket clusters: X" is displayed. Then proceed to the next 2 steps.

If "OTA interface is not running properly" is displayed, it is probably because you have not configured the `Websocket` address in the `Intelligent Console`. Then:

- 1. Use the super administrator to log in to the smart console

- 2. Click `Parameter Management` on the top menu

- 3. Find the `server.websocket` item in the list and enter your `Websocket` address. For example, mine is

```
ws://192.168.1.25:8000/xiaozhi/v1/
```

After configuring, use your browser to refresh your ota interface address to see if it is normal. If it is still not normal, check again whether Websocket starts normally and whether the Websocket address is configured.

## Step 2 Configure environment
First follow this tutorial to configure the project environment ["Building ESP IDF 5.3.2 development environment and compiling Xiaozhi on Windows"] (https://icnynnzcwou8.feishu.cn/wiki/JEYDwTTALi5s2zkGlFGcDiRknXf)

## Step 3 Open the configuration file
After configuring the compilation environment, download the source code of Xiazhi iaozhi-esp32 project.

Download Brother Xia [xiaozhi-esp32 project source code] (https://github.com/78/xiaozhi-esp32) from here.

After downloading, open the `xiaozhi-esp32/main/Kconfig.projbuild` file.

## Step 4 Modify OTA address

Find the content of `default` of `OTA_URL` and put `https://api.tenclass.net/xiaozhi/ota/`
Change it to your own address. For example, my interface address is `http://192.168.1.25:8002/xiaozhi/ota/`, so change the content to this.

Before modification:
```
config OTA_URL
    string "Default OTA URL"
    default "https://api.tenclass.net/xiaozhi/ota/"
    help
        The application will access this URL to check for new firmwares and server address.
```
After modification:
```
config OTA_URL
    string "Default OTA URL"
    default "http://192.168.1.25:8002/xiaozhi/ota/"
    help
        The application will access this URL to check for new firmwares and server address.
```

## Step 4 Set compilation parameters

Set compilation parameters

```
# Enter the root directory of xiaozhi-esp32 from the terminal command line
cd xiaozhi-esp32
# For example, the board I use is esp32s3, so set the compilation target to esp32s3. If your board is another model, please replace it with the corresponding model.
idf.py set-target esp32s3
# Enter menu configuration
idf.py menuconfig
```

After entering the menu configuration, enter `Xiaozhi Assistant` and set `BOARD_TYPE` to the specific model of your board
Save and exit, and return to the terminal command line.

## Step 5 Compile firmware

```
idf.py build
```

## Step 6 Package bin firmware

```
cd scripts
python release.py
```

After the above packaging command is executed, the firmware file `merged-binary.bin` will be generated in the `build` directory in the project root directory.
This `merged-binary.bin` is the firmware file to be burned to the hardware.

Note: If a "zip" related error is reported after executing the second command, please ignore this error and just generate the firmware file `merged-binary.bin` in the `build` directory.
, it won’t have much impact on you, please continue.

## Step 7 Burn firmware
Connect the esp32 device to the computer, use the chrome browser, and open the following URL

```
https://espressif.github.io/esp-launchpad/
```

Open this tutorial, [Flash tool/Web side burning firmware (without IDF development environment)](https://ccnphfhqs21z.feishu.cn/wiki/Zpz4wXBtdimBrLk25WdcXzxcnNS).
Turn to: `Method 2: ESP-Launchpad browser WEB side burning`, start from `3. Burn firmware/download to development board`, and follow the tutorial.

After successful burning and successful networking, wake up Xiaozhi through the wake word and pay attention to the console information output by the server.

## FAQ
Here are some frequently asked questions for reference:

[1. Why did Xiaozhi recognize a lot of Korean, Japanese, and English when I spoke](./FAQ.md)

[2. Why does "TTS task error file does not exist" appear? ](./FAQ.md)

[3. TTS often fails and times out](./FAQ.md)

[4. You can connect to the self-built server using Wifi, but cannot connect in 4G mode](./FAQ.md)

[5. How to improve Xiaozhi’s dialogue response speed? ](./FAQ.md)

[6. I speak very slowly, and Xiaozhi always grabs the conversation when I pause](./FAQ.md)

[7. I want to control lights, air conditioners, remote on/off and other operations through Xiaozhi](./FAQ.md)
