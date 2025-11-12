import discord
from discord import app_commands
from datetime import datetime, timedelta, timezone
import os

# --- CONFIG ---
CITIES = {
    "wellington": {"flag": "🇳🇿", "offset": 10, "link": "https://ipogo.app/?coords=-41.282965,174.766473"},
    "sydney": {"flag": "🇦🇺", "offset": 9, "link": "https://ipogo.app/?coords=-33.86498,151.21075"},
    "melbourne": {"flag": "🇦🇺", "offset": 9, "link": "https://ipogo.app/?coords=-37.8176,144.958812"},
    # ... add all other cities exactly like before
}

# --- DISCORD BOT ---
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}")

@tree.command(name="time", description="Show local time in a specific city.")
@app_commands.describe(city="Name of the city (e.g. Tokyo, Sydney, London)")
async def time_command(interaction: discord.Interaction, city: str):
    city_key = city.lower().strip()
    if city_key not in CITIES:
        await interaction.response.send_message(
            f"❌ City not found! Try one of: {', '.join(CITIES.keys())}", ephemeral=True
        )
        return

    data = CITIES[city_key]
    offset = data["offset"]
    now_fi = datetime.now(timezone.utc) + timedelta(hours=2)  # Finland = UTC+2
    local_time = now_fi + timedelta(hours=offset)
    time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")

    embed = discord.Embed(
        title=f"{data['flag']} {city.title()}",
        description=f"🕒 **{time_str}**\nUTC offset (from Finland): `{offset:+} h`",
        color=0x00BFFF
    )
    embed.add_field(name="📍 Map", value=f"[Open in iPogo]({data['link']})", inline=False)

    await interaction.response.send_message(embed=embed)

# --- RUN ---
import os
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
