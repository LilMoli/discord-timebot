import discord
from discord import app_commands
from datetime import datetime, timedelta, timezone

# --- CONFIG ---

# Define all cities, offsets (in hours), flags, and map links
CITIES = {
    "wellington": {"flag": "🇳🇿", "offset": 10, "link": "https://ipogo.app/?coords=-41.282965,174.766473"},
    "sydney": {"flag": "🇦🇺", "offset": 9, "link": "https://ipogo.app/?coords=-33.86498,151.21075"},
    "melbourne": {"flag": "🇦🇺", "offset": 9, "link": "https://ipogo.app/?coords=-37.8176,144.958812"},
    "adelaide": {"flag": "🇦🇺", "offset": 7.5, "link": "https://ipogo.app/?coords=-34.926748,138.600359"},
    "brisbane": {"flag": "🇦🇺", "offset": 8, "link": "https://ipogo.app/?coords=-27.470188,153.023664"},
    "tokyo": {"flag": "🇯🇵", "offset": 7, "link": "https://ipogo.app/?coords=35.6963,139.81440"},
    "kyoto": {"flag": "🇯🇵", "offset": 7, "link": "https://ipogo.app/?coords=35.00472,135.77119"},
    "osaka": {"flag": "🇯🇵", "offset": 7, "link": "https://ipogo.app/?coords=34.698088,135.50018"},
    "seoul": {"flag": "🇰🇷", "offset": 7, "link": "https://ipogo.app/?coords=37.56716,126.97787"},
    "hong kong": {"flag": "🇭🇰", "offset": 6, "link": "https://ipogo.app/?coords=22.301199,114.170167"},
    "singapore": {"flag": "🇸🇬", "offset": 6, "link": "https://ipogo.app/?coords=1.289856,103.845107"},
    "tainan": {"flag": "🇹🇼", "offset": 6, "link": "https://ipogo.app/?coords=25.039823,121.507339"},
    "bandung": {"flag": "🇮🇩", "offset": 5, "link": "https://ipogo.app/?coords=-8.7467172,115.166787"},
    "manila": {"flag": "🇵🇭", "offset": 6, "link": "https://ipogo.app/?coords=14.594369,120.974617"},
    "ho chi minh city": {"flag": "🇻🇳", "offset": 5, "link": "https://ipogo.app/?coords=10.773657,106.692288"},
    "dhaka": {"flag": "🇧🇩", "offset": 4, "link": "https://ipogo.app/?coords=23.724403,90.397809"},
    "pune": {"flag": "🇮🇳", "offset": 3.5, "link": "https://ipogo.app/?coords=18.5187,73.8531"},
    "maldives": {"flag": "🇲🇻", "offset": 3, "link": "https://ipogo.app/?coords=4.171946,73.50371"},
    "dubai": {"flag": "🇦🇪", "offset": 2, "link": "https://ipogo.app/?coords=25.072251,55.129011"},
    "izmir": {"flag": "🇹🇷", "offset": 1, "link": "https://ipogo.app/?coords=38.462970,27.217870"},
    "thessaloniki": {"flag": "🇬🇷", "offset": 0, "link": "https://ipogo.app/?coords=40.625426,22.953643"},
    "zaragoza": {"flag": "🇪🇸", "offset": -1, "link": "https://ipogo.app/?coords=41.661254,-0.892912"},
    "budapest": {"flag": "🇭🇺", "offset": 0, "link": "https://ipogo.app/?coords=47.531057,19.051142"},
    "paris": {"flag": "🇫🇷", "offset": -1, "link": "https://ipogo.app/?coords=48.864954,2.323832"},
    "rome": {"flag": "🇮🇹", "offset": -1, "link": "https://ipogo.app/?coords=41.892925,12.48174"},
    "santa cruz": {"flag": "🇪🇸", "offset": -2, "link": "https://ipogo.app/?coords=28.490291,-16.319225"},
    "london": {"flag": "🇬🇧", "offset": -2, "link": "https://ipogo.app/?coords=51.510077,-0.123853"},
    "são paulo": {"flag": "🇧🇷", "offset": -5, "link": "https://ipogo.app/?coords=-23.586354,-46.6583"},
    "são luís": {"flag": "🇧🇷", "offset": -5, "link": "https://ipogo.app/?coords=-2.557929,-44.307009"},
    "indaial": {"flag": "🇧🇷", "offset": -5, "link": "https://ipogo.app/?coords=-26.892904,-49.230269"},
    "central park": {"flag": "🇺🇸", "offset": -7, "link": "https://ipogo.app/?coords=40.770418,-73.974637"},
    "disneyworld": {"flag": "🇺🇸", "offset": -7, "link": "https://ipogo.app/?coords=28.415972,-81.580934"},
    "chicago": {"flag": "🇺🇸", "offset": -8, "link": "https://ipogo.app/?coords=41.880006,-87.623931"},
    "austin": {"flag": "🇺🇸", "offset": -8, "link": "https://ipogo.app/?coords=30.288607,-97.738525"},
    "mexico city": {"flag": "🇲🇽", "offset": -8, "link": "https://ipogo.app/?coords=19.433956,-99.139351"},
    "pier 39": {"flag": "🇺🇸", "offset": -10, "link": "https://ipogo.app/?coords=37.808673,-122.409821"},
    "san francisco": {"flag": "🇺🇸", "offset": -10, "link": "https://ipogo.app/?coords=37.785047,-122.40171"},
    "california disneyland": {"flag": "🇺🇸", "offset": -10, "link": "https://ipogo.app/?coords=33.811954,-117.919067"},
    "las vegas": {"flag": "🇺🇸", "offset": -10, "link": "https://ipogo.app/?coords=36.112068,-115.171898"},
    "honolulu": {"flag": "🇺🇸", "offset": -12, "link": "https://ipogo.app/?coords=21.298364,-157.860113"},
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
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
