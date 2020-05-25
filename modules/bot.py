import logging
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from auth import token

from db import extract_date, extract_list

import spacy
nlp = spacy.load("es_core_news_md")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_calidad_recomendacion(air_quality_predicted):
    if air_quality_predicted >= 301:
        return 'nociva', 'El aire estará irrespirable. Yo no saldría de casa'
    elif air_quality_predicted >= 201 and air_quality_predicted <= 300:
        return 'muy mala', 'La calidad del aire será muy mala. No salgas de casa salvo que sea necesario'
    elif air_quality_predicted >= 151 and air_quality_predicted <= 200:
        return 'mala', 'En caso de salir al exterior utiliza una mascarilla'
    elif air_quality_predicted >= 101 and air_quality_predicted <= 150:
        return 'mala', 'Hay bastante contaminación. Procura no estar mucho tiempo fuera'
    elif air_quality_predicted >= 51 and air_quality_predicted <= 100:
        return 'media', 'Habrá un poco de contaminación pero se puede salir de casa'
    elif air_quality_predicted >= 0 and air_quality_predicted <= 50:
        return 'buena', 'No habrá ni pizca de contaminación'

def start(update, context):
    message = """¡Encantado de conocerte! ¿Qué puedo hacer por ti? \n
    /air hh:mm dd-MM. Conocer la calidad del aire un momento concreto.
    /list dd-MM. Conocer las horas con mejor calidad del aire.
    /help. Ayuda sobre cómo hablar conmigo. 
    """
    
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
            update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
            return

        air_quality_predicted = result['air_quality_predicted']
        temperature = result['temperature']

        calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)

        message = 'La calidad del aire será de {}, {}, con una temperatura de {}°C. {}.'.format(air_quality_predicted, calidad, temperature, recomendacion)
       
        update.message.reply_text(message)

    except Exception:
        update.message.reply_text('No te he entendido')

def list(update, context):
    try:
        date = update.message.text.split(' ')[1]

        result = extract_list(date)
        if result is None:
            update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
            return

        message = 'Estas son las horas con menos contaminación para ese día: \n'
        for i in result:
            hour = i['date'].split('/')[1]
            air_quality_predicted = i['air_quality_predicted']
            calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)
            temperature = i['temperature']
            description = i['description']
            string = '{}. Nivel: {}, {}. Temperatura: {}°C. Pronóstico: {}. Recomendación: {}. \n'.format(hour, air_quality_predicted, calidad, temperature, description, recomendacion)
            message += string

        update.message.reply_text(message)

    except Exception:
        update.message.reply_text('No te he entendido')


def help(update, context):
    message = """ ¿En qué puedo ayudarte? \n
    /air hh:mm dd-MM. Conocer la calidad del aire un momento concreto. Ejemplo: /air 13:00 26-05
    /list dd-MM. Conocer las horas con mejor calidad del aire. Ejemplo: /list 26-05
    /help. Ayuda sobre cómo hablar conmigo. 
    """

    update.message.reply_text(message)


def echo(update, context):
    message = ''
    document = nlp(update.message.text)

    # Comprobar intents
    # Extraer advervios, nombres y numeros
    noum = []
    adv = ''
    num = []
    for s in document.sents:
        for token in s:
            if token.tag_ == 'ADV___':
                adv = token.orth_
            if token.tag_ == 'NOUN__AdvType=Tim' or token.tag_ == "NUM__NumForm=Digit|NumType=Card":
                num.append(token.orth_)
            if token.pos_ =="NOUN":
                noum.append(token.orth_.lower())

    if "gracias" in noum:
        message = "¡De nada! Espero acertar más que el hombre del tiempo."
        update.message.reply_text(message)
        
        return

    # Obtener nombres propios o de ciudades
    if document.ents is not None:
        if not 'leganés' in str(document.ents).lower() and len(document.ents) > 1:
            message = 'De momento solo conozco Leganés, culpa de mis creadores. ¡Lo siento!'
            update.message.reply_text(message)
            return

    if 'hoy' in adv and len(num) == 0:
        date = '{}-0{}'.format(datetime.datetime.today().day, datetime.datetime.today().month)
        result = extract_list(date)
        if result is None:
            update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
            return

        message = 'Estas son las horas con menos contaminación para ese día: \n'
        for i in result:
            hour = i['date'].split('/')[1]
            air_quality_predicted = i['air_quality_predicted']
            calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)
            temperature = i['temperature']
            description = i['description']
            string = '{}. Nivel: {}, {}. Temperatura: {}°C. Pronóstico: {}. {}.\n'.format(hour, air_quality_predicted, calidad, temperature, description, recomendacion)
            message += string

        update.message.reply_text(message)
        
        return 
    
    elif 'hoy' in adv and len(num) > 0:
        date = '{}-0{}'.format(datetime.datetime.today().day, datetime.datetime.today().month)
        hour = num[0].replace('/','-')
        result = extract_date(hour, date)
        if result is None:
            update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
            return
        
        air_quality_predicted = result['air_quality_predicted']
        temperature = result['temperature']

        calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)

        message = 'La calidad del aire será de {}, {}, con una temperatura de {}°C. {}.'.format(air_quality_predicted, calidad, temperature, recomendacion)
        
        update.message.reply_text(message)
        
        return
    
    else:
        if not adv and len(num) == 1:
            date = num[0].replace('/', '-')
            result = extract_list(date)
            if result is None:
                update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
                return

            message = 'Estas son las horas con menos contaminación para ese día: \n'
            for i in result:
                hour = i['date'].split('/')[1]
                air_quality_predicted = i['air_quality_predicted']
                calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)
                temperature = i['temperature']
                description = i['description']
                string = '{}. Nivel: {}, {}. Temperatura: {}°C. Pronóstico: {}. {}.\n'.format(hour, air_quality_predicted, calidad, temperature, description, recomendacion)
                message += string

            update.message.reply_text(message)
            
            return

        elif not adv and len(num) == 2:
            date = num[0].replace('/', '-')
            hour = num[1]

            result = extract_date(hour, date)

            if result is None:
                update.message.reply_text("Aún no tengo información sobre la fecha que me has dicho. Prueba dentro de unos días.")
                return

            air_quality_predicted = result['air_quality_predicted']
            temperature = result['temperature']

            calidad, recomendacion = get_calidad_recomendacion(air_quality_predicted)

            message = 'La calidad del aire será de {}, {}, con una temperatura de {}°C. {}.'.format(air_quality_predicted, calidad, temperature, recomendacion)
            update.message.reply_text(message)

            return

    update.message.reply_text('No te he entendido.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
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

    updater.idle()


if __name__ == '__main__':
    main()