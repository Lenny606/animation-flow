## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).
## 2025-04-11 - Add Progress Indicator
**Learning:** For multi-step React workflows using inline styles, aria-current="step" applied conditionally dynamically conveys current location while mapping an array to render visual indicators ensures consistency without CSS classes.
**Action:** Always add `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` on the container, and `aria-current="step"` on the active child item for accessible multi-step components.

## 2025-05-15 - Modal Keyboard Accessibility
**Learning:** When implementing custom modals in React, the browser's native dialog keyboard accessibility features are lost. This includes the ability to close the modal using the Escape key and automatically shifting focus to the modal when opened.
**Action:** Always manually provide these accessibility features: add a `keydown` event listener for the `Escape` key to close the modal, and use a `ref` with a brief `setTimeout` to automatically shift initial focus to the close button when the modal opens. Ensure to separate the auto-focus logic into its own `useEffect` hook distinct from other event listeners.
## 2026-04-23 - Form Required Field Accessibility
**Learning:** Required fields should use ARIA indicators like `aria-hidden="true"` on visual asterisks (`*`) alongside standard `required` attributes to ensure screen readers do not redundantly read 'asterisk'. Error messages must have a `role="alert"` and be explicitly linked to inputs via `aria-invalid` and `aria-describedby` to correctly associate errors with input contexts in screen readers.
**Action:** When implementing forms with validation, always manually link error `div` elements to input fields and use `aria-hidden` for decorative visual indicators of required fields.
