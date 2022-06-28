import telebot
from telebot import types
import asana
from TelegaFunctions import get_user_gid, get_gid_project, get_workspace_map

client_asana = asana.Client.access_token("1/383667085808411:fe9ad11908a3bae3f063662649f7e589")
bot = telebot.TeleBot("1999468498:AAHvT8bqUqyQ2ZaYx2HHxD9vv6l3mOMgKRY")
workspace_name = "TEST"
project_name = "Движение заказов"
user_name = "utkin@eltorg66.ru"

markup = types.ReplyKeyboardMarkup()
go_to_asana_button = types.KeyboardButton('Создать задачу')
cancel_button = types.KeyboardButton('Отмена')
markup.row(go_to_asana_button, cancel_button)


@bot.message_handler(content_types=['document', 'image'])
def send_welcome(message):

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'E:\\Загрузки' + message.document.file_name
    with open(src, 'wb') as new_file:
        # записываем данные в файл
        new_file.write(downloaded_file)

    gid_workspace, _ = get_workspace_map(workspace_name)
    gid_project = get_gid_project(workspace_name, project_name)
    user_gid = get_user_gid(gid_workspace, user_name)

    template_task = {"workspace": gid_workspace,
                     "assignee": user_gid,
                     "projects": gid_project,
                     "name": "Рассчитать проект по ТЗ",
                     "notes": "Рассчитать проект по приложенному ТЗ"}

    result = client_asana.tasks.create_task(template_task, opt_pretty=True)

    with open(src, 'rb') as f:
        data = f.read()
    client_asana.attachments.create_attachment_for_task(
        result['gid'], file_content=data, file_name=message.document.file_name, opt_pretty=True)

    bot.send_message(message.chat.id, "Задача создана, бро")


# @bot.message_handler(content_types=['document', 'image'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, "Создать задачу для Петько ?", reply_markup=markup)


# @bot.message_handler(content_types='text')
# def message_reply(message):
#
#     if message.text == "Создать задачу":
#         gid_workspace, _ = get_workspace_map(workspace_name)
#         gid_project = get_gid_project(workspace_name, project_name)
#         user_gid = get_user_gid(gid_workspace, user_name)
#
#         template_task = {"workspace": gid_workspace,
#                          "assignee": user_gid,
#                          "projects": gid_project,
#                          "name": "Рассчитать проект по ТЗ",
#                          "notes": "Рассчитать проект по приложенному ТЗ"}
#
#         result = client_asana.tasks.create_task(template_task, opt_pretty=True)
#
#         src = send_welcome()
#
#         with open(src, 'rb') as f:
#             data = f.read()
#         client_asana.attachments.create_attachment_for_task(
#             result['gid'], file_content=data, file_name=message.document.file_name, opt_pretty=True)
#
#         bot.send_message(message.chat.id, "Задача создана, бро")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
