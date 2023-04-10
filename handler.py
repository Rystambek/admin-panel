from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler, CallbackQueryHandler, CommandHandler
from request import media
import requests
from db import DB
db = DB('db.json')

def start(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    user_name = update.message.chat.username
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
    user_name = query.message.chat.username
    message_id = query.message.message_id
    user_id = query.from_user.id
    chanel_1 = db.get_channel()[0]
    chanel_2 = db.get_channel()[1]
    chanel1 = bot.getChatMember(f"@{chanel_1[13:]}",chat_id)['status']
    chanel2 = bot.getChatMember(f"@{chanel_2[13:]}",chat_id)['status']
    print(chanel1)
    print(chanel2)
    if chanel1!='left' and chanel2!='left':
        text = f"""🔥 Xush kelibsiz {query.message.chat.first_name}, Bot orqali yuklab olishingiz mumkin:

• Instagram - stories, post va IGTV;
• YouTube - video/audio istalgan formatda;
• TikTok - suv belgisiz video;
• Likee - suv belgisiz video;

🚀 Media yuklashni boshlash uchun uning havolasini yuboring.
😎 Bot guruhlarda ham ishlay oladi!"""
        bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id)
        admins = db.get_admins()
        if user_name in admins:
            text = 'Admin panel'
            admin=KeyboardButton('👤Admin panel')
            btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)       
            bot.sendMessage(user_id,text,reply_markup=btn)

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
            bot.send_video(chat_id=chat_id,video=data['media'],caption=data['text'])
            
        elif data['type']=='Post-Image':
            bot.send_photo(chat_id=chat_id,photo=data['media'],caption=data['text'])

        elif data['type'] == 'Carousel':
            for id in data['media']:
                if 'video' in id:
                    bot.send_video(chat_id=chat_id,video=id)
                else:
                    bot.send_photo(chat_id=chat_id,photo=id)
            bot.send_message(chat_id,text=data['text'])



def admin(update:Update,context:CallbackContext):
    bot=context.bot
    chad_id = update.message.chat.id
    chanel_1 = db.get_channel()[0]
    chanel_2 = db.get_channel()[1]
    
    text=f"Siz Administrator menyusidasiz.\n\nBOTGA ULANGAN KANALLAR\n@{chanel_1[13:]}\n@{chanel_2[13:]}"
    rek = KeyboardButton('Reklama')
    static=KeyboardButton('Statistika')
    chanel=KeyboardButton('Kanalni almashtirish')
    admin = KeyboardButton('Adminlarni boshqarish')
    back = KeyboardButton('Admindan chiqish')
    btn=ReplyKeyboardMarkup([[rek,static],[chanel,admin],[back]],resize_keyboard=True)
    bot.sendMessage(chad_id,text,reply_markup=btn)