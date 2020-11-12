from pydub import AudioSegment
import time
import os
import discord
from discord.ext import commands
from discord.utils import get
import os
from discord import FFmpegPCMAudio
import ffmpeg
from mutagen.mp3 import MP3
import asyncio
import random

filename = "pizzatime.mp3"
sound = AudioSegment.from_file(filename)
speed = 1
looptimes = 0
bot = commands.Bot(command_prefix="!z ")

@bot.command(name="pizzatime")
@commands.has_permissions(administrator=True)
async def pizzatime(ctx):
    global speed
    global looptimes
    global filename
    def speed_change(sound, speed=1.0):
        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        global looptimes
        global filename
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
             "frame_rate": int(sound.frame_rate * speed)
          })
         # convert the sound with altered frame rate to a standard frame rate
         # so that regular playback programs will work right. They often only
         # know how to play audio at standard frame rate (like 44.1k)
        filename = "pizzatime"+str(looptimes)+".mp3"
        file_handle = sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate).export(filename, format="mp3")
    restart=False
    voice_channel = await discord.VoiceChannel.connect(ctx.author.voice.channel)
    def restart():
        voice_channel.stop()

    while speed < 10:
        looptimes += 1
        speed += 0.1
        fast_sound = speed_change(sound, speed)
        audio_source = discord.FFmpegPCMAudio(filename)
        voice_channel.play(audio_source, after=restart())
        while voice_channel.is_playing():
            await asyncio.sleep(0.001)
        channel = bot.get_channel(775803299156721674)
        await channel.send("changed speed to "+str(speed*100)+"%")
        os.remove(filename)
    await voice_channel.disconnect(force=True)
    speed = 0
    looptimes = 0
    await channel.send("good job! you lived through the holy terror")

bot.run(os.getenv('TOKEN'))
   
