import os
import tempfile
import subprocess
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import *

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Send your files")

@app.on_message(filters.video | filters.document)
def handle_media(client, message):
    # If document, check if mimetype is video/mp4
    if message.document:
        if message.document.mime_type != "video/mp4":
            message.reply_text("Please send a valid MP4 video file.")
            return
        file_id = message.document.file_id
    else:
        file_id = message.video.file_id

    file = client.download_media(file_id)
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_filename = temp_file.name

    subprocess.run(
        f'ffmpeg -y -i "{file}" -c:v libx264 -preset superfast -crf 30 -pix_fmt yuv420p -movflags +faststart "{temp_filename}"',
        shell=True,
        check=True
    )
    
    message.reply_video(temp_filename)
    os.remove(file)
    os.remove(temp_filename)

app.run()
