import telebot
import datetime
from telebot import types
import mysql.connector
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import time
import upload_pdf, view_pdfs


token = "5346506402:AAGDGuV_khSGh7PTFe_C-kASBgT5wPKd5g0"
bot = telebot.TeleBot(token)

db = mysql.connector.connect(
            host="hasabym.com",
            user="u1184328_telegrm",
            passwd="telegram_db1",
            port="3306",
            database="u1184328_telegrm")


id_data = []
type_id_data = []
global image_date

pdf_date = []
image_date = []



cursor = db.cursor()
cursor.execute('SELECT img_id FROM tbl_images')
data_ad = cursor.fetchall()
img_data = data_ad[-1]
print(img_data)
for id_image in data_ad:
    image_date.append(*id_image)
    print("img ",image_date)
    
    


cursor = db.cursor()
cursor.execute('SELECT pdf_id FROM tbl_pdfs')
data_pdf = cursor.fetchall()
for id_pdf in data_pdf:
    pdf_date.append(*id_pdf)
    print("pdf", pdf_date)




















button_image = KeyboardButton('/Ýyladyşhananyň_suratlary')
button_balance = KeyboardButton('/Hasabyňyzy_görüň')
button_syn = KeyboardButton('/Agranom_tarapyndan_syn')
button_peyda = KeyboardButton('/Peyda_hasaplary')
button_case_investor = ReplyKeyboardMarkup(resize_keyboard=True).add(button_balance).add(button_image).add(button_syn).add(button_peyda)


pdf_upload = KeyboardButton('/Pdf_ýükle')
upload_image = KeyboardButton('/Surat_ýükle')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_image).add(pdf_upload).add(upload_image)










@bot.message_handler(commands=['start'])
def fn_check_inv_tlgrm_id(message):
    try:
       
        bot.send_message(message.chat.id, "Hoş geldiňiz <b>Tudana Bot</b>", parse_mode = 'HTML')
        user_id = message.from_user.id
        
        if len(str(user_id)) > 0 :
            cursor = db.cursor()
            cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
            result = cursor.fetchone()

            if result[0] != 'EXISTS' and result[1] == 0:
                bot.reply_to(message, "<b>Ulanyjy ID tapylmady!</b>", parse_mode = 'HTML')
                user_not_found = bot.send_message(message.chat.id, "Şahsy kodyňyzy giriň:")
                bot.register_next_step_handler(user_not_found, password_step)
            
            else:
                cursor = db.cursor()
                cursor.execute("SELECT investor_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id) + "'")
                id_f = cursor.fetchone()
                tel_inv_id = id_f[0]
                
                
                id_data.append(tel_inv_id)
                print("User ID",id_data)
                bot.reply_to(message, "Hoş geldiňiz !!!")
                
                
                if result[1] == 2:
                    inv_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_investor)
                else:
                    admin_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_admin)
                
        else:
            bot.reply_to(message, "Ulanyjy ID boş alyndy !!!")
    except SyntaxError:
        bot.reply_to(message, "Başlamakda ýalňyşlyk ýüze çykdy !!!")





########################################################################################################################################################################################

def find_certificate_code(message):
    try:  
        user_id = message.from_user.id
        cert_code = message.text
        print(cert_code)
        cursor = db.cursor()
        cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result FROM tbl_investment WHERE certificate_code = '" + str(cert_code) + "' AND investor_id = '" + str(id_data[0]) + "'")
        q = cursor.fetchone()
        print(q)
        if q[0] != 'EXISTS':
            sert_error = bot.send_message(message.chat.id, "Sertifikat kodyňyz tapylmady !!!")
            bot.register_next_step_handler(sert_error, find_certificate_code)
        else:
            cursor.execute("UPDATE tbl_investors SET investor_telegram_name = '" + str(message.from_user.first_name) + "' ,investor_telegram_id = '" + str(user_id) + "' WHERE investor_id = '" + str(id_data[0]) + "'")
            db.commit()
            bot.reply_to(message, "<i>Hoş geldiňiz !!!</i>", parse_mode = 'HTML')
            if type_id_data[0] == 2:
                inv_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_investor)
            else:
                admin_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_admin)
    except SyntaxError:
        bot.reply_to(message, "Sertifikat kodyňyzy girizmekde ýalňyşlyk ýüze çykdy !!!")


###################################################################################################################################################################################

def password_step(message):
  try:
        user_id = message.from_user.id
        parol = message.text
        print(parol)
        cursor = db.cursor()
        cursor.execute("SELECT investor_id, type_id FROM tbl_investors WHERE investor_password = '" + str(parol) + "'")
        f = cursor.fetchall()
        investor_ids = f[0]
        
        print(investor_ids)
        print(investor_ids[0])
        id_data.append(investor_ids[0])
        type_id_data.append(investor_ids[1])
        print("type id  =>", type_id_data, "inves id =>",id_data)
        
        if investor_ids is None:
            code_error = bot.send_message(message.chat.id, "Bagyşlaň! Şahsy kodyňyz tapylmady. Kodyňyzy gaýtadan giriň:")
            bot.register_next_step_handler(code_error, password_step)
        else:
            
            if type_id_data[0] == 1:
                print("admin")
                admin_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_admin)
                cursor = db.cursor()
                cursor.execute("UPDATE tbl_investors SET investor_telegram_name = '" + str(message.from_user.first_name) + "' ,investor_telegram_id = '" + str(user_id) + "' WHERE investor_id = '" + str(id_data[0]) + "'")
                db.commit()
            else:
                
                code_exit = bot.send_message(message.chat.id, "Gutlaýarys! {0.first_name}. Sertifikat kodynyzy girin:".format(message.from_user))
                bot.register_next_step_handler(code_exit, find_certificate_code)
                
  except IndexError:
        code_not_exit = bot.send_message(message.chat.id, "Bagyşlaň! Şahsy kodyňyz tapylmady. Kodyňyzy gaýtadan giriň:")
        bot.register_next_step_handler(code_not_exit, password_step)
        
########################################################################################################################################################################################





    


###########################################     BALANCE    VIEWED    ###########################################################


@bot.message_handler(commands=['Hasabyňyzy_görüň'])
def balance_step(message):
      
    try:
        user_id = message.from_user.id
        db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
        
        cursor = db.cursor()
        cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
        result = cursor.fetchone()
        
        
        
        if result[0] != 'EXISTS' and result[1] == 1:
            bot.reply_to(message, "<b>Ulanyjy ID tapylmady!</b>", parse_mode = 'HTML')
            user_not_found = bot.send_message(message.chat.id, "Şahsy kodyňyzy giriň:")
            bot.register_next_step_handler(user_not_found, password_step)
         
        else:
            cursor = db.cursor()
            cursor.execute("SELECT sum(investment_amount) as investment_amount FROM tbl_investment WHERE investor_id = '" + str(id_data[0]) + "'")
            summa = cursor.fetchone()
            summa_balance = summa[0]
            
            cursor = db.cursor()
            cursor.execute("SELECT payment_amount FROM tbl_payments WHERE investor_id = '" + str(id_data[0]) + "'")
            payment = cursor.fetchone()
            payments = payment[0]
            print(payments)
            
            cursor = db.cursor()
            cursor.execute("SELECT sum(calculated_income) as calculated_income FROM tbl_income WHERE investor_id = '" + str(id_data[0]) + "'")
            summ_peyda = cursor.fetchone()
            summa_peyda = summ_peyda[0]
            print(summa_peyda)
            
            summa_all = summa_peyda + summa_balance - payments
            
            print(summa_all)
            
            bot.send_message(message.chat.id, "Sizin goýumyňyz:\t <b>{}</b> USD\nJemi hasaplanan peýdaňyz:\t <b>{}</b> USD\nGaýtarylan möçber:\t <b>{}</b> USD\nSiziň hasabyňyz: \t <b>{}</b> USD".format(summa_balance, summa_peyda, payments, summa_all), parse_mode = 'HTML')
            cursor.close()
            db.close()
    except TypeError:
        bot.reply_to(message, "Hasabyňyzy barlamakda ýalňyşlyk ýüze çykdy !!!")




########################################################################################################################################################################



@bot.message_handler(commands=['Surat_ýükle'])
def uploading_image(message):
    user_id = message.from_user.id
    cursor = db.cursor()
    cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
    result = cursor.fetchone()
    
    if result[0] != 'EXISTS' and result[1] == 0:
        bot.reply_to(message, "<b>Ulanyjy ID tapylmady!</b>", parse_mode = 'HTML')
        user_not_found = bot.send_message(message.chat.id, "Şahsy kodyňyzy giriň:")
        bot.register_next_step_handler(user_not_found, password_step)
        
    else:
        if result[1] == 2:
            bot.reply_to(message, "<b>Amal ýerine ýetirilmedi !</b>", parse_mode = 'HTML')
        else:
            
            image_uploading = bot.send_message(message.chat.id, "Suraty ýükläň! {0.first_name} {0.last_name}".format(message.from_user, message.from_user),reply_markup= False)
            bot.register_next_step_handler(image_uploading, upload_photo)


def upload_photo(message):
    try:
        if message.photo:
            print(message.photo[0].file_id)
            image =message.photo[0].file_id
            comment = message.caption
            
            print(comment)
            cursor = db.cursor()
            sql = "INSERT INTO tbl_images(img_data, img_name) VALUES (%s, %s) "
            val = (image, comment)
            cursor.execute(sql, val)
            db.commit()
            
            
            
            cursor = db.cursor()
            cursor.execute("Select img_id from tbl_images")
            image_id = cursor.fetchall()
            
            # for i in image_id:
            image_date.append(*image_id[-1])
            print(image_date)
                
            
            bot.reply_to(message, "Suraty üstünlikli ýüklendi !!!")
            
           
        else:
            pass
            bot.send_message(message.chat.id, "Diňe surat ýükläň!  {0.first_name} {0.last_name}\n Täzeden synanş!".format(message.from_user, message.from_user),reply_markup= False)
    except IndexError:
        bot.reply_to(message, "Ýüklemek prosesi esaslandyrylmady !!!")
        
    
########################################################################################################################################################################



SelectedCardId = len(image_date)
print("SelectedCardId",SelectedCardId)
a = SelectedCardId
b = a-1
@bot.message_handler(commands=['Ýyladyşhananyň_suratlary'])
def search(message):
    
    
    user_id = message.from_user.id
    print(user_id)
    cursor = db.cursor()
   
    cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
    result = cursor.fetchone()
    print(result)
    
    if result[0] != 'EXISTS':
        bot.reply_to(message, "<b>Ulanyjy ID tapylmady!</b>", parse_mode = 'HTML')
        user_not_found = bot.send_message(message.chat.id, "Şahsy kodyňyzy giriň:")
        bot.register_next_step_handler(user_not_found, password_step)
        
    else:
        # bot.register_next_step_handler(message, GetCard(message))
        return GetCard(message)



def GetCard(message):
    global b
    g = image_date[b]
    j = len(image_date)-1
    
    # SelectedCardId = SelectedCardId -1
    # a = image_date[SelectedCardId]
    markupall = types.InlineKeyboardMarkup(row_width=2)
    markupall.add(types.InlineKeyboardButton('<Öňki surat', callback_data ='BackCard'),types.InlineKeyboardButton('Indiki surat>', callback_data ='NextCard'),)
    
    markup_back = types.InlineKeyboardMarkup(row_width=2)
    markup_back.add(types.InlineKeyboardButton('<Öňki surat', callback_data ='BackCard'),)
    
    
    markup_next = types.InlineKeyboardMarkup(row_width=2)
    markup_next.add(types.InlineKeyboardButton('Indiki surat>', callback_data ='NextCard'),)

    user_id = message.from_user.id
    db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
    
        
    
    
    cursor = db.cursor()
    cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result FROM tbl_images WHERE img_id = '" + str(g) + "'")
    step_next_image = cursor.fetchone()
    print(step_next_image)
    
    if step_next_image[0] != 'EXISTS':
        bot.send_message(message.chat.id, "Bu iň soňky!")
        
    else:
        cursor = db.cursor()
        cursor.execute("SELECT img_data, img_name FROM tbl_images WHERE img_id = '" + str(g) + "'")
        select_image = cursor.fetchone()
        image = select_image[0]
        image_name = select_image[1]
        
        if b == j:
            print("!!!!!!",b)
            bot.send_photo(message.chat.id, image,"Teswir: <i><b>{}</b></i>".format(image_name), reply_markup= markup_back, parse_mode = 'HTML') 
            # bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedCardId), reply_markup= , parse_mode = 'HTML')
        elif b == 0:
            print("@@@@",b)
            bot.send_photo(message.chat.id, image,"Teswir: <i><b>{}</b></i>".format(image_name), reply_markup= markup_next, parse_mode = 'HTML')
            # bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedCardId), reply_markup= , parse_mode = 'HTML')
        else:
            print("####",b)
        
            bot.send_photo(message.chat.id, image,"Teswir: <i><b>{}</b></i>".format(image_name), reply_markup= markupall, parse_mode = 'HTML')




@bot.callback_query_handler(func=lambda call:True)
def query_handlers(call):
    global b
    c = len(image_date)-1
    if call.data == "NextCard":
        
        if b == c:
            return bot.send_message(call.message.chat.id, "Bu iň soňky!")
            
        else:
            b += 1
            GetCard(call.message)
            
    elif call.data == "BackCard":
        
        if b == 0:
            return bot.send_message(call.message.chat.id, "Bu iň soňky!")
            
        else:
            b -= 1
            GetCard(call.message)
            
     
    
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
        print("else")
            



########################################################################################################################################################################



@bot.message_handler(commands=['Pdf_ýükle'])
def upload(message):
    user_id = message.from_user.id
    cursor = db.cursor()
   
    cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
    result = cursor.fetchone()
    print(result)
    
    if result[0] != 'EXISTS':
        bot.reply_to(message, "<b>Ulanyjy ID tapylmady!</b>", parse_mode = 'HTML')
        user_not_found = bot.send_message(message.chat.id, "Şahsy kodyňyzy giriň:")
        bot.register_next_step_handler(user_not_found, password_step)
        
    else:
        if result[1] == 2:
            admin_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name} {0.last_name}".format(message.from_user, message.from_user), reply_markup = button_case_investor)
            bot.reply_to(message, "<b>Amal ýerine ýetirilmedi !</b>", parse_mode = 'HTML')
            
        else:
            uploading = bot.send_message(message.chat.id, "Pdf ýükläň! {0.first_name} {0.last_name}".format(message.from_user, message.from_user))
            bot.register_next_step_handler(uploading, upload_pdf.upload_pdf)
    

########################################################################################################################################################################

SelectedID = max(pdf_date)
@bot.message_handler(commands=['Agranom_tarapyndan_syn'])
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
            bot.send_document(message.chat.id, pdf, reply_markup= markup_back_pdf) 
            # bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup=markup_back_pdf , parse_mode = 'HTML')
        elif SelectedID == min(pdf_date):
            print(SelectedID)
            bot.send_document(message.chat.id, pdf, reply_markup= markup_next_pdf)
            # bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup= markup_next_pdf, parse_mode = 'HTML')
        else:
            print(SelectedID)
            # bot.send_message(message.chat.id,"Teswir: <i><b>{}</b></i>".format(SelectedID), reply_markup= markupall_pdf, parse_mode = 'HTML')
            bot.send_document(message.chat.id, pdf, reply_markup= markupall_pdf)






    
########################################################################################################################################################################   
    
@bot.message_handler(commands=['Peyda_hasaplary'])
def look_peyda(message):
    db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
    cursor = db.cursor()
    cursor.execute("SELECT investment_date, investment_end_date  FROM tbl_investment Where investor_id = '" + str(id_data[0]) + "'")
    outputs = cursor.fetchone()
    start_date = outputs[0]
    end_date = outputs[1]
    print(start_date)

    now = datetime.date.today()
    now_time = now.strftime("%y-%m-%d")
    start_to_now_time = now - start_date
    start_to_now_time = start_to_now_time.days / 30
    jemi_goyum_dowri =round(start_to_now_time, 2)  
    
    print("jemi_goyum_dowri =>" ,jemi_goyum_dowri)

    db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
    cursor = db.cursor()
    cursor.execute("SELECT sum(invest_period) FROM tbl_income Where investor_id = '" + str(id_data[0]) + "'")
    outputss = cursor.fetchone()
    hasap_pey_dowri = (outputss[0])
    ulanylmadyk_peyda_dowri = jemi_goyum_dowri - hasap_pey_dowri
    ulanylmadyk_peyda = round(ulanylmadyk_peyda_dowri, 2)
    
    bot.send_message(message.chat.id, f"Jemi goyum dowri:\t{jemi_goyum_dowri}\nHasaplanan peýda döwri:\t{hasap_pey_dowri}\nUlanylmadyk peýda döwri:\t{ulanylmadyk_peyda}\n\nAýlar boýunça")
    db = mysql.connector.connect(
                host="hasabym.com",
                user="u1184328_telegrm",
                passwd="telegram_db1",
                port="3306",
                database="u1184328_telegrm")
    cursor = db.cursor()
    cursor.execute("SELECT invest_period, investment_month, calculated_income FROM tbl_income Where investor_id = '" + str(id_data[0]) + "'")
    output = cursor.fetchall()
    for i in output:
        invest_period = i[0]
        invest_month = i[1]
        invest_income = i[2]
        bot.send_message(message.chat.id, f"Peyda Ayy:\t\t{invest_month}\nPeyda:\t\t{invest_income}\tUSD\n\n")   
    

bot.infinity_polling()  

