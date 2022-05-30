import telebot
import datetime
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


pdf_date = []

cursor = db.cursor()
cursor.execute('SELECT pdf_id FROM tbl_pdfs')
data_ad = cursor.fetchall()
for id_pdf in data_ad:
    pdf_date.append(*id_pdf)
    print("pdf ",pdf_date)



SelectedID = max(pdf_date)



def GetPdf(message):
    user_id = message.from_user.id
    db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
    
        
    markupall_pdf = types.InlineKeyboardMarkup(row_width=2)
    markupall_pdf.add(types.InlineKeyboardButton('<Öňki pdf', callback_data ='BackPdf'),types.InlineKeyboardButton('Indiki pdf>', callback_data ='NextPdf'),)
    markup_back_pdf = types.InlineKeyboardMarkup(row_width=2)
    markup_back_pdf.add(types.InlineKeyboardButton('<Öňki pdf', callback_data ='BackPdf'),)
    markup_next_pdf = types.InlineKeyboardMarkup(row_width=2)
    markup_next_pdf.add(types.InlineKeyboardButton('Indiki pdf>', callback_data ='NextPdf'),)
    
    cursor = db.cursor()
    cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result FROM tbl_pdfs WHERE pdf_id = '" + str(SelectedID) + "'")
    step_next_pdf = cursor.fetchone()
    print(step_next_pdf)
    
    if step_next_pdf[0] != 'EXISTS':
        bot.send_message(message.chat.id, "Bu iň soňky!")
        
    else:
        cursor = db.cursor()
        cursor.execute("SELECT pdf_data, pdf_name FROM tbl_pdfs WHERE pdf_id = '" + str(SelectedID) + "'")
        select_pdf = cursor.fetchone()
        pdf = select_pdf[0]
        pdf_name = select_pdf[1]
        
        if SelectedID == max(pdf_date):
            print(SelectedID)
            # bot.send_document(message.chat.id, pdf, reply_markup= markup_back_pdf) 
            bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup=markup_back_pdf , parse_mode = 'HTML')
        elif SelectedID == min(pdf_date):
            print(SelectedID)
            # bot.send_document(message.chat.id, pdf, reply_markup= markup_next_pdf)
            bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup= markup_next, parse_mode = 'HTML')
        else:
            print(SelectedID)
            bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup= markupall_pdf, parse_mode = 'HTML')
            # bot.send_document(message.chat.id, pdf, reply_markup= markupall_pdf)







@bot.callback_query_handler(func =lambda call:True)
def query_handlers(call):
    print("lambda")
    global SelectedID
    
    if call.data == "NextPdf":
        
        if SelectedID == max(pdf_date):
            return bot.send_message(call.message.chat.id, "Bu iň soňky!")
            
        else:
            SelectedID += 1
            print("Next", SelectedID)
            GetPdf(call.message)
            
    elif call.data == "BackPdf":
        
        if SelectedID == 1:
            return bot.send_message(call.message.chat.id, "Bu iň soňky!")
            
        else:
            SelectedID -= 1
            print("Back", SelectedID)
            GetPdf(call.message)
            
            
    else:
        pass