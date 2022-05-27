<h1 align="center"><img src="https://user-images.githubusercontent.com/82606298/170775456-475ffa71-9cf9-4584-9723-b3917ae0aecc.svg" alt="DebilBot" border="0" height="30px"> DebilBot</h1>


#### Sample russian discord bot, written on discord.py 
#### Creator: GamerDisclaimer

<a href="https://discord.gg/4dEmQjt"><img src="https://img.shields.io/badge/Discord-Join%20TODAY!-7289DA?logo=discord&logoColor=7289DA"></a>
<a href="https://youtube.com/c/gamerdisclaimer"><img src="https://img.shields.io/badge/YouTube-Subscribe%20NOW!-red?logo=youtube&logoColor=red"></a>
<a href="https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot"><img src="https://img.shields.io/badge/DebilBot-Add to Discord server-orange?logo=probot&logoColor=orange"></a>
<br>
<img src="https://img.shields.io/badge/Python-3.10x-yellow">
<img src="https://img.shields.io/badge/Discord.Py-1.7.3-blue">

***

### Requirements

#### Languages
+ **Python 3.10.0**

#### Python modules
+ discord
+ discord_components
+ googletrans==3.1.0a0
+ requests
+ youtube_dl
+ asyncio
+ PyNaCl
+ ffmpeg
+ rich

#### Programs
+ FFmpeg


***

### Usage

***Recomendation: before using, please, read the LICENSE file!***

Open `config.py` file in root directory, and edit prefix value, token value (or make environment variable DEBIL_TOKEN with your token value),
path to ffmpeg, and in dict with emojis set up values with emoji id.

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
avatar *member mention*                 | Sends user avatar
user_info *member mention*              | Shows user information
server_info                             | Shows server information
encode_b64 *text*                       | Coverts text to base64
decode_b64 *base64*                     | Converts Base64 to the text
encode_binary *text*                    | Coverts text to the binary code
decode_binary *binary code*             | Converts binary code to the text
translate *lang in ISO 639-1* *text*    | Translates the text
poll *question* *answer1* *answ2*       | Creates a poll. Minimum 2 answers, max 10. !!!Questions and answers take IN QUOTES
echo *text*                             | Repeats your text
slots                                   | Slot machine
