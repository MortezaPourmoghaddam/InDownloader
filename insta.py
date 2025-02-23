import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from pytube import YouTube
import yt_dlp

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("سلام! لینک ویدیوی اینستاگرام یا یوتیوب را ارسال کنید تا دانلود کنم.")

def download_instagram_video(link):
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        
        loader = instaloader.Instaloader()

        shortcode = link.split("/")[-2]
        print(f"در حال دانلود پست با shortcode: {shortcode}")

        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="downloads")
        
        print("محتویات پوشه downloads:")
        for file in os.listdir("downloads"):
            print(f"فایل پیدا شده: {file}")

        video_path = None
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                video_path = os.path.join("downloads", file)
                break

        if video_path:
            print(f"فایل ویدیو پیدا شد: {video_path}")
        else:
            print("فایل ویدیو پیدا نشد")
        return video_path
    except Exception as e:
        print(f"خطا در دانلود: {str(e)}")
        return str(e)


def download_youtube_video(link):
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("محتویات پوشه downloads:")
        for file in os.listdir("downloads"):
            print(f"فایل پیدا شده: {file}")

        return "ویدیو با موفقیت دانلود شد."

    except Exception as e:
        print(f"خطا در دانلود ویدیو یوتیوب: {str(e)}")
        return f"خطا در دانلود ویدیو یوتیوب: {str(e)}"
    
async def handle_video_link(update: Update, context: CallbackContext):
    message = update.message.text
    if "instagram.com" in message:
        await update.message.reply_text("در حال دانلود ویدیو اینستاگرام...")
        try:
            video_path = download_instagram_video(message)
            if video_path and os.path.exists(video_path):
                await update.message.reply_video(video=open(video_path, 'rb'))
#                 os.remove(video_path)
            else:
                await update.message.reply_text("خطا: فایل ویدیو پیدا نشد یا لینک نامعتبر است.")
        except Exception as e:
            await update.message.reply_text(f"خطا در دانلود ویدیو: {e}")
    elif "youtube.com" in message or "youtu.be" in message:
        await update.message.reply_text("در حال دانلود ویدیو یوتیوب...")
        try:
            video_path = download_youtube_video(message)
            if video_path and os.path.exists(video_path):
                await update.message.reply_video(video=open(video_path, 'rb'))
#                 os.remove(video_path)
            else:
                await update.message.reply_text("خطا: فایل ویدیو پیدا نشد یا لینک نامعتبر است.")
        except Exception as e:
            await update.message.reply_text(f"خطا در دانلود ویدیو یوتیوب: {e}")
    else:
        await update.message.reply_text("لطفاً یک لینک معتبر اینستاگرام یا یوتیوب ارسال کنید.")

def main():
    BOT_TOKEN = <YOUR TOKEN API>
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))
    print("ربات در حال اجرا است...")
    app.run_polling()

if __name__ == "__main__":
    main()
