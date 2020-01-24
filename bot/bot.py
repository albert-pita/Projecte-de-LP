# importa l'API de Telegram
import telegram
import pickle
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram import ParseMode
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import OrderedDict

resKeeper = {}


# defineix /start
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola " +
                     update.message.chat.first_name + ' ' +
                     update.message.chat.last_name + "! Em dic Wilson" +
                     " i sóc un bot dissenyat per " +
                     "fer enquestes a través de Telegram.")


# defineix /help
def help_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="El propòsit " +
                     "d'aquest bot és recollir dades d'enquestes " +
                     "fetes a través de Telegram, i poder fer consultes " +
                     "gràfiques i informes sobre les dades recollides.")
    bot.send_message(chat_id=update.message.chat_id, text="Les comandes" +
                     " possibles són:\n" +
                     "/start\n/help\n/author\n/quiz <idEnquesta>\n" +
                     "/bar <idPregunta>\n/pie <idPregunta>\n/report")


# defineix /author
def author_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Autor: " +
                     "Albert Pita Argemí\n" +
                     "Correu: albert.pita@est.fib.upc.edu")


# defineix / quiz
def quiz_command(bot, update, args, user_data):
    try:
        global resKeeper
        with open('resKeeper.pkl', 'rb') as pickle_file:
            resKeeper = pickle.load(pickle_file)

        idEnquesta = args[0]

        if 'num_pregunta' not in user_data:
            user_data['num_pregunta'] = 1
            user_data['option'] = False
            user_data['node_opt'] = "-1"

        if user_data['num_pregunta'] != 1:
            user_data['num_pregunta'] = 1
            user_data['option'] = False
            user_data['node_opt'] = "-1"

        with open('graph.pkl', 'rb') as pickle_file:
            DG = pickle.load(pickle_file)

        bot.send_message(chat_id=update.message.chat_id, text="Enquesta E:")

        question = "E> "
        iterator_q = DG.successors(idEnquesta)

        next_q = next(iterator_q)
        while DG[idEnquesta][next_q]['tipus'] != 2:
            next_q = next(iterator_q)

        if DG.nodes[next_q]['text'] != "END":

            question += DG.nodes[next_q]['text'] + '\n'

            iterator_a = DG.successors(next_q)
            l = [x for x in iterator_a if DG[next_q][x]['tipus'] == 3]

            if len(l) != 0:
                user_data['option'] = True
                if user_data['node_opt'] == "-1":
                    iterator_a = DG.successors(next_q)
                    l = [x for x in iterator_a if DG[next_q][x]['tipus'] == 2]
                    user_data['node_opt'] = l[0]

            iterator_a = DG.successors(next_q)
            next_a = next(iterator_a)
            while DG[next_q][next_a]['tipus'] != 1:
                next_a = next(iterator_a)

            for x in DG.nodes[next_a]['dic_opt']:
                opt = DG.nodes[next_a]['dic_opt'][x]
                question += x + ": " + opt[:-2] + '\n'

        else:
            question += "Gràcies pel teu temps!"

        bot.send_message(chat_id=update.message.chat_id, text=question)

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# defineix com processar les respostes
def handle_message(bot, update, user_data):
    try:
        answer = update.message.text

        with open('graph.pkl', 'rb') as pickle_file:
            DG = pickle.load(pickle_file)

        node_anterior = "P" + str(user_data['num_pregunta'])

        if node_anterior not in resKeeper:
            resKeeper[node_anterior] = {}
            resKeeper[node_anterior][int(answer)] = 1
        else:
            if int(answer) not in resKeeper[node_anterior]:
                resKeeper[node_anterior][int(answer)] = 1
            else:
                resKeeper[node_anterior][int(answer)] += 1

        with open('resKeeper.pkl', 'wb') as pickle_file:
            pickle.dump(resKeeper, pickle_file)

        question = "E> "
        iterator_q = DG.successors(node_anterior)

        if user_data['option']:
            l = [x for x in iterator_q if DG[node_anterior][x]['tipus'] == 3
                 if DG[node_anterior][x]['text'] == answer]
            if len(l) != 0:
                user_data['num_pregunta'] = int(l[0][1:])
                next_q = l[0]

            else:
                user_data['num_pregunta'] += 1
                iterator_q = DG.successors(node_anterior)
                next_q = next(iterator_q)
                while DG[node_anterior][next_q]['tipus'] != 2:
                    next_q = next(iterator_q)

        else:
            user_data['num_pregunta'] += 1
            l = [x for x in iterator_q if DG[node_anterior][x]['tipus'] == 2]
            if len(l) != 0:
                next_q = l[0]
            else:
                next_q = user_data['node_opt']
                user_data['node_opt'] = "-1"

        if DG.nodes[next_q]['text'] != "END":
            question += DG.nodes[next_q]['text'] + '\n'

            iterator_a = DG.successors(next_q)
            l = [x for x in iterator_a if DG[next_q][x]['tipus'] == 3]

            if user_data['option']:
                user_data['option'] = False
            if len(l) != 0:
                user_data['option'] = True
                if user_data['node_opt'] == "-1":
                    iterator_a = DG.successors(next_q)
                    l = [x for x in iterator_a if DG[next_q][x]['tipus'] == 2]
                    user_data['node_opt'] = l[0]

            iterator_a = DG.successors(next_q)
            next_a = next(iterator_a)
            while DG[next_q][next_a]['tipus'] != 1:
                next_a = next(iterator_a)

            for x in DG.nodes[next_a]['dic_opt']:
                opt = DG.nodes[next_a]['dic_opt'][x]
                question += x + ": " + opt[:-2] + '\n'

        else:
            question += "Gràcies pel teu temps!"

        bot.send_message(chat_id=update.message.chat_id, text=question)

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# defineix / pie
def pie_command(bot, update, args):
    try:
        global resKeeper
        with open('resKeeper.pkl', 'rb') as pickle_file:
            resKeeper = pickle.load(pickle_file)

        question = resKeeper[args[0]]

        sortedQuestion = OrderedDict(sorted(question.items(),
                                     key=lambda x: x[1], reverse=True))

        labels = sortedQuestion.keys()
        sizes = sortedQuestion.values()
        explode = [0.1] * len(labels)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True)
        ax1.axis('equal')

        plt.savefig('pie.png')
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open('pie.png', 'rb'))
        os.remove('pie.png')

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# defineix / bar
def bar_command(bot, update, args):
    try:
        global resKeeper
        with open('resKeeper.pkl', 'rb') as pickle_file:
            resKeeper = pickle.load(pickle_file)

        question = resKeeper[args[0]]

        sortedQuestion = OrderedDict(sorted(question.items(),
                                     key=lambda x: x[1], reverse=True))

        objects = sortedQuestion.keys()
        y_pos = np.arange(len(objects))
        performance = sortedQuestion.values()

        fig, ax = plt.subplots()
        rects = plt.bar(y_pos, performance, align='center', alpha=1.0)
        plt.xticks(y_pos, objects)

        plt.savefig('bar.png')
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open('bar.png', 'rb'))
        os.remove('bar.png')

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# defineix / command
def report_command(bot, update):
    try:
        global resKeeper
        with open('resKeeper.pkl', 'rb') as pickle_file:
            resKeeper = pickle.load(pickle_file)

        message = "*pregunta  valor  respostes*\n"
        for i in resKeeper:
            sortedP = sorted(resKeeper[i].items(),
                             key=lambda t: t[1], reverse=True)
            for x, y in sortedP:
                message += i + "  " + str(x) + "  " + str(y) + '\n'

        bot.send_message(chat_id=update.message.chat_id,
                         text=message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('author', author_command))

dispatcher.add_handler(CommandHandler('quiz', quiz_command,
                                      pass_args=True, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.regex(r'^[0-9]+$'),
                                      handle_message, pass_user_data=True))

dispatcher.add_handler(CommandHandler('pie', pie_command, pass_args=True))
dispatcher.add_handler(CommandHandler('bar', bar_command, pass_args=True))
dispatcher.add_handler(CommandHandler('report', report_command))

# engega el bot
updater.start_polling()
