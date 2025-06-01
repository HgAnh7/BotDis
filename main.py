import os
import discord
from bot.random import *
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã đăng nhập thành công trên Discord!')
    try:
        # Đồng bộ các lệnh slash (application commands) với Discord
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} lệnh slash!")
    except Exception as e:
        print(f"Lỗi khi đồng bộ lệnh slash: {e}")
# Random
register_nude(bot)
register_girl(bot)
register_butt(bot)
register_anime(bot)
register_pussy(bot)
register_cosplay(bot)
register_imganime(bot)
register_girlsexy(bot)
register_breastsqueeze(bot)

if __name__ == '__main__':
    print("Bot Discord đang hoạt động...")
    bot.run(TOKEN)
