# tabbar description

`tabbar` is divided into `4` situations:

- 0 `No tabbar`, only one page entry, no `tabbar` displayed at the bottom; temporary active page of common phrases.
- 1 `Native tabbar`, use `switchTab` to switch tabbar, `tabbar` page is cached.
- Advantages: The native tabbar is rendered first and cached.
- Disadvantage: Only 2 sets of images can be used to switch the selected and unselected states. To modify the color, you can only change the image again (or use iconfont).
- 2 `Customized tabbar` has cache, use `switchTab` to switch tabbar, `tabbar` page has cache. The `tabbar` component of a third-party UI library is used and the display of the native `tabbar` is hidden.
- Advantages: You can configure the `svg icon` you want at will, and it is convenient to switch the font color. There is a cache. All kinds of fancy animations can be achieved.
- Disadvantage: tababr will flicker when clicked for the first time.
- 3 `No cache custom tabbar`, use `navigateTo` to switch `tabbar`, `tabbar` page has no cache. Uses the `tabbar` component of a third-party UI library.
- Advantages: You can configure the svg icon you want at will, and it is easy to switch the font color. All kinds of fancy animations can be achieved.
- Disadvantage: The first click of `tababr` will flicker and there is no cache.


> Note: Fancy effects need to be realized by yourself, this template does not provide them.
