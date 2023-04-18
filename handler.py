from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler, CallbackQueryHandler, CommandHandler
from request import media
from pprint import pprint
import requests
from db import DB
db = DB('db.json')

def start(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    user_name = update.message.chat.username
    
    try :
        admin = db.get_admin(chat_id)
        if admin == 'creator':
            text = f"""🔥 Xush kelibsiz {update.message.chat.first_name}, Bot orqali yuklab olishingiz mumkin:\n\n• Instagram - stories, post va IGTV;\n• YouTube - video/audio istalgan formatda;\n• TikTok - suv belgisiz video;\n• Likee - suv belgisiz video;\n\n🚀 Media yuklashni boshlash uchun uning havolasini yuboring.\n😎 Bot guruhlarda ham ishlay oladi!"""
            admin=KeyboardButton('🔐 Admin')
            btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)       
            bot.sendMessage(chat_id,text,reply_markup=btn)
        elif admin == 'member':
            text = "⛔️ *Botdan to'liq foydalanish uchun* quyidagi kanallarga obuna bo'ling"
            chanel_1 = db.get_channel()[0]
            chanel_2 = db.get_channel()[1]
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
                [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
                ],
            )
            bot.sendMessage(chat_id,text,reply_markup=keyboard,parse_mode="MarkdownV2")

    except KeyError:
        
        text = "⛔️ *Botdan to'liq foydalanish uchun* quyidagi kanallarga obuna bo'ling"
        db.starting(chat_id=chat_id,user_name=user_name)
        db.save()
        chanel_1 = db.get_channel()[0]
        chanel_2 = db.get_channel()[1]
        keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
                [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
                ],
            )
        bot.sendMessage(chat_id,text,reply_markup=keyboard,parse_mode="MarkdownV2")
    

def tekshir(update:Update, context:CallbackContext):
    bot = context.bot
    query = update.callback_query
    chat_id = query.message.chat.id

    message_id = query.message.message_id
    user_id = query.from_user.id
    chanel_1 = db.get_channel()[0]
    chanel_2 = db.get_channel()[1]
    chanel1 = bot.getChatMember(f"@{chanel_1[13:]}",chat_id)['status']
    chanel2 = bot.getChatMember(f"@{chanel_2[13:]}",chat_id)['status']
    print(chanel1)
    print(chanel2)
    if chanel1!='left' and chanel2!='left':
        text = f"""🔥 Xush kelibsiz {query.message.chat.first_name}, Bot orqali yuklab olishingiz mumkin:\n\n• Instagram - stories, post va IGTV;\n• YouTube - video/audio istalgan formatda;\n• TikTok - suv belgisiz video;\n• Likee - suv belgisiz video;\n\n🚀 Media yuklashni boshlash uchun uning havolasini yuboring.\n😎 Bot guruhlarda ham ishlay oladi!"""
        bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id)

    else:
        text = "Kanallarga a'zo bo'lmadingiz"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
            [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
            ]
        )
        bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id,reply_markup=keyboard,parse_mode="MarkdownV2")
        


def download(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    if update.message.text:
        message = update.message.text
        print(message[12:21])
        if message[12:21] == 'instagram':
            post = media(message)
            print(post)
            data = {
                'text':post.get('title','@JR_InstagramBot bilan yuklab olindi.'),
                'media':post.get('media'),
                'type':post.get('Type')
            }

            if data['type']=='Post-Video':
                text = data['text'] + '\n\n@JR_InstagramBot bilan yuklab olindi.'
                bot.send_video(chat_id=chat_id,video=data['media'],caption=text)
                
            elif data['type']=='Post-Image':
                text = data['text'] + '\n\n@JR_InstagramBot bilan yuklab olindi.'
                bot.send_photo(chat_id=chat_id,photo=data['media'],caption=text)

            elif data['type'] == 'Carousel':
                text = data['text'] + '\n\n@JR_InstagramBot bilan yuklab olindi.'
                for id in data['media']:
                    if 'video' in id:
                        bot.send_video(chat_id=chat_id,video=id)
                    else:
                        bot.send_photo(chat_id=chat_id,photo=id)
                bot.send_message(chat_id,text=text)
        else:
            admin = db.get_admin(chat_id)
            if admin != 'creator':
                bot.send_message(chat_id,'⛔️ Linkda xatolik bor\nTekshirib qayta yuboring')

    if db.get_admin(chat_id) == 'creator':

        if update.message.video:
            text = update.message.caption_markdown_v2
            video = update.message.video.file_id
            bot.send_video(chat_id,video, caption = text,parse_mode='MarkdownV2')
            media = {'video':video,'text':text}
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('🚫 Bekor qilish',callback_data=f'rek_False'),InlineKeyboardButton('✅ Yuborish',callback_data=f'rek_True')]])
            bot.send_message(chat_id,'❇️ Xabarni tekshiring va yuborishni tasdiqlang…',reply_markup=keyboard)
        elif update.message.photo:
            text = update.message.caption_markdown_v2
            photo = update.message.photo[0]['file_id']
            bot.send_photo(chat_id,photo, caption = text,parse_mode='MarkdownV2')
            media = {'photo':photo,'text':text}
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('🚫 Bekor qilish',callback_data=f'rek_False'),InlineKeyboardButton('✅ Yuborish',callback_data=f'rek_True')]])
            bot.send_message(chat_id,'❇️ Xabarni tekshiring va yuborishni tasdiqlang…',reply_markup=keyboard)
        
        else:
            bot.send_message(chat_id,'❌ Xabar turi qo‘llab-quvvatlanmaydi.')


def admin(update:Update,context:CallbackContext):
    bot=context.bot
    chad_id = update.message.chat.id
    admin = db.get_admin(chad_id)
    if admin == 'creator':
        chanel_1 = db.get_channel()[0]
        chanel_2 = db.get_channel()[1]
        
        text=f"🔧 Siz Administrator menyusidasiz.\n\n◾️ BOTGA ULANGAN KANALLAR\n☞ @{chanel_1[13:]}\n☞ @{chanel_2[13:]}"
        rek = KeyboardButton('🔖 Reklama')
        static=KeyboardButton('📊 Statistika')
        chanel=KeyboardButton('🧫 Kanallarni almashtirish')
        admin = KeyboardButton('🛂 Adminlarni boshqarish')
        back = KeyboardButton('🔚 Admindan Chiqish')
        btn=ReplyKeyboardMarkup([[rek,static],[chanel,admin],[back]],resize_keyboard=True)
        bot.sendMessage(chad_id,text,reply_markup=btn)

def back_admin(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    text = '🔝 Asosiy Menyu'
    admin=KeyboardButton('🔐 Admin')
    btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)       
    bot.sendMessage(chat_id,text,reply_markup=btn)

def reklama(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    admin = db.get_admin(chat_id=chat_id)
    if admin == 'creator':
        text = '*Reklamangizni yuboring*'
        back = KeyboardButton('🔚 Chiqish')
        btn=ReplyKeyboardMarkup([[back]],resize_keyboard=True) 
        bot.sendMessage(chat_id,text,reply_markup = btn,parse_mode='MarkdownV2')


def rek_query(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query
    data,bool = query.data.split('_')
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    print(bool)
    if bool == 'True':
        bot.edit_message_text(chat_id=chat_id,message_id=message_id,text='⏳')
        users = db.get_users()
        user_number = len(users)-1 # adminlar sonini ayiramiz
        s = 1
        for user,data in users.items():
            if data['status'] != 'creator':
                bot.send_message(chat_id=user,text = 'xabar')
                
                bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=f'✅ Yuborildi {s}/{user_number}')
                s += 1
            else:
                continue

        
    else:
        bot.delete_message(chat_id=chat_id,message_id=message_id)

def statistic(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    admin = db.get_admin(chat_id=chat_id)
    users = db.get_users()
    total = len(users)
    admin_len = db.creator()
    member = db.member()

    if admin == 'creator':
        text = f"""📊 BOT STATISTIKASI\n#statistics\n\n@JR_InstagramBot\n▪️Yaratilgan: 18.03.2023\n\n▪️Foydalanuvchilar: {total}\n▫️Faol: {member}\n▪️Adminlar: {admin_len}"""
        back = KeyboardButton('🔚 Chiqish')
        btn=ReplyKeyboardMarkup([[back]],resize_keyboard=True) 
        bot.sendMessage(chat_id,text,reply_markup = btn)