```
{
  "artistName":"Green Day",
  "songName":"21 Guns",
  "status":"Online"
}
```

<hr>

<h4>Your Spotify App</h4>
<img width="469" alt="image" src="https://user-images.githubusercontent.com/62550592/179568130-33ad5129-3007-4262-99ad-4ab58414816b.png">

Create a string combining `{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}` (e.g. `5n7o4v5a3t7o5r2e3m1:5a8n7d3r4e2w5n8o2v3a7c5`) and **encode** into [Base64](https://base64.io/).

Then run a [curl command](https://httpie.org/run) in the form of:
```sh
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {BASE64}" -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" https://accounts.spotify.com/api/token
```

Save the Refresh token

<hr>

<h4>Deployment</h4>

<img width="403" alt="image" src="https://user-images.githubusercontent.com/62550592/179567410-59736038-a973-44f7-8003-60e90367ca37.png">
<img width="603" alt="image" src="https://user-images.githubusercontent.com/62550592/179569143-5b2e6aac-a00b-4d02-aecd-dc0e22235601.png">
