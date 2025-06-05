from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import sqlite3


class Bot:
    def __init__(self, token, gp_admin_id, channel_id, channel_username):
        self.gp_admin_id = gp_admin_id
        self.channel_id = channel_id
        self.channel_username = channel_username
        self.app = ApplicationBuilder().token(token).build()
        self.setup_handler()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            """
سلام کاربر عزیز 🌟
به ربات اختصاصی Configs Center خوش اومدی!

کافیه پست مورد نظرت رو برامون ارسال کنی؛
✅ هر پست بعد از تأیید توسط ادمین، یک ❤️ بهت تعلق می‌گیره!

منتظریم ببینیم چی برامون داری 😉

            """
        )

    async def user_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        usr_post = update.message
        # user = update.effective_user
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        if usr_post.text:
            message_type = "text"
            cursor.execute(
                "INSERT INTO users (CHAT_ID ,  MESSAGE_ID , TEXT_USER , MESSAGE_TYPE ,COUNT_HEART ) VALUES (? , ? , ? , ? , ? )",
                (usr_post.chat_id, usr_post.message_id, usr_post.text, message_type, 0),
            )
            connection.commit()
        elif usr_post.photo:
            message_type = "photo"
            file_id = usr_post.photo[-1].file_id
            caption = usr_post.caption or ""
            cursor.execute(
                "INSERT INTO users (CHAT_ID , MESSAGE_ID, FILE_ID , TEXT_USER , MESSAGE_TYPE , COUNT_HEART) VALUES (? , ? , ? , ? , ? , ?)",
                (
                    usr_post.chat_id,
                    usr_post.message_id,
                    file_id,
                    caption,
                    message_type,
                    0,
                ),
            )
            connection.commit()
        elif usr_post.video:
            file_id = usr_post.video.file_id
            caption = usr_post.caption or ""
            message_type = "video"
            cursor.execute(
                "INSERT INTO users (CHAT_ID , MESSAGE_ID , FILE_ID , TEXT_USER , MESSAGE_TYPE , COUNT_HEART) VALUES (? , ? , ? , ? , ? , ?)",
                (
                    usr_post.chat_id,
                    usr_post.message_id,
                    file_id,
                    caption,
                    message_type,
                    0,
                ),
            )
            connection.commit()
        elif usr_post.audio:
            file_id = usr_post.audio.file_id
            caption = usr_post.caption or ""
            message_type = "audio"
            cursor.execute(
                "INSERT INTO users (CHAT_ID , MESSAGE_ID , FILE_ID , TEXT_USER , MESSAGE_TYPE , COUNT_HEART) VALUES (? , ? , ? , ? , ? , ?)",
                (
                    usr_post.chat_id,
                    usr_post.message_id,
                    file_id,
                    caption,
                    message_type,
                    0,
                ),
            )
            connection.commit()
        else:
            message_type = "unknow"
        connection.close()

        control_button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Accept",
                        callback_data=f"approve_{message_type}_{usr_post.message_id}",
                    ),
                    InlineKeyboardButton(
                        "❌ Reject",
                        callback_data=f"Reject_{message_type}_{usr_post.message_id}",
                    ),
                ]
            ]
        )

        if usr_post.text:
            await context.bot.send_message(
                chat_id=self.gp_admin_id,
                text=f"{usr_post.text}\n\n👈🏻 اتصال به پروکسی\n\n{self.channel_username}",
                reply_markup=control_button,
            )
        elif usr_post.photo:
            photo = usr_post.photo[-1].file_id
            caption = usr_post.caption or ""
            await context.bot.send_photo(
                chat_id=self.gp_admin_id,
                photo=photo,
                caption=f"{caption}\n\n👈🏻 اتصال به پروکسی\n\n{self.channel_username}",
                reply_markup=control_button,
            )
        elif usr_post.video:
            video = usr_post.video.file_id
            caption = usr_post.caption or ""
            await context.bot.send_video(
                chat_id=self.gp_admin_id,
                video=video,
                caption=f"{caption}\n\n👈🏻 اتصال به پروکسی\n\n{self.channel_username}",
                reply_markup=control_button,
            )
        elif usr_post.audio:
            audio = usr_post.audio.file_id
            caption = usr_post.caption or ""
            await context.bot.send_audio(
                chat_id=self.gp_admin_id,
                audio=audio,
                caption=f"{caption}\n\n👈🏻 اتصال به پروکسی\n\n{self.channel_username}",
                reply_markup=control_button,
            )
        await update.message.reply_text("پست شما برای بررسی به ادمین ارسال شد .")

    async def unsupported_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        await update.message.reply_text(
            "از این پیام پشتیبانی نمی شود ، مجاز به ارسال متن ، عکس یا ویدیو می باشید ❣️"
        )

    async def add_proxy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ADMINS_ID = [606195093, 883936046, 7907024687, 7607381994]
        user_id = update.effective_user.id
        if user_id not in ADMINS_ID:
            await update.message.reply_text(
                "کاربر عزیز این بخش مخصوص ادمین ها می باشد ، دسترسی ندارید ..."
            )
            return

        admin_proxy = "".join(context.args).strip()
        if not admin_proxy.startswith("https://t.me/proxy?"):
            await update.message.reply_text(
                "فرمت پروکسی ارسال شده درست نمی باشد ، دوباره امتحان کنید ."
            )
        else:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO proxy (PROXY) VALUES (?)", (admin_proxy,))
            connection.commit()
            connection.close()
            await update.message.reply_text("پروکسی با موفقیت اضافه شد")

    def setup_handler(self):
        self.app.add_handler(
            CommandHandler("start", self.start_command, filters.ChatType.PRIVATE)
        )
        self.app.add_handler(
            CommandHandler("proxy", self.add_proxy, filters.ChatType.PRIVATE)
        )
        self.app.add_handler(
            MessageHandler(
                filters.ChatType.PRIVATE & filters.TEXT
                | filters.PHOTO
                | filters.VIDEO
                | filters.AUDIO,
                self.user_post,
                filters.ChatType.PRIVATE,
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.ChatType.PRIVATE
                & ~(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.AUDIO),
                self.unsupported_message,
            )
        )
        self.app.add_handler(CallbackQueryHandler(self.handler_button))

    async def handler_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        action, message_type, message_id = data.split("_")
        message_id = int(message_id)
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT CHAT_ID , FILE_ID , TEXT_USER , MESSAGE_TYPE , COUNT_HEART FROM users WHERE MESSAGE_ID = ?",
            (message_id,),
        )
        result = cursor.fetchone()
        cursor.execute("SELECT PROXY FROM proxy ORDER BY ID DESC LIMIT 1")
        proxy = cursor.fetchone()

        proxy_text = f'<a href="{proxy[0]}">👈🏻 اتصال به پروکسی </a>'
        chat_id, file_id, text_user, message_type, count_heart = result

        if not result:
            await query.message.reply_text("The Message not found !")

        if action == "approve" and message_type == "text":
            await context.bot.send_message(
                chat_id=self.channel_id,
                text=f"{text_user}\n\n{proxy_text}\n\n{self.channel_username}",
                parse_mode="HTML",
            )
            await context.bot.delete_message(
                chat_id=query.message.chat.id, message_id=query.message.message_id
            )
            count_heart += 1
            cursor.execute(
                "UPDATE users SET COUNT_HEART = ? WHERE CHAT_ID = ?",
                (count_heart, chat_id),
            )
            connection.commit()
            connection.close()
        elif action == "approve" and message_type == "photo":
            await context.bot.send_photo(
                chat_id=self.channel_id,
                photo=file_id,
                caption=f"{text_user}\n\n{proxy_text}\n\n{self.channel_username}",
                parse_mode="HTML",
            )
            await context.bot.delete_message(
                chat_id=query.message.chat.id, message_id=query.message.message_id
            )
            count_heart += 1
            cursor.execute(
                "UPDATE users SET COUNT_HEART = ? WHERE CHAT_ID = ?",
                (count_heart, chat_id),
            )
            connection.commit()
            connection.close()
        elif action == "approve" and message_type == "video":
            await context.bot.send_video(
                chat_id=self.channel_id,
                video=file_id,
                caption=f"{text_user}\n\n{proxy_text}\n\n{self.channel_username}",
                parse_mode="HTML",
            )
            await context.bot.delete_message(
                chat_id=query.message.chat.id, message_id=query.message.message_id
            )
            count_heart += 1
            cursor.execute(
                "UPDATE users SET COUNT_HEART = ? WHERE CHAT_ID = ?",
                (count_heart, chat_id),
            )
            connection.commit()
            connection.close()
        elif action == "approve" and message_type == "audio":
            await context.bot.send_audio(
                chat_id=self.channel_id,
                audio=file_id,
                caption=f"{text_user}\n\n{proxy_text}\n\n{self.channel_username}",
                parse_mode="HTML",
            )
            await context.bot.delete_message(
                chat_id=query.message.chat.id, message_id=query.message.message_id
            )
            count_heart += 1
            cursor.execute(
                "UPDATE users SET COUNT_HEART = ? WHERE CHAT_ID = ?",
                (count_heart, chat_id),
            )
            connection.commit()
            connection.close()
        if action == "Reject":
            await context.bot.delete_message(
                chat_id=query.message.chat.id, message_id=query.message.message_id
            )
            await context.bot.send_message(
                chat_id=chat_id,
                text="متاسفانه به دلایلی پست شما در چنل قرار نگرفت ، می تونی پست های بیشتری ارسال کنی تا بررسی و در صورت تایید در چنل منتشر بشن",
            )
            return
        await context.bot.send_message(
            chat_id=chat_id,
            text="پست شما با موفقیت در چنل قرار گرفت",
        )

    def run_bot(self):
        print("bot starting Mr meti ...  ✅🫡")
        self.app.run_polling()


if __name__ == "__main__":
    with open("token.txt", "r") as file:
        token = file.read()
    bot = Bot(token, "-1002633533356", "-1002582145804", "ID : @Configs_center 💫")
    bot.run_bot()
