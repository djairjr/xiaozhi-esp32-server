## Smart console mobile version (manager-mobile)
Cross-end mobile management terminal based on uni-app v3 + Vue 3 + Vite, supporting App (Android & iOS) and WeChat mini-programs.

### Platform Compatibility

| H5 | iOS | Android | WeChat Mini Program |
| -- | --- | ------- | ---------- | 
| √  | √   | √       | √          | 

Tip: The adaptability of different UI components on different platforms is slightly different, please refer to the corresponding component library documentation.

### Development environment requirements
- Node >= 18
- pnpm >= 7.30 (it is recommended to use `pnpm@10.x` declared in the project)
- Optional: HBuilderX (App debugging/packaging), WeChat developer tools (WeChat applet)

### Quick start
1) Configure environment variables
- Copy `env/.env.example` to `env/.env.development`
- Modify the configuration items according to the actual situation (especially `VITE_SERVER_BASEURL`, `VITE_UNI_APPID`, `VITE_WX_APPID`)

2) Install dependencies

```bash
pnpm i
```

3) Local development (hot update)
- h5: `pnpm dev:h5`, and then observe the ip port number displayed in the startup log
- WeChat applet: `pnpm dev:mp` or `pnpm dev:mp-weixin`, and then use WeChat developer tools to import `dist/dev/mp-weixin`
- App: Use HBuilderX to import `manager-mobile`, and then refer to the tutorial below to run it

### Environment variables and configuration
The project uses a custom `env` directory to store environment files, named according to Vite specifications: `.env.development`, `.env.production`, etc.

Key variables (part):
- VITE_APP_TITLE: application name (write into `manifest.config.ts`)
- VITE_UNI_APPID: uni-app application appid (App)
- VITE_WX_APPID: WeChat applet appid (mp-weixin)
- VITE_FALLBACK_LOCALE: default language, such as `zh-Hans`
- VITE_SERVER_BASEURL: Server base address (HTTP request baseURL)
- VITE_DELETE_CONSOLE: Whether to remove console when building (`true`/`false`)
- VITE_SHOW_SOURCEMAP: whether to generate sourcemap (off by default)
- VITE_LOGIN_URL: Login page path for non-login jump (used by routing interceptor)

Example (`env/.env.development`):
```env
VITE_APP_TITLE=Xiao Zhi
VITE_FALLBACK_LOCALE=zh-Hans
VITE_UNI_APPID=
VITE_WX_APPID=

VITE_SERVER_BASEURL=http://localhost:8080

VITE_DELETE_CONSOLE=false
VITE_SHOW_SOURCEMAP=false
VITE_LOGIN_URL=/pages/login/index
```

illustrate:
- `manifest.config.ts` will read the title, appid, language and other configurations from `env`.

### Important Notes
⚠️ **Configuration items that must be modified before deployment:**

1. **Application ID Configuration**
- `VITE_UNI_APPID`: You need to create an application and obtain the AppID in [DCloud Developer Center](https://dev.dcloud.net.cn/)
- `VITE_WX_APPID`: You need to register the mini program on [WeChat Public Platform](https://mp.weixin.qq.com/) and obtain the AppID

2. **Server address**
- `VITE_SERVER_BASEURL`: change to your actual server address

3. **Application Information**
- `VITE_APP_TITLE`: change to your application name
- Update icon resources such as `src/static/logo.png`

4. **Other configuration**
- Check application configuration information in `manifest.config.ts`
- Modify the tabbar configuration in `src/layouts/fg-tabbar/tabbarList.ts` as needed

### Detailed operation guide

#### 1. Get uni-app AppID
![Generate AppID](../../docs/images/manager-mobile/generate appid.png)
- Copy the generated AppID to the environment variable `VITE_UNI_APPID`

#### 2. Local running steps
![Run locally](../../docs/images/manager-mobile/Run locally.png)

**App local debugging:**
1. Use HBuilderX to import the `manager-mobile` directory
2. Re-identify the project
3. Connect to a mobile phone or use an emulator for real device debugging

**Project identification problem resolution:**
![Re-identify project](../../docs/images/manager-mobile/Re-identify project.png)

If HBuilderX does not recognize the project type correctly:
- Right-click on the project root directory and select "Re-identify project type"
- Make sure the project is recognized as a "uni-app" project

### Routing and Authentication
- The route interception plug-in `routeInterceptor` is registered in `src/main.ts`.
- Blacklist interception: Only verify pages configured to require login (source `getNeedLoginPages` of `@/utils`).
- Login judgment: Based on user information (`useUserStore` of `pinia`), if not logged in, it will jump to `VITE_LOGIN_URL`, with parameters for redirecting back to the original page.

### Network request
- Based on `alova` + `@alova/adapter-uniapp`, create instances in `src/http/request/alova.ts` uniformly.
- `baseURL` reads the environment configuration (`getEnvBaseUrl`) and can dynamically switch domain names through `method.config.meta.domain`.
- Authentication: By default, the `Authorization` header is injected from the local `token` (`uni.getStorageSync('token')`). If it is missing, the login will be redirected.
- Response: Unified processing of `statusCode !== 200` HTTP errors and business `code !== 0` errors; `401` will clear the token and jump to login.

### Build and release

**WeChat Mini Program:**
1. Make sure the correct `VITE_WX_APPID` is configured
2. Run `pnpm build:mp`, the product is in `dist/build/mp-weixin`
3. Use WeChat developer tools to import the project directory and upload the code
4. Submit for review on WeChat public platform

**Android & iOS App：**

#### 3. App packaging and distribution steps

**Step 1: Prepare to pack**
![Packaging and publishing steps 1](../../docs/images/manager-mobile/Packaging and publishing steps 1.png)

1. Make sure the correct `VITE_UNI_APPID` is configured
2. Run `pnpm build:app`, the product is in `dist/build/app`
3. Use HBuilderX to import the project directory
4. Click "Release" → "Native App-Cloud Packaging" in HBuilderX

**Step 2: Configure packaging parameters**
![Packaging and publishing step 2](../../docs/images/manager-mobile/Packaging and publishing step 2.png)

1. **Application icon and startup image**: Upload the application icon and startup page image
2. **Application version number**: Set the version number and version name
3. **Signature Certificate**:
- Android: Upload keystore certificate file
- iOS: Configure developer certificates and profiles
4. **Package name configuration**: Set the application package name (Bundle ID)
5. **Packaging type**: Select test package or official package
6. Click "Package" to start the cloud packaging process

**Publish to App Store:**
- **Android**: Upload the generated APK file to major Android application markets
- **iOS**: Upload the generated IPA file to the App Store via App Store Connect (requires Apple developer account)

### Convention and Engineering
- Pages and subpackaging: generated by `@uni-helper/vite-plugin-uni-pages` and `pages.config.ts`; tabbar is configured in `src/layouts/fg-tabbar/tabbarList.ts`.
- Automatic import of components and hooks: see `unplugin-auto-import` and `@uni-helper/vite-plugin-uni-components` in `vite.config.ts`.
- Style: Use UnoCSS with `src/style/index.scss`.
- State management: `pinia` + `pinia-plugin-persistedstate`.
- Code specifications: built-in `eslint`, `husky`, `lint-staged`, automatic formatting before submission (`lint-staged`).

### Commonly used scripts
```bash
# develop
pnpm dev:mp # Equivalent to dev:mp-weixin

# Build
pnpm build:mp # Equivalent to build:mp-weixin

# other
pnpm type-check
pnpm lint && pnpm lint:fix
```

### License
MIT
