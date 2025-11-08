# get_news_from_newsnow Plug-in news source configuration guide

## Overview

The `get_news_from_newsnow` plugin now supports dynamic configuration of news sources through the web management interface, no longer requiring code modifications. Users can configure different news sources for each agent in the intelligent console.

## Configuration method

### 1. Configure through the web management interface (recommended)

1. Log in to the smart console
2. Enter the "Role Configuration" page
3. Select the agent to configure
4. Click the "Edit Features" button
5. Find the "newsnow news aggregation" plug-in in the parameter configuration area on the right
6. Enter the semicolon-separated Chinese names in the "News Source Configuration" field

### 2. Configuration file method

Configure in `config.yaml`:

```yaml
plugins:
  get_news_from_newsnow:
    url: "https://newsnow.busiyi.world/api/s?id="
news_sources: "The Paper; Baidu Hot Search; Financial Associated Press; Weibo; Douyin"
```

## News source configuration format

News source configuration uses semicolon-separated Chinese names in the format:

```
Chinese name 1; Chinese name 2; Chinese name 3
```

### Configuration example

```
The Paper; Baidu Hot Search; Cai Lianshe; Weibo; Douyin; Zhihu; 36Kr
```

## Supported news sources

The plug-in supports the Chinese names of the following news sources:

- The Paper
- Baidu hot search
- Financial Associated Press
- Weibo
- Tik Tok
- Zhihu
- 36 krypton
- Wall Street Insights
- IT Home
- Today's headlines
- Hupu
- Bilibili
- Kuaishou
- Snowball
- Gelonghui
- Fab Finance
- Golden Ten Data
- Niuke
- Minority
- Rare Earth Nuggets
-ifeng.com
- Bug Tribe
- Lianhe Zaobao
- Coolan
- Vision Forum
- Reference message
- Satellite News Agency
- Baidu Tieba
- Reliable news
- and more...

##Default configuration

If the news source is not configured, the plugin will use the following default configuration:

```
The Paper; Baidu Hot Search; Financial Associated Press
```

## Instructions for use

1. **Configure news source**: Set the Chinese name of the news source in the web interface or configuration file, separated by semicolons
2. **Calling the plug-in**: Users can say "report news" or "get news"
3. **Specify news sources**: Users can say "Report The Paper" or "Get Baidu hot searches"
4. **Get details**: Users can say "Details about this news"

## Working principle

1. The plug-in accepts Chinese names as parameters (such as "The Paper")
2. According to the configured news source list, convert the Chinese name into the corresponding English ID (such as "thepaper")
3. Use English ID to call API to obtain news data
4. Return news content to the user

## Notes

1. The configured Chinese name must be exactly the same as the name defined in CHANNEL_MAP
2. After configuration changes, you need to restart the service or reload the configuration.
3. If the configured news source is invalid, the plug-in will automatically use the default news source
4. Use English semicolons (;) to separate multiple news sources, do not use Chinese semicolons (;)