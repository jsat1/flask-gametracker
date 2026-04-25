# html_css_notes.txt — HTML & Jinja2 Progression

This file documents the full HTML build progression for the Flask GameTracker, written as each feature was added. Each section is separated by a header and pairs the actual code with inline comments explaining what each piece does and why.

---

## Sections in order

### HTML Skeleton
The bare minimum structure every HTML page starts with — `<!DOCTYPE html>`, `<html>`, `<head>`, and `<body>`. Covers what each tag's role is and what lives inside it.

### Core HTML Tags
A reference list of the most common tags used in this project — `<title>`, `<h1>`–`<h6>`, `<p>`, `<form>`, `<input>`, `<button>` — with a plain English explanation of each.

### First Working Example
The first real page built for GameTracker. Covers a POST form with a text input, how Flask reads form data with `request.form`, and a Jinja2 for loop to display a hardcoded games list.

Key concepts: `method="POST"`, `name` attribute on inputs, `{{ }}` vs `{% %}` in Jinja2

### Updated For Loop
Switches from a hardcoded list to a SQLite-backed `game_list`. Shows how to index into database rows by column position — `game[0]` through `game[4]`.

### Delete Route
Adds a delete button to each game using a hidden input to pass the game's ID silently to the `/delete` route without showing it to the user.

Key concepts: `type="hidden"`, `action=` on forms, passing data invisibly

### Edit Hyperlink
Adds a clickable Edit link next to each game using an `<a>` anchor tag. The link dynamically includes the game's ID in the URL, routing to `/edit/3` for example.

Key concepts: `<a href="">`, dynamic URLs with `{{ game[0] }}`

### edit.html
The separate edit page. Pre-fills all form fields with the game's existing data. Uses Jinja2 conditionals inside `<select>` to keep the previously chosen status selected.

Key concepts: `value="{{ game[1] }}"`, `selected` attribute, Jinja2 inline conditionals

### Search Feature
Adds an IGDB search form using GET instead of POST. Covers why GET is used for searching (fetching data) vs POST for submitting (sending data).

### JavaScript Autofill
Adds a clickable search result that auto-fills the Add Game form. The `onclick` attribute passes the game name and genre to a JavaScript function that targets the input fields by name.

Key concepts: `onclick`, `document.querySelector`, passing arguments from Jinja2 to JavaScript

### Subtitle
Adds a subtitle line under the `<h1>` using a `<p>` tag with a CSS class.

### Game Cards
Replaces bare `<p>` tags with structured `<div>` containers. Introduces `<span>` for inline badge elements, and uses Jinja2 conditionals to apply different badge classes based on game status.

Key concepts: `<div>` vs `<span>`, multiple CSS classes on one element, `&nbsp;` for spacing

### Final index.html
The complete finished template combining all of the above into one clean file with Search, Add Game, and Library sections.
