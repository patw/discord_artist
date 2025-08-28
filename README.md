# Discord Artist

A simple discord bot that can prompt Flux dev running on Gemini's flash-image model

![Sample output](output.jpg)

## Local Installation

Windows:

```
pip install -r requirements.txt
```

Linux:

```
pip3 install -r requirements.txt
```

## Running discord bot

* Copy sample.env to .env
* Fill in your Bot Token (https://discord.com/developers/applications)
* Fill in your google gemini token (https://ai.google.dev/gemini-api/docs/api-key)
* Run the following:

Windows:

```
python discord_artist.py
```

Linux/MacOS

```
python3 discord_artist.py
```