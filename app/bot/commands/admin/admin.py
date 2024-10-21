from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot import handler
from app.models import Account
from datetime import datetime
import json


# @handler.message(name='администрирование', dialog=Account.Dialog.DEFAULT, admin=True)
# async def _(message, path_args, bot, user):
#     await user.reply(f'Это ваш личный кабинет администратора', keyboard=IKM(inline_keyboard=[
#         [IKB('📖 Мероприятия', callback_data = 'admin_events')],
#         [IKB('Проекты', callback_data = 'admin_projects')],
#         [IKB('Добавить администратора', callback_data = 'add_admin')] if user.super_admin == True else [],
#         [IKB('Удалить администратора', callback_data = 'delete_admin')] if user.super_admin == True else []]))

# @handler.callback(name='main_admin_menu', admin=True)
# async def _(callback, path_args, bot, user):
# 	await callback.message.edit_text(f'Это ваш личный кабинет администратора', reply_markup=IKM(inline_keyboard=[
#         [IKB('📖 Мероприятия', callback_data = 'admin_events')],
#         [IKB('Проекты', callback_data = 'admin_projects')],
#         [IKB('Добавить администратора', callback_data = 'add_admin')] if user.super_admin == True else [],
#         [IKB('Удалить администратора', callback_data = 'delete_admin')] if user.super_admin == True else []]))


# @handler.callback(name='admin_events', admin=True)
# async def _(callback, path_args, bot, user):
# 	await callback.message.edit_text('📖 Список мероприятий (<i>символом 🔸 обозначены актуальные мероприятия</i>):', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# 			[IKB('%s%s' % ('🔸 ' if event.is_relevant else '', event.title), callback_data=f'admin_event {event.id}')] for event in Event.objects.all().order_by('-date_of_event')
# 		] + [
# 			[IKB('➕ Добавить новое', callback_data='add_event')],
# 			[IKB('◀️ Назад', callback_data='main_admin_menu')]
# 		]))


# @handler.callback(name='admin_projects', admin=True)
# async def _(callback, path_args, bot, user):
#     await callback.message.edit_text('📖 Список проектов:', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# 			[IKB(f'{project.name}', callback_data=f'admin_project {project.id}')] for project in Project.objects.all()
# 		] + [
# 			[IKB('➕ Добавить новое', callback_data='add_project')],
# 			[IKB('◀️ Назад', callback_data='main_admin_menu')]
# 		]))

# #########################################################################################

# @handler.callback(name='admin_project', admin=True)
# async def _(callback, path_args, bot, user):
#     if len(path_args) == 2 and path_args[1].isdigit():
#         project = Project.objects.filter(id = path_args[1]).first()
#         if project is not None:
# 	        income = 'высокодоходный' if project.type == Project.Type.HIGH else ('среднедоходный' if project.type == Project.Type.MEDIUM else 'низкодоходный')
# 	        await callback.message.edit_text(f'💼 Название проекта: <b>{project.name}</b> ({income})\n\nОписание проекта: <b>{project.desc}</b>\n\nСсылка: <a>{project.link}</a>', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# 	                [IKB('⭐️ Изменить название', callback_data=f'edit_project_name {project.id}')],
# 					[IKB('✏️ Изменить описание', callback_data=f'edit_project_desc {project.id}')],
# 					[IKB('🔗 Изменить ссылку', callback_data=f'edit_project_link {project.id}')],
# 					[IKB('💵 Изменить доходность', callback_data=f'edit_project_income {project.id}')],
# 					[IKB('🗑 Удалить', callback_data=f'delete_project {project.id}')],
# 					[IKB('◀️ Назад', callback_data='admin_projects')]
# 	            ]))


# ##########################################################################################################
# @handler.callback(name='admin_event', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		event = Event.objects.filter(id=path_args[1]).first()
# 		if event is not None:
# 			await callback.message.edit_text(f'📖 Мероприятие <b>«{event.title}»</b>\n\n{event.desc}', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# 					[IKB('Изменить название', callback_data=f'edit_event_title {event.id}')],
# 					[IKB('Изменить описание', callback_data=f'edit_event_desc {event.id}')],
# 					[IKB('Дата проведения: %s' % event.date_of_event.strftime('%d.%m.%Y %H:%M'), callback_data=f'edit_event_date_of_event {event.id}')],
# 					[IKB('Место проведения: %s' % event.place, callback_data=f'edit_event_place {event.id}')],
# 					[IKB('Цена: %s руб.' % event.cost, callback_data=f'edit_event_cost {event.id}')],
# 					[IKB('Кол-во билетов: %s' % ('неограничено' if event.number_of_tickets is None else event.number_of_tickets), callback_data=f'edit_event_number_of_tickets {event.id}')],
# 					[IKB('Покупка до: %s' % (event.finish_date.strftime('%d.%m.%Y %H:%M') if event.finish_date is not None else 'не задано'), callback_data=f'edit_event_finish_date {event.id}')],
# 					[IKB('Удалить мероприятие', callback_data=f'delete_event {event.id}')],
# 					[IKB('◀️ Назад', callback_data='admin_events')]
# 				]))

# #######################################################################################################

# @handler.message(name='/id', admin=True)
# async def _(message, path_args, bot, user):
# 	await user.reply(f'Чтобы стать администратором вам необходимо отправить этот id: <b>{user.id}</b> супер-администратору, он вас добавит\nПосле добавления напишите боту <b>меню</b> и у вас будет расширенная панель управления')


# @handler.callback(name='add_admin', admin=True)
# async def _(callback, path_args, bot, user):
# 	if user.super_admin:
# 		await user.reply('Для того, чтобы добавить администратора вам необходимо попросить человека, которого вы хотите добавить написать боту\
# 			<b>/id</b>, после получения id нажмите на кнопку <b>Добавить</b> под этим сообщением, далее Вам придут дальнейшие инструкции',\
# 			keyboard = IKM(inline_keyboard = [[IKB('Добавить', callback_data = f'add_admin_get_id')]]))


# @handler.callback(name='add_admin_get_id', admin=True)
# async def _(callback, path_args, bot, user):
# 	if user.super_admin:
# 		user.dialog = Account.Dialog.ADD_ADMIN_GET_ID
# 		await user.reply('Введите <b>/id</b>, который вам отправил человек')


# @handler.message(name='', dialog=Account.Dialog.ADD_ADMIN_GET_ID, admin=True)
# async def _(message, path_args, bot, user):
# 	if message.text.isdigit() and user.super_admin:
# 		new_admin = Account.objects.filter(id = message.text).first()
# 		new_admin.admin = True
# 		new_admin.save()
# 		await user.reply(f'Администратор: {new_admin.first_name} с id: {new_admin.id} успешно добавлен')


# @handler.callback(name='delete_admin', admin=True)
# async def _(callback, path_args, bot, user):
# 	if user.super_admin:
# 		user.dialog = Account.Dialog.DELETE_ADMIN_GET_ID
# 		user.save()
# 		await user.reply('Для того, чтобы человек потерял права пользователя введите его <b>/id</b>')


# @handler.message(name='', dialog=Account.Dialog.DELETE_ADMIN_GET_ID, admin=True)
# async def _(message, path_args, bot, user):
# 	if user.super_admin and message.text.isdigit():
# 		last_admin = Account.objects.filter(id=message.text).first()
# 		last_admin.admin = False
# 		last_admin.save()
# 		await user.return_menu(f'Администратор: {last_admin.first_name} с id: {last_admin.id} успешно <b>удалён</b>')
