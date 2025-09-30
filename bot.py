# من شغل NaDaR، والزين ما يجي صدفة.
# ورى هالترتيب واحد اسمه NaDaR: @@Ky_n0

import telebot
from telebot import types
import requests
import io

NaDaR_BOT_TOKEN = "7632463880:AAGpV9McNIbGDBfvOnK1HZIdLp6zAgKSkro"
NaDaR_API_URL = "https://477h9ikcl5zx.manus.space/API.php"

NaDaR_bot = telebot.TeleBot(NaDaR_BOT_TOKEN)

def NaDaR_start_keyboard():
    NaDaR_markup = types.InlineKeyboardMarkup(row_width=2)
    NaDaR_markup.add(
        types.InlineKeyboardButton("- اضفني لمجموعتك .", url="https://t.me/asaslybot?startgroup=true")
    )
    NaDaR_markup.row(
        types.InlineKeyboardButton("- المطور .", url="https://t.me/@Ky_n0"),
        types.InlineKeyboardButton("- تنصيب بوت مشابه .", url="https://t.me/Ky_n0")
    )
    return NaDaR_markup

@NaDaR_bot.message_handler(commands=['start'])
def NaDaR_start_handler(NaDaR_message):
    NaDaR_bot.send_message(NaDaR_message.chat.id,
                     "- بدون مقدمات، هذا بوت تحميل .\n"
                     "- كتب يوت وخل الباقي عليه .\n"
                     "- مرتب، ميتعبك، ويفيدك .\n"
                     "- يشتغل خاص وكروب، فويزات نظيفة .",
                     reply_markup=NaDaR_start_keyboard())

@NaDaR_bot.message_handler(func=lambda NaDaR_msg: NaDaR_msg.text and NaDaR_msg.text.lower().startswith("يوت "))
def NaDaR_search_youtube(NaDaR_message):
    NaDaR_query = NaDaR_message.text[4:].strip()
    if not NaDaR_query:
        NaDaR_bot.reply_to(NaDaR_message, "- اكتب اسم الأغنية بعد كلمة يوت .")
        return

    NaDaR_bot.send_chat_action(NaDaR_message.chat.id, 'typing')
    NaDaR_bot.send_message(NaDaR_message.chat.id, "جار سحب البيانات من سيرفر NaDaR...")

    try:
        NaDaR_resp = requests.get(f"{NaDaR_API_URL}?prompt=يوت {NaDaR_query}", timeout=20)
        NaDaR_data = NaDaR_resp.json()

        if "search_results" not in NaDaR_data or len(NaDaR_data["search_results"]) == 0:
            NaDaR_bot.reply_to(NaDaR_message, "- ما لقيت نتائج تناسب طلبك، جرب بعد شوي .")
            return

        NaDaR_results = NaDaR_data["search_results"][:1]
        NaDaR_video_id = NaDaR_results[0]['video_id']

        NaDaR_bot.send_chat_action(NaDaR_message.chat.id, 'upload_audio')
        NaDaR_bot.send_message(NaDaR_message.chat.id, "جار تحميل الملف من سيرفر NaDaR...")

        NaDaR_mp3_resp = requests.get(f"{NaDaR_API_URL}?prompt={NaDaR_video_id}", timeout=60)
        NaDaR_mp3_data = NaDaR_mp3_resp.json()

        if NaDaR_mp3_data.get("status") == "success":
            NaDaR_mp3_url = NaDaR_mp3_data["mp3_link"]
            NaDaR_title = NaDaR_mp3_data["title"]
            NaDaR_audio_data = requests.get(NaDaR_mp3_url, timeout=60).content
            NaDaR_audio_file = io.BytesIO(NaDaR_audio_data)
            NaDaR_audio_file.name = f"{NaDaR_title}.mp3"

            NaDaR_thumb_url = NaDaR_mp3_data.get("thumbnail", f"https://img.youtube.com/vi/{NaDaR_video_id}/hqdefault.jpg")
            NaDaR_thumb_data = requests.get(NaDaR_thumb_url, timeout=30).content
            NaDaR_thumb_file = io.BytesIO(NaDaR_thumb_data)
            NaDaR_thumb_file.name = "thumb.jpg"

            NaDaR_user_id = NaDaR_message.from_user.id
            NaDaR_username = NaDaR_message.from_user.first_name
            NaDaR_user_mention = f"[{NaDaR_username}](tg://user?id={NaDaR_user_id})"

            NaDaR_caption = (
                f"- اسم الأغنية: {NaDaR_title}\n\n"
                f"- ورى هالترتيب واحد اسمه NaDaR: @@Ky_n0"
            )

            NaDaR_bot.send_audio(
                chat_id=NaDaR_message.chat.id,
                audio=NaDaR_audio_file,
                caption=NaDaR_caption,
                parse_mode="Markdown",
                thumb=NaDaR_thumb_file,
                reply_to_message_id=NaDaR_message.message_id,
                performer="Enjoy Music",
                title=NaDaR_title
            )
        else:
            NaDaR_bot.reply_to(NaDaR_message, "- ما قدرنا نحمل الملف، جرب مرة ثانية .")

    except Exception as NaDaR_e:
        NaDaR_bot.reply_to(NaDaR_message, f"- صار خطأ أثناء التحميل: {str(NaDaR_e)} .")

NaDaR_bot.polling(none_stop=True)
