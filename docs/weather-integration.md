# Weather plug-in usage guide

## Overview

The weather plug-in `get_weather` is one of the core functions of Xiaozhi ESP32 voice assistant and supports querying weather information across the country through voice. The plug-in is based on the Zephyr Weather API and provides real-time weather and 7-day weather forecast functions.

## API Key Application Guide

### 1. Register a Zefeng Weather account

1. Visit [Qweather Console](https://console.qweather.com/)
2. Register an account and complete email verification
3. Log in to the console

### 2. Create an application to obtain API Key

1. After entering the console, click ["Project Management"](https://console.qweather.com/project?lang=zh) → "Create Project" on the right
2. Fill in the project information:
- **Project name**: such as "Xiaozhi Voice Assistant"
3. Click Save
4. After the project is created, click "Create Credentials" in the project
5. Fill in the credential information:
- **Credential Name**: Such as "Xiao Zhi Voice Assistant"
- **Identity authentication method**: Select "API Key"
6. Click Save
7. Copy `API Key` in the credentials, which is the first key configuration information

### 3. Get API Host

1. Click ["Settings"](https://console.qweather.com/setting?lang=zh) → "API Host" in the console
2. View the exclusive `API Host` address assigned to you. This is the second key configuration information.

The above operation will get two important configuration information: `API Key` and `API Host`

## Configuration method (choose one)

### Method 1. If you use smart console deployment (recommended)

1. Log in to the smart console
2. Enter the "Role Configuration" page
3. Select the agent to configure
4. Click the "Edit Features" button
5. Find the "Weather Query" plug-in in the parameter configuration area on the right
6. Check "Weather Query"
7. Fill in the copied first key configuration `API Key` into the `Weather Plug-in API Key`
8. Fill in the copied second key configuration `API Host` into `Developer API Host`
9. Save the configuration, and then save the agent configuration

### Method 2. If you only deploy a single module xiaozhi-server

Configure in `data/.config.yaml`:

1. Fill in the copied first key configuration `API Key` into `api_key`
2. Fill in the copied second key configuration `API Host` into `api_host`
3. Fill in your city into `default_location`, such as `Guangzhou`

```yaml
plugins:
  get_weather:
api_key: "Your Zephyr Weather API key"
api_host: "Your Zephyr Weather API host address"
default_location: "Your default query city"
```

