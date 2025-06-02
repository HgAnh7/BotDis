import random
import discord
from pathlib import Path
from discord.ext import commands

# Cấu hình
ALLOWED_CHANNELS = [1375707188252901376, 1375707367051886654]
ERROR_CHANNEL_ID = 1377693583741812867

# Định nghĩa lệnh với đường dẫn file tùy chỉnh và giới hạn kênh
COMMANDS = {
    "nude": {
        "title": "Ảnh Nude Ngẫu Nhiên", 
        "desc": "Gửi ảnh nude ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/nude",
        "restricted": True  # Giới hạn kênh
    },
    "butt": {
        "title": "Ảnh Butt Ngẫu Nhiên", 
        "desc": "Gửi ảnh butt ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/butt",
        "restricted": True  # Giới hạn kênh
    },
    "pussy": {
        "title": "Ảnh Pussy Ngẫu Nhiên", 
        "desc": "Gửi ảnh pussy ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/pussy",
        "restricted": True  # Giới hạn kênh
    },
    "cosplay": {
        "title": "Ảnh Cosplay Ngẫu Nhiên (only: 🔞┊nsfw)",
        "desc": "Gửi ảnh cosplay ngẫu nhiên",
        "path": "bot/url/cosplay",
        "restricted": True  # Không giới hạn kênh
    },
    "anime": {
        "title": "Ảnh Anime Ngẫu Nhiên", 
        "desc": "Gửi ảnh anime ngẫu nhiên",
        "path": "bot/url/anime",
        "restricted": False  # Không giới hạn kênh
    },
    "blowjob": {
        "title": "Ảnh Blow Job Ngẫu Nhiên", 
        "desc": "Gửi ảnh blow job ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/nsfw/blowjob",
        "restricted": True  # Giới hạn kênh
    },
    "girlsexy": {
        "title": "Ảnh Gái Sexy Ngẫu Nhiên", 
        "desc": "Gửi ảnh gái sexy ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/girlsexy",
        "restricted": True  # Giới hạn kênh
    },
    "breastsqueeze": {
        "title": "Breastsqueeze Ngẫu Nhiên", 
        "desc": "Gửi ảnh breastsqueeze ngẫu nhiên (only: 🔞┊nsfw)",
        "path": "bot/url/breastsqueeze",
        "restricted": True  # Giới hạn kênh
    }
}

# Tải tất cả ảnh với xử lý lỗi
def load_all_images():
    collections = {}
    for cmd, config in COMMANDS.items():
        try:
            file_path = Path(config["path"])
            collections[cmd] = [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()] if file_path.exists() else []
        except Exception as e:
            print(f"[Tải Ảnh] Lỗi khi đọc file {cmd}: {e}")
            collections[cmd] = []
    return collections

IMAGE_COLLECTIONS = load_all_images()

async def send_random_image(interaction: discord.Interaction, bot: commands.Bot, cmd: str):
    # Kiểm tra giới hạn kênh nếu lệnh có restricted = True
    if COMMANDS[cmd].get("restricted", False) and interaction.channel_id not in ALLOWED_CHANNELS:
        return await interaction.response.send_message(
            "❌ Lệnh này chỉ có thể sử dụng trong các kênh được chỉ định!", ephemeral=True)
    
    if not (images := IMAGE_COLLECTIONS[cmd]):
        if error_channel := bot.get_channel(ERROR_CHANNEL_ID):
            await error_channel.send(f"❌ [{cmd.title()}] Danh sách ảnh chưa được tải hoặc trống.")
        return await interaction.response.send_message("❌ Lỗi: Danh sách ảnh không tồn tại.", ephemeral=True)
    
    try:
        embed = discord.Embed(title=COMMANDS[cmd]["title"])
        embed.set_image(url=random.choice(images))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        if error_channel := bot.get_channel(ERROR_CHANNEL_ID):
            await error_channel.send(f"❌ [{cmd.title()}] Lỗi: {e}")
        await interaction.response.send_message("❌ Đã có lỗi xảy ra. Vui lòng thử lại sau.", ephemeral=True)

def register_all_commands(bot: commands.Bot):
    """Đăng ký tất cả lệnh tự động"""
    for cmd, config in COMMANDS.items():
        # Sửa lỗi closure với lambda và tham số mặc định
        def create_command(cmd_name=cmd):
            async def image_command(interaction: discord.Interaction):
                await send_random_image(interaction, bot, cmd_name)
            return image_command
        
        bot.tree.command(name=cmd, description=config["desc"])(create_command())

# Các hàm tiện lợi - chỉ cần gọi 1 lần register_all_commands()
register_nude = register_butt = register_pussy = register_cosplay = register_anime = register_girlsexy = register_breastsqueeze = register_all_commands