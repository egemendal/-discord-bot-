import discord
import os
import google.generativeai as genai
from discord.ext import commands
from flask import Flask
from threading import Thread

# 7/24 aktif tutmak için
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Gemini AI (bedava Türkçe)
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} aktif!")

@bot.command()
async def ai(ctx, *, soru):
    async with ctx.typing():
        try:
            response = model.generate_content(soru)
            await ctx.reply(f"🤖 {response.text[:1900]}")
        except Exception as e:
            await ctx.reply(f"❌ Hata: {e}")

@bot.command()
async def yardim(ctx):
    await ctx.reply("`!ai <soru>` → AI'a soru sor\n`!yardim` → Bu menü")

# Başlat
keep_alive()
bot.run(os.environ['DISCORD_TOKEN'])
      
