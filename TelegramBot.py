import telebot
from telebot import types
import asana
from TelegaFunctions import get_user_gid, get_gid_project, get_workspace_map

client_asana = asana.Client.access_token("1/383667085808411:fe9ad11908a3bae3f063662649f7e589")
bot = telebot.TeleBot("1999468498:AAHvT8bqUqyQ2ZaYx2HHxD9vv6l3mOMgKRY")
workspace_name = "eltorg66.ru"
project_name = "Движение заявок Сборка"
user_name = "utkin@eltorg66.ru"

markup = types.InlineKeyboardMarkup(row_width=2)
go_to_asana_button = types.InlineKeyboardButton('Создать задачу', callback_data='create')
cancel_button = types.InlineKeyboardButton('Отмена', callback_data='cancel')
markup.row(go_to_asana_button, cancel_button)

my_message = None


@bot.message_handler(content_types=['document', 'photo'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ого, это же полная хрень ! Ты же не будешь этим заниматься, бро ? "
                                      "Перешлём Петько?", reply_markup=markup)
    global my_message
    my_message = message


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global my_message
    try:
        if call.message:
            if call.data == "create":
                bot.send_message(call.message.chat.id, "Ща всё сделаем, сходи покури ...")

                file_info = bot.get_file(my_message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'E:\\Загрузки' + my_message.document.file_name
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
                    result['gid'], file_content=data, file_name=my_message.document.file_name, opt_pretty=True)

                bot.send_message(my_message.chat.id, "Задача создана, бро")

            if call.data == "cancel":
                bot.send_message(call.message.chat.id, "Да мне похуй, возись сам ...")
    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Дарова, чел! Я мало что умею, но всё же ...')


bot.infinity_polling()
