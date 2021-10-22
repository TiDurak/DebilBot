<h1 align="center"><img src="https://tidurak.github.io/DebilBot2.svg" alt="DebilBot" border="0" height="28px"> DebilBot</h1>


#### Sample russian discord bot, written on discord.py 
#### Creator: GamerDisclaimer

<a href="https://discord.gg/4dEmQjt"><img src="https://img.shields.io/badge/Discord-Join%20TODAY!-7289DA?logo=discord&logoColor=7289DA"></a>
<a href="https://youtube.com/c/gamerdisclaimer"><img src="https://img.shields.io/badge/YouTube-Subscribe%20NOW!-red?logo=youtube&logoColor=red"></a>
<a href="https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot"><img src="https://img.shields.io/badge/DebilBot.exe-Add to Discord server-orange?logo=probot&logoColor=orange"></a>
<br>
<img src="https://img.shields.io/badge/Python-3.9x-yellow">
<img src="https://img.shields.io/badge/Discord.Py-1.7.3-blue">
<img src="https://img.shields.io/badge/Requests-2.26.0-blue">
<img src="https://img.shields.io/badge/Googletrans-3.1.0a0-blue">
<img src="https://img.shields.io/badge/YouTube__DL-2021.6.6-blue">
<img src="https://img.shields.io/badge/discord__components-2.0.4-blue">
<img src="https://img.shields.io/badge/PyNaCl-1.4.0-blue">
<img src="https://img.shields.io/badge/Colorama-0.4.4-blue">


***

### Requirements

#### Languages
+ **Python 3.9.0**

#### Python modules
+ Discord.py
+ requests
+ youtube_dl
+ asyncio
+ PyNaCl
+ colorama
+ discord_components
+ googletrans==3.1.0a0

#### Programs
+ FFmpeg


***

### Usage

***Recomendation: before using, please, read the LICENSE file!***

Open `config.py` file in root directory, and edit prefix value:
```
settings = {
    'token': os.environ['DEBIL_TOKEN'],
    'prefix': 'd.',
    'path_to_ffmpeg': r'C:\Program Files\ffmpeg\bin\ffmpeg.exe', # Path to ffmpeg. For Linux users just type "ffmpeg"
}
```

Then create environment variable "DEBIL_TOKEN" with your token value

To launch music commands, as **play**:
Windows: [download ffmpeg build](https://www.gyan.dev/ffmpeg/builds/), unpack archive, `path_to_ffmpeg` value must be your path to ffmpeg.
Linux: just install ffmpeg (`sudo apt install ffmpeg`, `sudo apt-get install ffmpeg`, etc), in `path_to_ffmpeg` value type `ffmpeg`

**For bot starting, open `main.py` file**

---

### Commands List

Command                                 | Description
----------------------------------------|---------------------------------------------------------------------------------
help                                    | Show command list
help *command name*                     | Show details about command
play *song name*                        | Starts playing the song (U need to be connected in the Voice Chat)
pause                                   | Pausing the song
resume                                  | Resume song playing
stop                                    | Stopping the song
leave                                   | Disconnects the bot from voice chat
clear *number of messages*              | Delete messages from text chat
fetch *ID of the message*               | Delete one message from chat by ID
kick *member mention*                   | Kicks member from server
ban *member mention*                    | Bans member on server
encode_b64 *text*                       | Coverts text to base64
decode_b64 *base64*                     | Converts Base64 to the text
encode_binary *text*                    | Coverts text to the binary code
decode_binary *binary code*             | Converts binary code to the text
translate *lang in ISO 639-1* *text*    | Translates the text
poll *question* *answer1* *answ2*       | Creates a poll. Minimum 2 answers, max 10. !!!Questions and answers take IN QUOTES
echo *text*                             | Repeats your text
slots                                   | Slot machine
