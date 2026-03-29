## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).

## 2024-10-27 - Playwright Verification with Malformed URLs
**Learning:** If `VITE_API_URL` is unset in the frontend environment, API calls default to a malformed `https:///` URL, causing immediate fetch failures. Playwright's `page.route()` fails to intercept these malformed URLs because the browser's `fetch` API rejects them before hitting the network layer.
**Action:** To bypass this when testing locally with Playwright, use `page.add_init_script` to override `window.fetch` directly and return mocked `Response` objects instead of relying on `page.route()`.
