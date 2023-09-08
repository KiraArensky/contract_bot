from telebot import types


def support(bot, message, cur, con):
    markup = types.InlineKeyboardMarkup()  # cоздание inline кнопок
    markup_list = [types.InlineKeyboardButton("Контрактник, гражданин РФ", callback_data='sup_1'),
                   types.InlineKeyboardButton("Доброволец", callback_data='sup_2'),
                   types.InlineKeyboardButton("Контрактник, иностранец", callback_data='sup_3'),
                   types.InlineKeyboardButton("Члены семьи контрактников и добровольцев", callback_data='sup_4'),
                   types.InlineKeyboardButton("Мобилизованный", callback_data='sup_5'),
                   types.InlineKeyboardButton("Члены семьи мобилизованных", callback_data='sup_6'),
                   types.InlineKeyboardButton("Военнослужащие и сотрудники федеральных органов", callback_data='sup_7'),
                   types.InlineKeyboardButton("Члены семей военнослужащих и сотрудников федеральных органов",
                                              callback_data='sup_8'),
                   types.InlineKeyboardButton("Иные категории граждан, награжденные наградами РФ",
                                              callback_data='sup_9')]
    for btn in markup_list:
        markup.row(btn)
    msg = bot.send_message(message.chat.id, text="Выбери свою категорию:", reply_markup=markup)
    cur.execute(
        f'''UPDATE id SET back = {msg.id} WHERE id = {message.chat.id} ''')
    cur.execute(
        f'''UPDATE id SET post_number = 0 WHERE id = {message.chat.id} ''')
    con.commit()


def how_join(bot, message, cur, con):
    msg = bot.send_message(message.chat.id,
                           text="<b>Чтобы поступить на службу по контракту тебе необходимо выполнить 5 шагов:</b>\n\n"
                                "1. Позвонить специалисту горячей линии по телефону 8 800 301 68 88"
                                " (звонок бесплатен и доступен круглосуточно)\n"
                                "2. Сообщить о времени и месте прибытия в выбранный город ХМАО. Вас"
                                " встретят сотрудники военкомата. Затраты на билеты будут компенсированы "
                                "в течение 1 суток\n"
                                "3. Подать заявление на службу по контракту можно подать через портал "
                                "госуслуг или лично в пункте отбора. Сотрудник пункта отбора рассматривает"
                                " заявление не более 3 рабочих дней. Информацию о принятом решении направят "
                                "на указанный телефон SMS-сообщением, эл. почту, по адресу проживания, на портал "
                                "госуслуг. Пройти медицинский осмотр в Югре за 1 сутки\n"
                                "4. Подписать контракт на службу в вооруженных силах РФ\n"
                                "5. Отбыть в военную часть Вооруженных сил Министерства Обороны РФ\n\n"
                                "Больше подробностей ищи здесь: https://voin86.ru/?ysclid=lmav21f8ez765721714",
                           parse_mode="HTML")
    cur.execute(
        f'''UPDATE id SET back = {msg.id} WHERE id = {message.chat.id} ''')
    con.commit()


def change_city(bot, message, cur, con):
    markup = types.InlineKeyboardMarkup()  # cоздание inline кнопок
    btn1 = types.InlineKeyboardButton("Нефтеюганский район", callback_data='nefteyugansk')
    btn2 = types.InlineKeyboardButton("Другая территория", callback_data='other')
    markup.row(btn1, btn2)

    msg = bot.send_message(message.chat.id, text="Выбери регион", reply_markup=markup)
    cur.execute(
        f'''UPDATE id SET back = {msg.id} WHERE id = {message.chat.id} ''')
    con.commit()
