<h1 align="center"><img src="https://user-images.githubusercontent.com/82606298/170775456-475ffa71-9cf9-4584-9723-b3917ae0aecc.svg" alt="DebilBot" border="0" height="30px"> DebilBot</h1>


#### Simple Russian Discord Bot, Written in Discord.py
#### Creator: gdisclaimer aka. tidurak, gamerdisclaimer

<a href="https://discord.gg/4dEmQjt"><img src="https://img.shields.io/badge/Discord-Join%20today!-7289DA?logo=discord&logoColor=7289DA"></a>
<a href="https://youtube.com/c/gamerdisclaimer"><img src="https://img.shields.io/badge/YouTube-Subscribe-red?logo=youtube&logoColor=red"></a>
<a href="https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot"><img src="https://img.shields.io/badge/DebilBot-Add to Discord server-orange?logo=probot&logoColor=orange"></a>
<br>
<img src="https://img.shields.io/badge/Python-3.10+-yellow">
<img src="https://img.shields.io/badge/Discord.Py-2.2.2+-blue">

***

## Usage

1. Install all Python dependencies (`pip install -r requirements.txt`) and ffmpeg.
2. If you are a Linux user, you should install the *Times New Roman* font.
3. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), set up [`GOOGLE_API_KEY`](https://aistudio.google.com/app/apikey), and follow [these instructions](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev) for using the `/ai` command.
4. Get your bot token from the [Discord Developer Portal](https://discord.com/developers/applications). 
5. Set the `DEBIL_TOKEN` environment variable, **OR** put it in `settings.token` in `config.py`.
6. Run the `main.py` file.

## To launch music commands:

### Windows 
[Download the ffmpeg build](https://www.gyan.dev/ffmpeg/builds/), unpack the archive, and set `path_to_ffmpeg` to your path to ffmpeg.

### Linux
Just install ffmpeg (`sudo apt install ffmpeg`, `sudo pacman -S ffmpeg`, etc.), and for the `path_to_ffmpeg` value, type `ffmpeg`.

## If the quote slash/context command works incorrectly, and you are a Linux user:
### For Ubuntu/Debian/Mint users

Add the following non-free repos to your `/etc/apt/sources.list`, then run:
```
sudo apt update
sudo apt install ttf-mscorefonts-installer
```

