#-*- coding: utf-8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)                
import logging
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

ENCRYPT, DECRYPT = range(2)

tabula_recta=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'0','1','2','3','4','5','6','7','8','9',' ','!','+','=','?','@','(',')','*','$','-','№','.',',']

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    try:
        update.message.reply_text(
            'Greetings, dear {}!\n'
            'Given Telegram bot will\n'
            'help you to encrypt\n'
            'and decrypt your messages\n'
            'via symmetric-key algorithm.\n'
            'Developed by Dmitry Moldovanov.\n'
            '\nYou can use /help to view a list of commands'
            .format(update.message.from_user.first_name))
    except Exception:
        update.message.reply_text('Sorry, something went wrong.')

def help(bot, update):  
    try:
        update.message.reply_text(
            'There is a list of commands that I provide :'
            '\n/encrypt - start of encryption process'
            '\n/decrypt - start of decryption process'
            '\n/cancel - canceling encryption or decryption processes'
            '\n/list - will be displayed a list of symbols that is supported by this bot')
    except Exception:
        update.message.reply_text('Sorry, something went wrong.')

def encrypt_command(bot, update):
    try:
        update.message.reply_text(
            'I am listerning you right now.'
            '\nSo please, enter your TEXT'
            '\nand secret KEY down below with'
            '\nnext pattern : t#YOUR TEXT k#YOUR KEY')    
    except Exception:
        update.message.reply_text('Sorry, something went wrong.')
    return ENCRYPT

def encryption(bot, update, user_data):
    try:    
        result = re.split(r'[#]', update.message.text)     
        temp = result[1]
        text = temp.replace(" k","")
        key = result[2]      
        listKeys = get_key_list(key)    
        encrypted_text = encrypt(text, listKeys)
        update.message.reply_text('There is your encrypted text : {}'.
        format(encrypted_text))
    except Exception:
         update.message.reply_text('Sorry, something went wrong at encryption process.\n')
    return ConversationHandler.END

def encrypt(text, listKeys):
    for key in listKeys:
        final = ""
        key *= len(text)//len(key)+1
        for index, symbol in enumerate(text):
            temp=(tabula_recta.index(symbol)+tabula_recta.index(key[index]))%len(tabula_recta)
            final+=tabula_recta[temp] 
        text = final   
    return final

def decrypt_command(bot, update):
    try:
        update.message.reply_text(
            'I am listerning you right now.'
            '\nSo please, enter your encrypted TEXT'
            '\nand secret KEY down below with'
            '\nnext pattern : t#YOUR ENCRYPTED TEXT k#YOUR KEY') 
    except Exception:
        update.message.reply_text('Sorry, something went wrong.')
    return DECRYPT

def decryption(bot, update, user_data):
    try:
        result = re.split(r'[#]', update.message.text)
        temp = result[1]
        text = temp.replace(" k","")
        key = result[2]      
        listKeys = get_key_list(key)  
        decrypted_text = decrypt(text, listKeys)
        update.message.reply_text('There is your decrypted text : {}'.
        format(decrypted_text))
    except Exception:
         update.message.reply_text('Sorry, something went wrong.')
    return ConversationHandler.END

def decrypt(text, listKeys):
    for key in listKeys:
        final = ""
        key *= len(text)//len(key)+1
        for index, symbol in enumerate(text):
            temp=(tabula_recta.index(symbol)+len(tabula_recta)-tabula_recta.index(key[index]))%len(tabula_recta)
            final+=tabula_recta[temp]
        text = final
    return final

def get_key_list(keyword):
    listKeys = []
    for index in range(3):
        if index%2 != 0:
            listKeys.append(keyword[::-1])
        else:
            listKeys.append(keyword)
    return listKeys

def get_symbols(bot, update):
    update.message.reply_text(tabula_recta)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def cancel(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("<your token>")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", get_symbols))

    encryption_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('encrypt', encrypt_command)],
        states={
            ENCRYPT: [RegexHandler('.*',callback=encryption, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(encryption_conv_handler)

    decryption_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('decrypt', decrypt_command)],
        states={
            DECRYPT: [RegexHandler('.*', callback=decryption, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(decryption_conv_handler)
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
