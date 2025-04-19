import discord
import asyncio
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv  # ← NEW

load_dotenv()
TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True  # Needed for sending messages

bot = commands.Bot(command_prefix="!", intents=intents)
sol_upper_target = 135.33
sol_lower_target = 132.6

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    while True:
        # Replace this logic with real data checks later
        alert_message = await check_solana_alerts()
        if alert_message:
            await channel.send(alert_message)
        await asyncio.sleep(60)  # Run every 1 minute

@bot.command()
async def setpth(ctx, value: float):
    global sol_upper_target
    sol_upper_target = value
    await ctx.send(f"✅ Upper price alert threshold set to ${sol_upper_target:.2f}")


@bot.command()
async def setptl(ctx, value: float):
    global sol_lower_target
    sol_lower_target = value
    await ctx.send(f"✅ Lower price alert threshold set to ${sol_lower_target:.2f}")

async def check_solana_alerts():
    global sol_upper_target, sol_lower_target

    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        data = response.json()
        sol_price = data["solana"]["usd"]
        print(f"Current SOL Price: ${sol_price}")  # Debug log

        if sol_price < sol_lower_target:
            return f"⚠️ SOL dropped **below ${sol_lower_target:.2f}**. Current price: ${sol_price:.2f}"
        elif sol_price > sol_upper_target:
            return f"🚀 SOL crossed **above ${sol_upper_target:.2f}**. Current price: ${sol_price:.2f}"
        else:
            return None

    except Exception as e:
        print("Error fetching price:", e)
        return None
    
@bot.command()
async def pos(ctx):
    global sol_lower_target, sol_upper_target

    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        data = response.json()
        sol_price = data["solana"]["usd"]

        msg = (
            f"📍 **SOL Price Position Check**\n"
            f"➤ Current Price: `${sol_price:.2f}`\n"
            f"🟥 Lower Target: `${sol_lower_target:.2f}`\n"
            f"🟩 Upper Target: `${sol_upper_target:.2f}`"
        )

        await ctx.send(msg)

    except Exception as e:
        await ctx.send("❌ Could not fetch SOL price.")
        print("Error in !pos command:", e)

bot.run(TOKEN)