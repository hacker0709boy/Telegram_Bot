import telebot
from telebot import types
import mysql.connector
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
token = "5346506402:AAGDGuV_khSGh7PTFe_C-kASBgT5wPKd5g0"
bot = telebot.TeleBot(token)

db = mysql.connector.connect(
            host="hasabym.com",
            user="u1184328_telegrm",
            passwd="telegram_db1",
            port="3306",
            database="u1184328_telegrm")


def upload_pdf(message):
    
    print(message.document.file_id)
    pdf =message.document.file_id
    comment = message.caption
    
    print(comment)
    cursor = db.cursor()
    sql = "INSERT INTO tbl_pdfs(pdf_data, pdf_name) VALUES (%s, %s) "
    val = (pdf, comment)
    cursor.execute(sql, val)
    db.commit()
    
    bot.send_message(message.chat.id, "PDF faýl üstünlikli ýüklendi !!!")
    
    