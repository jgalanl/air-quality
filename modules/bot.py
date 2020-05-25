import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from auth import token

from db import extract_date, extract_list

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_calidad(air_quality_predicted):
    if air_quality_predicted >= 301:
        return 'nociva'
    elif air_quality_predicted >= 201 and air_quality_predicted <= 300:
        return 'muy mala'
    elif air_quality_predicted >= 151 and air_quality_predicted <= 200:
        return 'mala'
    elif air_quality_predicted >= 101 and air_quality_predicted <= 150:
        return 'mala'
    elif air_quality_predicted >= 51 and air_quality_predicted <= 100:
        return 'media'
    elif air_quality_predicted >= 0 and air_quality_predicted <= 50:
        return 'buena'

def start(update, context):
    message = """¡Encantado de conocerte! ¿Qué puedo hacer por ti? \n
    /air hh:mm dd-MM. Conocer la calidad del aire un momento concreto.
    /list dd-MM. Conocer las horas con mejor calidad del aire.
    /help. Ayuda sobre cómo hablar conmigo. 
    """
    
    # Para conocer la calidad del aire introduce el comando /air seguido de la fecha en formato dd-mm'
    update.message.reply_text(message)

def air(update, context):
    try:
        full_date = update.message.text.split(' ')
        hour = full_date[1]
        date = full_date[2]
        if hour is None or date is None:
            update.message.reply_text('No te he entendido.')
            return

        # Extraer informacion de la bbdd
        result = extract_date(hour, date)

        if result is None:
            update.message.reply_text("""Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.""")
            return

        air_quality_predicted = result['air_quality_predicted']

        calidad = ''
        recomendacion = ''

        if air_quality_predicted >= 301:
            calidad = 'nociva'
            recomendacion = 'El aire estará irrespirable. Yo no saldría de casa...'
        elif air_quality_predicted >= 201 and air_quality_predicted <= 300:
            calidad = 'muy mala'
            recomendacion = 'La calidad del aire será muy mala. No salgas de casa salvo que sea necesario.'
        elif air_quality_predicted >= 151 and air_quality_predicted <= 200:
            calidad = 'mala'
            recomendacion = 'En caso de salir al exterior utiliza una mascarilla.'
        elif air_quality_predicted >= 101 and air_quality_predicted <= 150:
            calidad = 'mala'
            recomendacion = 'Hay bastante contaminación. Procura no estar mucho tiempo fuera.'
        elif air_quality_predicted >= 51 and air_quality_predicted <= 100:
            calidad = 'media'
            recomendacion = 'Habrá un poco de contaminación pero se puede salir de casa.'
        elif air_quality_predicted >= 0 and air_quality_predicted <= 50:
            calidad = 'buena'
            recomendacion = 'No habrá ni pizca de contaminación.'

        message = 'La calidad del aire será de {}, {}. {}'.format(air_quality_predicted, calidad, recomendacion)
       
        update.message.reply_text(message)

    except Exception:
        update.message.reply_text('No te he entendido')

def list(update, context):
    try:
        date = update.message.text.split(' ')[1]

        result = extract_list(date)
        if result is None:
            update.message.reply_text('No te he entendido')
            return

        message = 'Estas son las horas con menos contaminación para ese día: \n'
        for i in result:
            hour = i['date'].split('/')[1]
            air_quality_predicted = i['air_quality_predicted']
            calidad = get_calidad(air_quality_predicted)
            string = '{}. Nivel: {}, {}. \n'.format(hour, air_quality_predicted, calidad)
            message += string

        update.message.reply_text(message)

    except Exception:
        update.message.reply_text('No te he entendido')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("air", air))
    dp.add_handler(CommandHandler("list", list))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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