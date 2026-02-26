## 2026-02-26 - Inline Styles and Accessibility Associations
**Learning:** The app relies heavily on inline styles, which led to missing `htmlFor`/`id` associations on form labels and inputs. Also, reused style objects made it difficult to apply consistent disabled states (like `:disabled` pseudo-class) without inline conditional logic.
**Action:** When encountering inline styles in forms, prioritize adding explicit `htmlFor` and `id` attributes. For button states, consider moving to CSS classes or utility functions to handle state-dependent styles consistently.
