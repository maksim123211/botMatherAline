from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, ReplyKeyboardRemove as RKR, ReplyKeyboardMarkup as RKM
from app.bot import handler
from app.models import Account
from datetime import datetime, timezone
from decimal import Decimal
import ujson


# @handler.callback(name='add_event', admin=True)
# async def _(callback, path_args, bot, user):
#     user.dialog = Account.Dialog.CREATE_EVENT_TITLE
#     user.save()
#     await callback.message.delete()
#     await user.reply('⭐️ Отправьте <b>название</b> для нового мероприятия, которое вы хотите добавить в систему', keyboard=RKR())
 
 
# @handler.message(name='', dialog = Account.Dialog.CREATE_EVENT_TITLE, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.dumps({'title': message.text})
#     user.dialog = Account.Dialog.CREATE_EVENT_DESC
#     user.save()
#     await user.reply('✏️ Задайте <b>описание</b> для нового мероприятия, добавляемого в систему')
 
 
# @handler.message(name='', dialog = Account.Dialog.CREATE_EVENT_DESC, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     user.temp['desc'] = message.text
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.CREATE_EVENT_PLACE
#     user.save()
#     await user.reply('🔗 Задайте <b>место</b> для нового мероприятия')
 

# @handler.message(name='', dialog=Account.Dialog.CREATE_EVENT_PLACE, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     user.temp['place'] = message.text
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.CREATE_EVENT_COST
#     user.save()
#     await user.reply('💵 Задайте <b>стоимость билета</b> для нового мероприятия')


# @handler.message(name='', dialog=Account.Dialog.CREATE_EVENT_COST, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     try:
#         cost = Decimal(message.text)
#         assert cost > 0
#     except:
#         return await user.reply('❗️ Укажите стоимость билета числом превышающее ноль. Например: 1500')
#     user.temp['cost'] = cost
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.CREATE_EVENT_NUMBER_OF_TICKETS
#     user.save()
#     await user.reply('💵 Задайте <b>количество доступных билетов</b> для нового мероприятия', keyboard=RKM([
#             ['⏩ Неограничено']
#         ], resize_keyboard=True))


# @handler.message(name='', dialog=Account.Dialog.CREATE_EVENT_NUMBER_OF_TICKETS, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     if message.text.isdigit():
#         user.temp['number_of_tickets'] = message.text
#     elif 'неограничено' in message.text.lower():
#         user.temp['number_of_tickets'] = None
#     else:
#         return await user.reply('❗️ Укажите количество билетов числом. Например: 100')
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.CREATE_EVENT_DATE_OF_EVENT
#     user.save()
#     await user.reply('💵 Задайте <b>дату проведения</b> для нового мероприятия в формате: 12.10.2020 15:00', keyboard=RKR())


# @handler.message(name='', dialog=Account.Dialog.CREATE_EVENT_DATE_OF_EVENT, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     try:
#         date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
#         assert date > datetime.now()
#     except ValueError:
#         return await user.reply('❗️ Дата мероприятия должна быть в формате: 12.10.2020 15:00')
#     except:
#         return await user.reply('❗️ Дата проведения мероприятия должна находиться в будущем')
#     user.temp['date_of_event'] = message.text
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.CREATE_EVENT_FINISH_DATE
#     user.save()
#     await user.reply('💵 Задайте <b>дату окончания покупки билетов</b> для нового мероприятия в формате: 12.10.2020 15:00', keyboard=RKM([
#             ['⏩ Пропустить']
#         ], resize_keyboard=True))


# @handler.message(name='', dialog=Account.Dialog.CREATE_EVENT_FINISH_DATE, admin=True)
# async def _(message, path_args, bot, user):
#     user.temp = ujson.loads(user.temp)
#     if 'пропустить' in message.text.lower():
#         user.temp['finish_date'] = None
#     else:
#         try:
#             date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
#             end_date = datetime.strptime(user.temp['date_of_event'], '%d.%m.%Y %H:%M')
#             assert date > datetime.now() and date <= end_date
#         except ValueError:
#             return await user.reply('❗️ Дата окончания покупки должна быть в формате: 12.10.2020 15:00')
#         except:
#             return await user.reply('❗️ Дата окончания покупки должна находиться в будущем и не должна быть больше даты окончания мероприятия')
#         user.temp['finish_date'] = message.text
#     user.temp = ujson.dumps(user.temp)
#     user.dialog = Account.Dialog.DEFAULT
#     data = ujson.loads(user.temp)
#     user.save()
#     Event.objects.create(title = data['title'], desc = data['desc'], place = data['place'], cost = data['cost'], number_of_tickets = data['number_of_tickets'],\
#      date_of_event = data['date_of_event'] and datetime.strptime(data['date_of_event'], '%d.%m.%Y %H:%M'), finish_date = data['finish_date'] and datetime.strptime(data['finish_date'], '%d.%m.%Y %H:%M'), create_date = datetime.now())
#     await user.return_menu('✅ Проект успешно <b>создан!</b> Вы сможете просмотреть, отредактировать или удалить его используя вашу панель администратора.')
#     await user.reply('Либо вы можете вернуться к вашим мероприятиям', keyboard = IKM([[IKB('Вернуться к списку', callback_data = 'return_events')]]))
        

# ##############################################################################################

# # @handler.callback(name='edit_event')
# # async def _(callback, path_args, bot, user):
# #     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
# #         event = Event.objects.filter(id=path_args[1]).first()
# #         count = event.number_of_tickets if event.number_of_tickets >= 1 else 'Неограничено'
# #         await callback.message.edit_text(f'💼 Мероприятие: {event.title}\nСтоимость: {event.cost}\nДата проведения: {event.date_of_event}\nОписание: {event.desc}\nМесто проведения: {event.place}\n\
# #         Количество билетов: {count}', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# #                 [IKB('⭐️ Изменить название', callback_data=f'edit_event_title {event.id}')],
# #                 [IKB('✏️ Изменить описание', callback_data=f'edit_event_desc {event.id}')],
# #                 [IKB('✏️ Изменить место', callback_data=f'edit_event_place {event.id}')],
# #                 [IKB('✏️ Изменить стоимость', callback_data=f'edit_event_cost {event.id}')],
# #                 [IKB('🔗 Изменить количество билетов', callback_data=f'edit_event_number_of_tickets {event.id}')],
# #                 [IKB('✏️ Изменить дату мероприятия', callback_data=f'edit_event_date_of_event {event.id}')],
# #                 [IKB('💵 Изменить дату окончания продаж', callback_data=f'edit_event_finish_date {event.id}')],
# #                 [IKB('🗑 Удалить', callback_data=f'delete_event {event.id}')],
# #             ]))

# ##########################################################################################################################
 
# @handler.callback(name='edit_event_title')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_TITLE_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новое название для данного мероприятия', keyboard=RKR())
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_TITLE_DIALOG)
# async def _(message, path_args, bot, user):
#     if user.admin == True or user.super_admin == True:
#         event = Event.objects.filter(id = int(user.temp)).first()
#         if event is not None:
#             event.title = message.text
#             event.save()
#             user.dialog = Account.Dialog.DEFAULT
#             user.save()
#             await user.reply(f'✅ Название мероприятия успешно изменено на <b>{event.title}</b>', keyboard=IKM(inline_keyboard=[
#                 [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#                 [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#                 ]))
 
 
# @handler.callback(name = 'edit_event_desc')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_DESC_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новое описание для данного проекта', keyboard=RKR())
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_DESC_DIALOG)
# async def _(message, path_args, bot, user):
#     if user.admin == True or user.super_admin == True:
#         event = Event.objects.filter(id = int(user.temp)).first()
#         if event is not None:
#             event.desc = message.text
#             event.save()
#             user.dialog = Account.Dialog.DEFAULT
#             user.save()
#             await user.reply(f'✅ Описание мероприятия успешно изменено на\n\n<b>{event.desc}</b>', keyboard=IKM(inline_keyboard=[
#                 [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#                 [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#                 ]))
 
 
# @handler.callback(name='edit_event_place', admin=True)
# async def _(callback, path_args, bot, user):
#     if len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_PLACE_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новое местоположение для данного мероприятия', keyboard=RKR())
 

# @handler.message(name='', dialog=Account.Dialog.EDIT_EVENT_PLACE_DIALOG, admin=True)
# async def _(message, path_args, bot, user):
#     event = Event.objects.filter(id = int(user.temp)).first()
#     if event is not None:
#         event.place = message.text
#         event.save()
#         user.dialog = Account.Dialog.DEFAULT
#         user.save()
#         await user.reply(f'✅ Местоположение мероприятия успешно изменено на <b>{event.place}</b>', keyboard=IKM(inline_keyboard=[
#             [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#             [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#         ]))
 

# @handler.callback(name='edit_event_cost', admin=True)
# async def _(callback, path_args, bot, user):
#     if len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_COST_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новую стоимость билета для данного мероприятия', keyboard=RKR())
 

# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_COST_DIALOG, admin = True)
# async def _(message, path_args, bot, user):
#     event = Event.objects.filter(id = int(user.temp)).first()
#     if event is not None:
#         event.cost = int(message.text)
#         event.save()
#         user.dialog = Account.Dialog.DEFAULT
#         user.save()
#         await user.reply(f'✅ Стоимость билета успешно изменена на <b>{event.cost}</b>', keyboard=IKM(inline_keyboard=[
#             [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#             [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#             ]))


# @handler.callback(name = 'edit_event_number_of_tickets')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_NUMBER_OF_TICKETS_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новое количество билетов для данного мероприятия', keyboard=RKR())
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_NUMBER_OF_TICKETS_DIALOG)
# async def _(message, path_args, bot, user):
#     if user.admin == True or user.super_admin == True:
#         event = Event.objects.filter(id = int(user.temp)).first()
#         if event is not None:
#             if message.text.isdigit():
#                 event.number_of_tickets = int(message.text)
#                 event.save()
#             elif 'неограничено' in message.text.lower():
#                 event.number_of_tickets = None
#             else:
#                 return await user.reply('❗️ Укажите количество билетов числом. Например: 100')
#             user.dialog = Account.Dialog.DEFAULT
#             user.save()
#             await user.reply(f'✅ Количество билетов успешно изменено на <b>{event.number_of_tickets}</b>', keyboard=IKM(inline_keyboard=[
#                 [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#                 [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#                 ]))


# @handler.callback(name = 'edit_event_date_of_event')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_DATE_OF_EVENT_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новую дату события для данного мероприятия в формате: 12.10.2020 15:00', keyboard=RKR())
 

# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_DATE_OF_EVENT_DIALOG)
# async def _(message, path_args, bot, user):
#     if user.admin == True or user.super_admin == True:
#         event = Event.objects.filter(id = int(user.temp)).first()
#         if event is not None:
#             try:
#                 date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
#                 assert date > datetime.now()
#             except ValueError:
#                 return await user.reply('❗️ Дата мероприятия должна быть в формате: 12.10.2020 15:00')
#             except:
#                 return await user.reply('❗️ Дата проведения мероприятия должна находиться в будущем')
#             event.date_of_event = date
#             event.save()
#             user.dialog = Account.Dialog.DEFAULT
#             user.save()
#             await user.reply(f'✅ Новая дата мероприятия успешно изменена на <b>{event.date_of_event}</b>', keyboard=IKM(inline_keyboard=[
#                 [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#                 [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#                 ]))


# @handler.callback(name = 'edit_event_finish_date')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             user.dialog = Account.Dialog.EDIT_EVENT_FINISH_DATE_DIALOG
#             user.temp = str(event.id)
#             user.save()
#             await callback.message.delete()
#             await user.reply('✏️ Отправьте новую дату окончания продажи билетов для данного мероприятия в формате: 12.10.2020 15:00',
#                 keyboard=RKM([['⏩ Пропустить']], one_time_keyboard=True, resize_keyboard=True))
 

# @handler.message(name='', dialog = Account.Dialog.EDIT_EVENT_FINISH_DATE_DIALOG, admin = True)
# async def _(message, path_args, bot, user):
#     event = Event.objects.filter(id = int(user.temp)).first()
#     if event is not None:
#         if 'пропустить' in message.text.lower():
#             event.finish_date = None
#         else:
#             try:
#                 date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
#                 assert date > datetime.now() and date.astimezone(timezone.utc) <= event.date_of_event
#             except ValueError:
#                 return await user.reply('❗️ Дата окончания покупки должна быть в формате: 12.10.2020 15:00')
#             except Exception as ex:
#                 print(ex)
#                 return await user.reply('❗️ Дата окончания покупки должна находиться в будущем и не должна быть больше даты окончания мероприятия')
#             event.finish_date = date
#             event.save()
#         user.dialog = Account.Dialog.DEFAULT
#         user.save()
#         result = 'начало мероприятия' if event.finish_date is None else event.finish_date.strftime('%d.%m.%Y %H:%M')
#         await user.reply(f'✅ Новая дата окончания продажи билетов мероприятия успешно изменена на <b>{result}</b>',keyboard=IKM(inline_keyboard=[
#             [IKB('✏️ Вернуться к редактированию', callback_data = f'admin_event {event.id}')],
#             [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#             ]))

# ##################################################################

# @handler.callback(name='delete_event')
# async def _(callback, path_args, bot, user):
#     if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
#         event = Event.objects.filter(id = path_args[1]).first()
#         if event is not None:
#             event.delete()
#             await callback.message.delete()
#             await user.reply(f'✅ Мероприятие было успешно <b>удалено</b>', keyboard=IKM(inline_keyboard=[
#                 [IKB('👀 Вернуться к общему списку', callback_data = f'admin_events')]
#                 ]))
 
# #############################################################################################################################################33


