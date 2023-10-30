from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler, CallbackQueryHandler, CommandHandler
from handler import start,tekshir,download,admin,back_admin,reklama,rek_query,statistic
import os

TOKEN = "6787477123:AAHMi_hfGusB1EUQaAe7m-kYoBgLose9PZc"

updater = Updater(token=TOKEN)

dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CallbackQueryHandler(tekshir,pattern='tekshirish'))
dp.add_handler(MessageHandler(Filters.text("🔐 Admin") | Filters.text("🔚 Chiqish"),admin))
dp.add_handler(MessageHandler(Filters.text("🔚 Admindan Chiqish"),back_admin))
dp.add_handler(MessageHandler(Filters.text("📊 Statistika"),statistic))
dp.add_handler(MessageHandler(Filters.text("🔖 Reklama"),reklama))
dp.add_handler(CallbackQueryHandler(rek_query,pattern='rek'))
dp.add_handler(MessageHandler(Filters.update,download))
updater.start_polling()
updater.idle()