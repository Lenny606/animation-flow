## 2024-05-24 - Inline Styles and Accessibility Traps
**Learning:** This codebase relies heavily on inline style objects (e.g., `const styles = { input: { outline: 'none' } }`). These often hide accessibility anti-patterns like removing focus indicators (`outline: none`) which are harder to spot than in CSS files where you might search for `:focus`.
**Action:** When auditing components in this repo, always check the `const styles` object at the bottom of the file specifically for `outline: 'none'` or missing focus states on interactive elements.

## 2024-06-25 - Disabled States with Inline Styles
**Learning:** Because this app relies on React inline style objects instead of CSS classes, standard CSS pseudo-classes like `:disabled` do not work to visually update elements when they are disabled. Adding `disabled={true}` to an element will functionally disable it, but without a visual change, users may not realize it's disabled.
**Action:** Always implement a conditional style object merge (e.g., `style={{ ...styles.button, ...(isDisabled ? styles.buttonDisabled : {}) }}`) alongside the `disabled` attribute to ensure proper visual feedback (reduced opacity, changed background, `cursor: 'not-allowed'`).

## 2024-04-01 - Missing ARIA structures in Multi-Step UI Components
**Learning:** In complex, multi-step generation flows (like the 5-step video generation in GenerateImage), visual step text alone ('Step 1: Description') provides no context to screen readers about the total length of the process or the current state of progression, leading to confusion.
**Action:** Always wrap multi-step progress indicators in a parent container with `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`, and mark the currently active step child with `aria-current="step"`.
