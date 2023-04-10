from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler, CallbackQueryHandler, CommandHandler
from handler import start,tekshir,download,admin
import os

TOKEN = "6004154698:AAEo2pZT8WqoCqRGAXZchoYMtdgozcq3Kbc"

updater = Updater(token=TOKEN)

dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CallbackQueryHandler(tekshir,pattern='tekshirish'))
dp.add_handler(MessageHandler(Filters.text("👤Admin panel"),admin))
dp.add_handler(MessageHandler(Filters.update,download))
updater.start_polling()
updater.idle()