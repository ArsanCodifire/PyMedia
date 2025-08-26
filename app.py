import os
import discord
from discord.ext import commands
from discord import app_commands
from yt import YTDLSource
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

cooldowns = commands.CooldownMapping.from_cooldown(
    2, 86400, commands.BucketType.user  # 2 uses per 24h
)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online as PyMedia")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="🎵 PyMedia Music")
    )
    try:
        synced = await bot.tree.sync()
        print(f"🔗 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="play", description="Play music from YouTube")
async def play(interaction: discord.Interaction, search: str):
    bucket = cooldowns.get_bucket(interaction)
    retry = bucket.update_rate_limit()
    if retry:
        await interaction.response.send_message("⏳ You’ve hit your daily play limit (2/day). Try again tomorrow.", ephemeral=True)
        return

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("⚠️ You must be in a voice channel to use this!", ephemeral=True)
        return

    vc = interaction.user.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if not voice:
        voice = await vc.connect()
    elif voice.channel != vc:
        await voice.move_to(vc)

    await interaction.response.send_message(f"🎶 Searching and playing: `{search}`")

    player = await YTDLSource.from_url(search, loop=bot.loop, stream=True)
    voice.play(player, after=lambda e: print(f"Finished playing: {e}" if e else "✅ Done"))
    

@bot.tree.command(name="stop", description="Stop playing and leave the channel")
async def stop(interaction: discord.Interaction):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await interaction.response.send_message("🛑 Stopped and left the channel.")
    else:
        await interaction.response.send_message("⚠️ I’m not in a voice channel.")

keep_alive()
bot.run(os.environ["TOKEN"])
