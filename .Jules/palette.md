## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).
## 2026-03-20 - Added visual progress indicator for multi-step form
**Learning:** Implementing visual progress bars in inline-styled React components is particularly effective when relying strictly on state-dependent flex layout techniques ( on wrappers, absolute positioning for connectors) while injecting  properties (, , ) onto the container to provide non-visual feedback.
**Action:** Replicate the structural ARIA patterns combined with compact inline styles when defining sequence-based multi-step components.

## 2025-03-20 - Added visual progress indicator for multi-step form
**Learning:** Implementing visual progress bars in inline-styled React components is particularly effective when relying strictly on state-dependent flex layout techniques (`flex: 1` on wrappers, absolute positioning for connectors) while injecting `aria-` properties (`aria-valuenow`, `aria-valuemin`, `aria-valuemax`) onto the container to provide non-visual feedback.
**Action:** Replicate the structural ARIA patterns combined with compact inline styles when defining sequence-based multi-step components.
