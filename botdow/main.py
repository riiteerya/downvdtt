from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import shutil
import requests
import re
import os
import time
from dotenv import load_dotenv

load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
api = os.environ.get('API_KEY')
hash = os.environ.get('API_HASH')
chnnl = os.environ.get('CHANNEL_URL')
BOT_URL = os.environ.get('BOT_URL')
workers = int(os.environ.get('WORKERS'))

app = Client("JayBee", bot_token=bot_token, api_id=api, api_hash=hash, workers=workers)


@app.on_message(filters.command('start'))
def start(client, message):
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Channel 🛡', url=chnnl),
                InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")
            ]
        ]
    )
    message.reply_text(
        "Xin chào, tôi là **TikTok Downloader Bot**.\nTôi có thể tải xuống video TikTok mà không có watermark.\n\n"
        "__**Nhà phát triển :**__ __@JayBeeDev__\n"
        "__**Ngôn ngữ :**__ __Python__\n"
        "__**Framework :**__ __🔥 Pyrogram__",
        parse_mode='markdown',
        reply_markup=kb
    )


@app.on_message(filters.command('help'))
def help(client, message):
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Channel 🛡', url=chnnl),
                InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")
            ]
        ]
    )
    message.reply_text(
        "Xin chào, tôi là **TikTok Downloader Bot**.\nTôi có thể tải xuống bất kỳ video TikTok nào từ một liên kết được chỉ định.\n\n"
        "__Hãy gửi cho tôi một liên kết video TikTok__",
        parse_mode='markdown',
        reply_markup=kb
    )


@app.on_message(filters.regex(r"(http://|https://).*?(tiktok|douyin)"))
def tiktok_dl(client, message):
    link = re.findall(r'(https?://.*?(?:tiktok|douyin)[^\s]+)', message.text)[0]
    link = link.split("?")[0]

    params = {"link": link}
    headers = {
        'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
        'x-rapidapi-key': os.environ.get('API_KEY')
    }
    api = "https://tiktok-info.p.rapidapi.com/dl/"
    response = requests.get(api, params=params, headers=headers)
    data = response.json()

    if 'videoLinks' in data and 'download' in data['videoLinks']:
        video_url = data['videoLinks']['download']

        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open("video.mp4", "wb") as f:
                shutil.copyfileobj(r.raw, f)

        caption = f"**Video URL:** {link}"
        message.reply_video("video.mp4", caption=caption)
    else:
        message.reply_text("Xin lỗi, tôi không thể tải xuống video.")


app.run()
