from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB
from app.bot import handler
import ujson
import urllib.request
from app.models import Account
from datetime import datetime

# # @handler.callback(name='edit_project')
# # async def _(callback, path_args, bot, user):
# # 	if (user.admin == True or user.super_admin == True) and len(path_args) == 2 and path_args[1].isdigit():
# # 		project = Project.objects.filter(id = path_args[1]).first()
# # 		income = 'высокодоходный' if project.type == Project.Type.HIGH else ('среднедоходный' if project.type == Project.Type.MEDIUM else 'низкодоходный')
# # 		await callback.message.edit_text(f'💼 Название проекта: <b>{project.name}</b> ({income})\n\nОписание проекта: <b>{project.desc}</b>\n\nСсылка: <b>{project.link}</b>', parse_mode='HTML', reply_markup=IKM(inline_keyboard=[
# # 				[IKB('⭐️ Изменить название', callback_data=f'edit_project_name {project.id}')],
# # 				[IKB('✏️ Изменить описание', callback_data=f'edit_project_desc {project.id}')],
# # 				[IKB('🔗 Изменить ссылку', callback_data=f'edit_project_link {project.id}')],
# # 				[IKB('💵 Изменить доходность', callback_data=f'edit_project_income {project.id}')],
# # 				[IKB('🗑 Удалить', callback_data=f'delete_project {project.id}')]
# # 			]))
 
 
# @handler.callback(name='edit_project_name', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		project = Project.objects.filter(id = path_args[1]).first()
# 		if project is not None:
# 			user.dialog = Account.Dialog.EDIT_PROJECT_NAME_DIALOG
# 			user.temp = str(project.id)
# 			user.save()
# 			await callback.message.edit_text('✏️ Отправьте новое название для данного проекта')
 
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_PROJECT_NAME_DIALOG, admin=True)
# async def _(message, path_args, bot, user):
# 	project = Project.objects.filter(id=user.temp).first()
# 	if project is not None:
# 		project.name = message.text
# 		project.save()
# 		user.dialog = Account.Dialog.DEFAULT
# 		user.save()
# 		await user.reply(f'✅ Название проекта успешно изменено на <b>{project.name}</b>', 
# 			keyboard = IKM(inline_keyboard = [
# 				[IKB('Вернуться к списку', callback_data='admin_projects')],
# 				[IKB('Вернуться к редактированию', callback_data=f'admin_project {project.id}')]
# 			]))
 
 
# @handler.callback(name='edit_project_desc', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		project = Project.objects.filter(id=path_args[1]).first()
# 		if project is not None:
# 			user.dialog = Account.Dialog.EDIT_PROJECT_DESC_DIALOG
# 			user.temp = str(project.id)
# 			user.save()
# 			await callback.message.edit_text('✏️ Отправьте новое описание для данного проекта')
 
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_PROJECT_DESC_DIALOG, admin=True)
# async def _(message, path_args, bot, user):
# 	project = Project.objects.filter(id=user.temp).first()
# 	if project is not None:
# 		project.desc = message.text
# 		project.save()
# 		user.dialog = Account.Dialog.DEFAULT
# 		user.save()
# 		await user.reply(f'✅ Описание проекта успешно изменено на\n\n<b>{project.desc}</b>', 
# 			keyboard = IKM(inline_keyboard = [
# 				[IKB('Вернуться к списку', callback_data='admin_projects')],
# 				[IKB('Вернуться к редактированию', callback_data=f'admin_project {project.id}')]
# 			]))
 
 
# @handler.callback(name='edit_project_link', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		project = Project.objects.filter(id=path_args[1]).first()
# 		if project is not None:
# 			user.dialog = Account.Dialog.EDIT_PROJECT_LINK_DIALOG
# 			user.temp = str(project.id)
# 			user.save()
# 			await callback.message.edit_text('✏️ Отправьте новую ссылку для данного проекта')
 
 
# @handler.message(name='', dialog = Account.Dialog.EDIT_PROJECT_LINK_DIALOG, admin=True)
# async def _(message, path_args, bot, user):
# 	project = Project.objects.filter(id=user.temp).first()
# 	if project is not None and urllib.request.urlopen(message.text):
# 		project.link = message.text
# 		project.save()
# 		user.dialog = Account.Dialog.DEFAULT
# 		user.save()
# 		await user.reply(f'✅ Ссылка проекта успешно изменена на <b>{project.link}</b>', 
# 			keyboard = IKM(inline_keyboard = [
# 				[IKB('Вернуться к списку', callback_data='admin_projects')],
# 				[IKB('Вернуться к редактированию', callback_data=f'admin_project {project.id}')]
# 			]))
# 	else:
# 		await user.reply('Ваша ссылка недействительна, повторите попытку')

 
# @handler.callback(name='edit_project_income', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		project = Project.objects.filter(id=path_args[1]).first()
# 		if project is not None:
# 			user.temp = str(project.id)
# 			user.save()
# 			await callback.message.edit_text('✏️ С помощью кнопок выберите новую доходность для данного проекта', reply_markup=IKM(inline_keyboard=[
# 					[IKB('Высокодоходный', callback_data=f'set_project_income {Project.Type.HIGH} {project.id}')],
# 					[IKB('Среднедоходный', callback_data=f'set_project_income {Project.Type.MEDIUM} {project.id}')],
# 					[IKB('Низкодоходный', callback_data=f'set_project_income {Project.Type.LOW} {project.id}')]
# 				]))
 
 
# @handler.callback(name='set_project_income', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 3 and path_args[2].isdigit():
# 		project = Project.objects.filter(id=path_args[2]).first()
# 		if project is not None:
# 			income = 'высокодоходный' if path_args[1] == Project.Type.HIGH else ('среднедоходный' if path_args[1] == Project.Type.MEDIUM else 'низкодоходный')
# 			project.type = path_args[1]
# 			project.save()
# 			await callback.message.edit_text(f'✅ Доходность проекта изменена на <b>{income}</b>', parse_mode='HTML', 
# 				reply_markup = IKM(inline_keyboard = [
# 					[IKB('Вернуться к списку', callback_data='admin_projects')],
# 					[IKB('Вернуться к редактированию', callback_data=f'admin_project {project.id}')]
# 				]))
 
 
# @handler.callback(name='delete_project', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2 and path_args[1].isdigit():
# 		project = Project.objects.filter(id=path_args[1]).first()
# 		if project is not None:
# 			project.delete()
# 			await callback.message.edit_text(f'✅ Проект был успешно <b>удалён</b>', parse_mode='HTML', 
# 				reply_markup = IKM(inline_keyboard = [[IKB('Вернуться к просмотру', callback_data='admin_projects')]]))
 
# #############################################################################################################################################33

# @handler.callback(name='add_project', admin=True)
# async def _(callback, path_args, bot, user):
# 	user.dialog = Account.Dialog.CREATE_PROJECT_NAME
# 	user.save()
# 	await user.reply('⭐️ Отправьте <b>название</b> для нового проекта, который вы хотите добавить в систему')
 
 
# @handler.message(name='', dialog = Account.Dialog.CREATE_PROJECT_NAME, admin=True)
# async def _(message, path_args, bot, user):
# 	user.temp = ujson.dumps({'name': message.text})
# 	user.dialog = Account.Dialog.CREATE_PROJECT_DESC
# 	user.save()
# 	await user.reply('✏️ Задайте <b>описание</b> для нового проекта, добавляемого в систему')
 
 
# @handler.message(name='', dialog = Account.Dialog.CREATE_PROJECT_DESC, admin=True)
# async def _(message, path_args, bot, user):
# 	user.temp = ujson.loads(user.temp)
# 	user.temp['desc'] = message.text
# 	user.temp = ujson.dumps(user.temp)
# 	user.dialog = Account.Dialog.CREATE_PROJECT_LINK
# 	user.save()
# 	await user.reply('🔗 Задайте <b>ссылку</b> для нового проекта')

 
# @handler.message(name='', dialog = Account.Dialog.CREATE_PROJECT_LINK, admin=True)
# async def _(message, path_args, bot, user):
# 	if urllib.request.urlopen(message.text):
# 		user.temp = ujson.loads(user.temp)
# 		user.temp['link'] = message.text
# 		user.temp = ujson.dumps(user.temp)
# 		user.dialog = Account.Dialog.DEFAULT
# 		user.save()
# 		await user.reply('💵 С помощью кнопок выберите подходящую <b>категорию доходности</b> для создаваемого проекта', keyboard = IKM(inline_keyboard=[
# 			[IKB('Высокорисковые', callback_data=f'create_project_income {Project.Type.HIGH}')],
# 			[IKB('Среднерисковые', callback_data=f'create_project_income {Project.Type.MEDIUM}')],
# 			[IKB('Низкорисковые', callback_data=f'create_project_income {Project.Type.LOW}')]
# 		]))
 
 
# @handler.callback(name='create_project_income', admin=True)
# async def _(callback, path_args, bot, user):
# 	if len(path_args) == 2:
# 		#income = 'высокодоходный' if path_args[1] == Project.Type.HIGH else ('среднедоходный' if path_args[1] == Project.Type.MEDIUM else 'низкодоходный')
# 		data = ujson.loads(user.temp)
# 		Project.objects.create(name = data['name'], desc = data['desc'], link = data['link'], type = path_args[1])
# 		await user.reply('✅ Проект успешно <b>создан!</b> Вы сможете просмотреть, отредактировать или удалить его используя вашу панель администратора.',
# 			keyboard = IKM(inline_keyboard = [[IKB('Вернуться к просмотру', callback_data='admin_projects')]]))
		
