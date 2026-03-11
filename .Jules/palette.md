## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).

## 2024-11-20 - Multi-Step Progress Indicators and ARIA Attributes
**Learning:** When building custom multi-step progress indicators using inline styles, standard accessible HTML elements like `<progress>` might be harder to style. When using `<div>` elements to visually represent steps, it is critical to add structural ARIA attributes. Providing `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` on the container, and specifically using `aria-current="step"` on the active child element, ensures screen readers can correctly interpret the current progress within the multi-step flow.
**Action:** When creating or modifying multi-step flows in this codebase, ensure visual progress bars are accompanied by comprehensive ARIA attributes, emphasizing `aria-current="step"` to communicate the current state to assistive technologies.
