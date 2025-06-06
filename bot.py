import telebot
import yt_dlp
import os

API_TOKEN = '8195833232:AAEa8gFwTcP-npt5n69OQltYMDdXZ71srew'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    if url.startswith("http"):
        bot.reply_to(message, f"📥 تم استلام الرابط:\n{url}\nجارِ التحميل (قريباً 🍆)")
        try:
            output_path = "downloaded_video.%(ext)s"

            ydl_opts = {
                'outtmpl': output_path,
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'merge_output_format': 'mp4'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info)

            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🎉 تفضل الفيديو!")

            os.remove(video_file)

        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحميل:\n{e}")
    else:
        bot.reply_to(message, "🔗 أرسل رابط فيديو صالح يبدأ بـ http")

bot.polling()
