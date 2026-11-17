<div align="center">

# Spotify API

A tiny Flask API that tells your website what you are listening to on Spotify.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![Spotify Web API](https://img.shields.io/badge/Spotify_Web_API-1DB954?style=flat-square&logo=spotify&logoColor=white) ![Heroku](https://img.shields.io/badge/Heroku-430098?style=flat-square&logo=heroku&logoColor=white)

</div>

## About

This service exposes a single public endpoint that returns the song you are playing on Spotify right now. When nothing is playing, it returns a random track from your recently played list and marks you as offline. It is designed to power a "now playing" widget on a personal website, and it sends a CORS header so any frontend can call it.

## Example response

`GET /`

```json
{
  "message": {
    "artistName": "Green Day",
    "songName": "21 Guns",
    "status": "Online"
  }
}
```

| Field | Description |
| --- | --- |
| `artistName` | Main artist of the track |
| `songName` | Track title |
| `status` | `Online` if a track is playing now, `Offline` if the track is from your recently played list |

## How it works

1. A long-lived Spotify **refresh token** is exchanged for a short-lived access token on every request.
2. The service calls Spotify's **currently playing** endpoint.
3. If nothing is playing, it falls back to the **recently played** endpoint and picks a random track.
4. It returns the artist, song and status as JSON.

## Tech Stack

| Area | Technology |
| --- | --- |
| API | Python, Flask |
| Spotify | Web API (authorization code flow with refresh token) |
| Hosting | Gunicorn, Heroku `Procfile` |

## Getting Started

### 1. Create a Spotify app

Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and add `http://localhost/callback/` as a redirect URI.

### 2. Get a refresh token

Open this URL in your browser, replacing `{SPOTIFY_CLIENT_ID}`, and approve access:

```
https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing,user-read-recently-played&redirect_uri=http://localhost/callback/
```

Copy the `code` value from the URL you are redirected to. Then Base64-encode `{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}` and exchange the code for a refresh token:

```bash
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic {BASE64}" \
  -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" \
  https://accounts.spotify.com/api/token
```

### 3. Configure and run

Create `api/.env`. It is listed in `.gitignore`, so it stays out of Git:

```
SPOTIFY_CLIENT_ID=
SPOTIFY_SECRET_ID=
SPOTIFY_REFRESH_TOKEN=
```

```bash
cd api
pip install -r requirements.txt
flask run
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Environment variables

| Variable | Description |
| --- | --- |
| `SPOTIFY_CLIENT_ID` | Client ID of your Spotify app |
| `SPOTIFY_SECRET_ID` | Client secret of your Spotify app |
| `SPOTIFY_REFRESH_TOKEN` | Refresh token from step 2 |

## Project Structure

```
api/
├── app.py            # Flask app and Spotify calls
├── requirements.txt
└── Procfile          # Heroku process definition
```
