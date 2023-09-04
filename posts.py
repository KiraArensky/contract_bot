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
    con.commit()


def how_join(bot, message, cur, con):
    msg = bot.send_message(message.chat.id, text="Информация о том, как поступить на службу")
    cur.execute(
        f'''UPDATE id SET back = {msg.id} WHERE id = {message.chat.id} ''')
    con.commit()
