import telebot
from telebot import types
from datetime import datetime
import openai

#токен бота
bot = telebot.TeleBot('6201830922:AAETvNm4onehtfZCnJHCK6XvFlaFeEDrkoU')

#искусственный интелект
openai.api_key = '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'
@bot.message_handler(commands=['ai'])
def ai(message):
    bot.send_message(message.chat.id, 'Задавайте свой вопрос')
    bot.register_next_step_handler(message, intelect)
def intelect(message):
	bot.send_message(message.chat.id, 'Ждите ответа')
	response = openai.Completion.create(
		engine="text-davinci-003",
		prompt=f"{message.text}",
		max_tokens=1024,
		n=1,
		stop=None,
		temperature=0.5,
	)
	bot.send_message(message.chat.id, response.choices[0].text)

#начало
@bot.message_handler(commands=['start'])
def start(message):
	id = message.from_user.id
	file_db_id = open("БД с id пользователей.txt", "a")
	file_db_id.write(str(id) + '\n')
	file_db_id.close()

	# убрать повторяющиеся id
	file = 'БД с id пользователей.txt'
	uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
	gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))

    # узнать в каком классе учится ученик
	bot.send_message(message.chat.id, 'Привет, в каком классе ты учишься? (напиши только цифру)')
	bot.register_next_step_handler(message, clas)

#запись id человека и его класса в БД
def clas(message):
	username = message.from_user.id
	clas = message.text.strip()
	log = str(username) + '-' + str(clas)
	file_db = open("База Данных.txt", "a")
	file_db.write(log + '\n')
	file_db.close()
	bot.send_message(message.chat.id, 'Спасибо за информацию, теперь ты можешь пользоваться ботом')

	# убрать повторяющиеся значения из БД
	file = 'База Данных.txt'
	uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
	gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))

#сделать рассылку с текстом и картинкой если ты администратор
@bot.message_handler(commands=['rasilka'])
def rasilka(message):
	if message.chat.id == 1150892740:
		bot.send_message(message.chat.id, 'Отправьте текст, которы хотите пустить в рассылку')
		bot.register_next_step_handler(message, send)
	else:
		bot.send_message(message.chat.id, 'У вас нет прав для использования данной функции')
def send(message):
	global send_message_rasilka
	send_message_rasilka = message.text.strip()
	bot.send_message(message.chat.id, 'Отправьте картинку, которая будет прикреплена к тексту')
	bot.register_next_step_handler(message, photo_save)
def photo_save(message):
	file = str(message.photo[-1].file_id)
	for users in open('БД с id пользователей.txt', 'r').readlines():
		bot.send_photo(users, file, f'{send_message_rasilka}')

#если человек хочет узнать про меню в столовой
@bot.message_handler(commands=['pitanie'])
def pitanie(message):
	kb = types.InlineKeyboardMarkup(row_width=1)
	bt = types.InlineKeyboardButton(text="Меню", callback_data='bt1')
	bt1 = types.InlineKeyboardButton(text="Оставить жалобу", callback_data='bt2')
	kb.add(bt, bt1)
	bot.send_message(message.chat.id, 'Тут ты можешь посмотреть меню на неделю или оставить комментарий об еде, который будет направлен администрации', reply_markup=kb)

#отправляется жалоба конкретному пользователю (на данный момент администратору)
def bad(message):
	bad = message.text.strip()
	bot.send_message(1150892740, f'{bad}')

#скидывается учебный календарь
@bot.message_handler(commands=['kalendar'])
def kalendar(message):
    file = open('расписание.png', 'rb')
    bot.send_photo(message.chat.id, file,)

#скидывается информация об учителях и администрации
@bot.message_handler(commands=['uchetila'])
def uchetila(message):
	file = open('учителя и администрация.png', 'rb')
	bot.send_photo(message.chat.id, file, )

#предлагается выбор. либо узнать какие вообще уроки на неделе у тебя либо какой сейчас урок у тебя
@bot.message_handler(commands=['raspisanie'])
def raspisanie(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    bt8 = types.InlineKeyboardButton(text="Расписание на неделю", callback_data='bt9')
    bt9 = types.InlineKeyboardButton(text="Какой сейчас урок", callback_data='bt10')
    kb.add(bt8, bt9)
    bot.send_message(message.chat.id, 'Ты можешь посмотреть расписание на всю неделю или узнать какой сейчас у тебя урок', reply_markup=kb)

#все ответы на разные кнопки в боте
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
	if callback.data == 'bt1':
		kb = types.InlineKeyboardMarkup(row_width=1)
		bt2 = types.InlineKeyboardButton(text="Понедельник", callback_data='bt3')
		bt3 = types.InlineKeyboardButton(text="Втоник", callback_data='bt4')
		bt4 = types.InlineKeyboardButton(text="Среда", callback_data='bt5')
		bt5 = types.InlineKeyboardButton(text="Четверг", callback_data='bt6')
		bt6 = types.InlineKeyboardButton(text="Пятница", callback_data='bt7')
		bt7 = types.InlineKeyboardButton(text="Буфет", callback_data='bt8')
		kb.add(bt2, bt3, bt4, bt5, bt6, bt7)
		bot.send_message(callback.message.chat.id,'Выбери день на который ты хочешь посмотреть меню',reply_markup=kb)
	if callback.data == 'bt2':
		bot.send_message(callback.message.chat.id, 'Напиши свою жалобу и это сообщение отправится в чат с администрацией. (Не забудь указать свою фамилию и имя)')
		bot.register_next_step_handler(callback.message, bad)
	if callback.data == 'bt3':
		file = open('понедельник.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt4':
		file = open('вторник.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt5':
		file = open('среда.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt6':
		file = open('четверг.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt7':
		file = open('пятница.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt8':
		file = open('Буфет.png', 'rb')
		bot.send_photo(callback.message.chat.id, file)
	if callback.data == 'bt9':
		username_now = callback.message.chat.id
		file_db = open("База Данных.txt", "r")
		x = file_db.readlines()
		for cl in range(len(x)):
			s = [int(i) for i in x[cl].split('-')]
			if s[0] == int(username_now):
				raspic = s[1]
				break
		file_db.close()
		if raspic == 11:
			file = open('расписание 11 класса.png', 'rb')
			bot.send_photo(callback.message.chat.id, file)
		elif raspic == 10:
			file = open('расписание 10 класса.png', 'rb')
			bot.send_photo(callback.message.chat.id, file)
		elif raspic == 9:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
		elif raspic == 8:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
		elif raspic == 7:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
		elif raspic == 6:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
		elif raspic == 5:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
		elif raspic == 4:
			bot.send_message(callback.message.chat.id, 'Скоро добавим ваше расписание')
	if callback.data == 'bt10':
		username_now = callback.message.chat.id
		file_db = open("База Данных.txt", "r")
		x = file_db.readlines()
		for cl in range(len(x)):
			s = [int(i) for i in x[cl].split('-')]
			if s[0] == int(username_now):
				raspic = s[1]
				break
		file_db.close()
		current_datetime = datetime.now()
		hour = int(current_datetime.hour)
		minute = int(current_datetime.minute)
		week = int(datetime.weekday(current_datetime))
		if raspic == 11:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 204 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 204 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физической культуры в гранд арене')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физической культуры в гранд арене')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 204 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок естествознания в 222 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок естествознания в 222 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас окно')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас окно')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок обществознания в 205 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок обществознания в 205 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 201 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок естествознания в 222 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок истории в 205 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок английского языка в 219 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 204 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок право в 204 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 204 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас ассамблея в актовом зале')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок английского языка в 219 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 205 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 10:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 203 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 205 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физический культуры в Градн Арене')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физический культуры в Градн Арене')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок истории в 205 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок истории в 205 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок английского языка в 220 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок фикизи в 224 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок биологии в 222 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 201 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 203 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 203 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок обществознания в 205 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок английского языка в 220 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок географии в 201 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок английского языка в 220 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейчас урок русского языка в 203 кабинете')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок химии в 224 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок информатики в 219 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физики в 224 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок физики в 224 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Сейчас урок истории в 205 кабинете')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Сейсас ассамблея в актовом зале')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Сейчас урок математики в 202 кабинете')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Сейчас урок литературы в 203 кабинете')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Сейчас урок географии в 201 кабинете')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 9:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 8:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 7:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 6:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 5:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
		elif raspic == 4:
			if week == 0:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 1:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 2:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 3:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')
			elif week == 4:
				if hour == 9 and minute < 40:
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 9 and minute > 55) or (hour == 10 and minute < 35):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 10 and minute > 50) or (hour == 11 and minute < 30):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 11 and minute > 40) or (hour == 12 and minute < 20):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 12 and minute > 30) or (hour == 13 and minute < 10):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				elif (hour == 13 and minute > 20) or (hour == 13 and minute < 59):
					bot.send_message(callback.message.chat.id, 'Скоро появится информация')
				else:
					bot.send_message(callback.message.chat.id, 'У тебя сейчас нет урока')

#непрерывная работа
bot.polling(none_stop=True)