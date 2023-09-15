import os
import re
import time
import asyncio
import traceback
import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from config import OWNER

@Client.on_message(filters.command(["بحث"], ""))
async def ytsearch(client, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("بحث اكتب شيئ للبحث ☢️")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("جاري البحث انتظر قليلاً ♻️")
        results = YoutubeSearch(query, max_results=6).to_dict()
        i = 0
        text = ""
        while i < 6:
            text += f"عنوان - {results[i]['title']}\n"
            text += f"المدة - {results[i]['duration']}\n"
            text += f"المشاهدات - {results[i]['views']}\n"
            text += f"القناة - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(e)

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


@Client.on_message(filters.command(["/song", "/video", "نزل", "تنزيل", "حمل", "تحميل"], ""))
async def downloaded(client: Client, message):
 if len(message.command) == 1:
  if message.chat.type == enums.ChatType.PRIVATE :
   ask = await client.ask(message.chat.id, "ارسل اسم الان ")
   query = ask.text
   m = await ask.reply_text("**جاري البحث انتظر قليلاً 🔎**")
  else:
   try:
    ask = await client.ask(message.chat.id, "ارسل الاسم الان.", filters=filters.user(message.from_user.id), reply_to_message_id=message.id, timeout=8)
   except:
      pass
   query = ask.text
   m = await ask.reply_text("**جاري البحث انتظر قليلاً ⚡**")
 else:
  query = message.text.split(None, 1)[1]
  m = await message.reply_text("**جاري البحث انتظر قليلاً .🔎**")
  if message.command[0] in ["/song", "نزل", "تنزيل"]:
    ydl_ops = {
        'format': 'bestaudio[ext=m4a]',
        'keepvideo': True,
        'prefer_ffmpeg': False,
        'geo_bypass': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("فشل العثور علي النتيجه المطلوبة ❌")
        return
    try:
     await m.edit("جاري التحميل انتظر قليلاً⚡")
    except:
      pass
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"• uploader @{OWNER[0]} "
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        try:
         await m.edit("جاري التحميل انتظر قليلاً ⚡")
        except:
            pass
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=host,
            thumb=thumb_name,
            title=title,
            duration=dur,
        )
        await m.delete()

    except Exception as e:
        await m.edit(" ERROR, wait for bot owner to fix")
    try:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        pass
  else:
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        pass
    try:
        try:
          await m.edit("جاري التحميل انتظر قليلاً ⚡")
        except:
           pass
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        pass
    preview = wget.download(thumbnail)
    try:
      await m.edit("جاري التحميل انتظر قليلاً ⚡")
    except:
      pass
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        remove_if_exists(file_name)
        remove_if_exists(preview)
        await msg.delete()
    except Exception as e:
        pass
