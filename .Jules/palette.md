## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).
## 2025-04-11 - Add Progress Indicator
**Learning:** For multi-step React workflows using inline styles, aria-current="step" applied conditionally dynamically conveys current location while mapping an array to render visual indicators ensures consistency without CSS classes.
**Action:** Always add `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` on the container, and `aria-current="step"` on the active child item for accessible multi-step components.

## 2024-05-24 - Custom Modal Accessibility
**Learning:** Custom modals in this app require manual implementation of native dialog accessibility features, like Escape key listeners and focus management.
**Action:** When implementing custom modals, always include an Escape key listener and an auto-focus effect to ensure keyboard accessibility.
