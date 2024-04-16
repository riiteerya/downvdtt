import os
import shutil
import re
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')
CHANNEL_URL = os.environ.get('CHANNEL_URL')
BOT_URL = os.environ.get('BOT_URL')
WORKERS = int(os.environ.get('WORKERS'))

def start(update: Update, context: CallbackContext) -> None:
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Channel 🛡', url=CHANNEL_URL),
                InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")
            ]
        ]
    )
    update.message.reply_text(
        "Xin chào, tôi là **TikTok Downloader Bot**.\nTôi có thể tải xuống video TikTok mà không có watermark.\n\n"
        "__**Nhà phát triển :**__ __@JayBeeDev__\n"
        "__**Ngôn ngữ :**__ __Python__\n"
        "__**Framework :**__ __🔥 python-telegram-bot__",
        parse_mode='markdown',
        reply_markup=kb
    )


def help_command(update: Update, context: CallbackContext) -> None:
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Channel 🛡', url=CHANNEL_URL),
                InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")
            ]
        ]
    )
    update.message.reply_text(
        "Xin chào, tôi là **TikTok Downloader Bot**.\nTôi có thể tải xuống bất kỳ video TikTok nào từ một liên kết được chỉ định.\n\n"
        "__Hãy gửi cho tôi một liên kết video TikTok__",
        parse_mode='markdown',
        reply_markup=kb
    )


def tiktok_dl(update: Update, context: CallbackContext) -> None:
    link = re.findall(r'(https?://.*?(?:tiktok|douyin)[^\s]+)', update.message.text)[0]
    link = link.split("?")[0]

    params = {"link": link}
    headers = {
        'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
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
        update.message.reply_video("video.mp4", caption=caption)
    else:
        update.message.reply_text("Xin lỗi, tôi không thể tải xuống video.")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"(http://|https://).*?(tiktok|douyin)"), tiktok_dl))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
