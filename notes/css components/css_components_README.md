# css_components — CSS Build Progression

This folder breaks the final `gamecards.css` into individual stages showing the order it was built in. Each file is a snapshot of what was added at that step, with inline comments explaining each property.

The final combined stylesheet lives at `static/gamecards.css`.

---

## Build Order

### `01_base.css`
The starting point. Sets the page background, text color, max width, centering, and font. Also styles the `h1` heading color and letter spacing.

Key properties: `background-color`, `color`, `max-width`, `margin: 0 auto`, `padding`, `font-family`, `text-align`, `letter-spacing`

---

### `02_sections.css`
Adds the three section containers — Search, Add Game, and Library — and styles them together using a grouped selector. Also styles the `h2` heading inside each section with an uppercase label style and a bottom border divider.

Key properties: grouped selectors, `border-radius`, `border`, `text-transform: uppercase`, `border-bottom`, `padding-bottom`

---

### `03_inputs_buttons.css`
Styles all input boxes, select dropdowns, and buttons globally. Adds a focus glow state for inputs and a hover darkening state for buttons. Introduces the secondary button style used on the Edit button — transparent background with a colored border.

Key properties: `outline: none`, `input:focus`, `box-shadow`, `cursor: pointer`, `font-weight`, `background: transparent`, pseudo-classes (`:hover`, `:focus`), `rgba()` for semi-transparent colors

---

### `04_gamecards.css`
Builds the game card layout using flexbox. Each card arranges its two children — `.game-info` and `.card-actions` — horizontally with space between them. `.game-info` uses `flex: 1` to stretch and fill all remaining space. `.card-actions` becomes its own separate flex container to line up the Edit and Delete buttons horizontally.

Key properties: `display: flex`, `align-items: center`, `justify-content: space-between`, `flex: 1`, `border-left`, `gap`

---

### `05_badges.css`
Adds the status badge styles — Playing, Played, and Want. The shared `.badge` class handles shape and text sizing. Each status gets its own color class applied alongside it. Uses `display: inline-block` so badges sit on the same line as the game title.

Key properties: `display: inline-block`, `border-radius: 20px`, `rgba()` for transparent backgrounds, multiple classes on one element (`badge badge-playing`)

---

## How it connects to the HTML

Each CSS stage has a matching HTML section in `../html_css_notes.txt` where the containers being styled were first created.
