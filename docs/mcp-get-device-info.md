#How does the MCP method obtain device information?

This tutorial will guide you on how to obtain device information using the MCP method.

Step 1: Customize your `agent-base-prompt.txt` file

Copy the contents of the `agent-base-prompt.txt` file in the xiaozhi-server directory to your `data` directory, and rename it to `.agent-base-prompt.txt`.

Step 2: Modify the `data/.agent-base-prompt.txt` file, find the `<context>` tag, and add the following code content in the tag content:
```
- **Device ID:** {{device_id}}
```

After the addition is completed, the content of the `<context>` tag in your `data/.agent-base-prompt.txt` file is roughly as follows:
```
<context>
【important! The following information has been provided in real time. There is no need to call the tool to query, please use it directly:】
- **Device ID:** {{device_id}}
- **Current time:** {{current_time}}
- **Today's date:** {{today_date}} ({{today_weekday}})
- **Today’s lunar calendar:** {{lunar_date}}
- **User's city:** {{local_address}}
- **Local weather for the next 7 days:** {{weather_info}}
</context>
```

Step 3: Modify the `data/.config.yaml` file and find the `agent-base-prompt` configuration. The content before modification is as follows:
```
prompt_template: agent-base-prompt.txt
```
Modify to
```
prompt_template: data/.agent-base-prompt.txt
```

Step 4: Restart your xiaozhi-server service.

Step 5: Add a parameter named `device_id`, type `string`, and described as `device ID` in your mcp method.

Step 6: Reawaken Xiaozhi and let him call the mcp method to see if your mcp method can obtain the `device ID`.
