## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).

## 2024-10-30 - Multi-Step Flow Progress Indicators
**Learning:** Multi-step flows in this application are often implemented via a single `step` state variable but lack visual cues indicating progression or total steps. Relying only on text changes makes the experience less grounded for the user, and screen readers aren't natively aware of the total number of steps.
**Action:** When working on multi-step forms, implement an accessible visual progress bar. Ensure the container has `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`, and the active step indicator has `aria-current="step"`. Use existing color codes (`#3b82f6` for active, `#10b981` for completed).
