# app.py — Flask GameTracker

This file is the backend of the GameTracker web app. It handles all routing, database operations, and IGDB API communication.

This is a rebuilt version of my earlier [CSV-based GameTracker](https://github.com/jsat1/gametracker) — same concept, but upgraded from flat file storage and a command line interface to a full web app with a database, REST-style routes, and a styled UI.

---

## What changed from the CSV version

| CSV GameTracker | Flask GameTracker |
|---|---|
| CSV file for storage | SQLite database |
| Command line interface | Web UI with Flask |
| No API integration | IGDB API search with OAuth2 |
| Plain text output | Styled game cards with badges |

---

## Routes

### `GET / POST /`— Home
Loads the full game library from the database and renders `index.html`. On POST, reads the submitted form data and inserts a new game into the database.

### `GET /search` — IGDB Search
Takes a search query from the URL, authenticates with the Twitch/IGDB API using OAuth2 client credentials, and returns up to 5 matching games with their genres. Includes a retry loop with exponential backoff for handling timeouts and server errors.

### `POST /delete` — Delete Game
Receives a game ID from a hidden form input and deletes that row from the database. Redirects back to home on completion.

### `GET /edit/<id>` — Edit Page
Fetches a single game row by ID and renders `edit.html` with the existing data pre-filled in the form.

### `POST /update` — Update Game
Receives the updated form data and runs an UPDATE query on the matching database row. Redirects back to home on completion.

---

## Database

Uses SQLite via Python's built-in `sqlite3` module. The database is created automatically on first run by `init_db()`.

Table: `Game_Tracker`

| Column | Type | Notes |
|---|---|---|
| ID | INTEGER | Primary key, auto-incremented |
| Name | TEXT | Game title |
| Genre | TEXT | Genre |
| Status | TEXT | Want / Playing / Played |
| Rating | REAL | Optional, 1–10 |

---

## IGDB API

Authentication uses Twitch OAuth2 client credentials flow — the app authenticates itself with a client ID and secret, no user login required. The access token is fetched fresh on each search request.

Credentials are stored in a `.env` file and loaded with `python-dotenv`. They are never hardcoded.

---

## Setup

1. Clone the repo
2. Create a `.env` file with your Twitch credentials:
```
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
```
3. Install dependencies:
```
pip install flask requests python-dotenv
```
4. Run the app:
```
python app.py
```
5. Open `http://127.0.0.1:5000` in your browser
