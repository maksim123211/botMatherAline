from aiogram import Bot, Dispatcher, executor, types
from app.models import Account
from app.bot import handler
import os, importlib, re
# import logging, sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TelegramBot:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'auth_token'}:
            raise Exception('Not enough arguments to initialize the bot')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.__bot = Bot(token=kwargs['auth_token'])
        self.__dp = Dispatcher(self.__bot)
        Account.TempData.bot = self.__bot
        self.read_handlers()
        self.create_listeners()
        executor.start_polling(self.__dp, skip_updates=True)

    def load_or_create(self, user_obj):
        return Account.objects.get_or_create(id=user_obj.id, defaults={'first_name': user_obj.first_name, 'last_name': user_obj.last_name, 'username': user_obj.username})[0]

    def create_listeners(self):
        @self.__dp.message_handler()
        async def _(message: types.Message):
            #print(message)
            processed_name = message.text.lower().strip()
            path_args = re.split(r'\s+', processed_name)
            user = self.load_or_create(message['from'])
            if (user.dialog != Account.Dialog.START and processed_name == '/start') or 'меню' in processed_name:    # Check user wants return to menu
                await user.return_menu()
            else:
                for command in handler.commands:
                    if ((not command.with_args and command.name in ['', processed_name]) or (command.with_args and command.name in ['', path_args[0]])) and command.dialog == user.dialog:
                        if command.admin and (not user.super_admin and not user.admin):
                            return
                        if not await command.handle(message, path_args, self.__bot, user):
                            await message.reply('❌ Произошла <b>системная</b> ошибка. Выйдите в меню и попробуйте <b>ещё раз</b>.', parse_mode='HTML')
                        break
                else:
                    await message.reply('⚠️ Неизвестная команда. Напишите мне <b>«Меню»</b> и воспользуйтесь кнопками', parse_mode='HTML')

        @self.__dp.callback_query_handler()
        async def _(call: types.CallbackQuery):
            path_args = re.split(r'\s+', call.data)
            user = self.load_or_create(call.from_user)
            for callback in handler.callbacks:
                if callback.name == path_args[0]:
                    if callback.admin and (not user.super_admin and not user.admin):
                        return
                    if not await callback.handle(call, path_args, self.__bot, user):
                        await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Возникла ошибка при обработке события', show_alert=True)
                    break
            else:
                await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Неизвестный запрос', show_alert=True)

    def read_handlers(self):
        for root, dirs, files in os.walk('app/bot/commands'):
            check_extension = filter(lambda x: x.endswith('.py'), files)
            for command in check_extension:
                path = os.path.join(root, command)
                spec = importlib.util.spec_from_file_location(command, os.path.abspath(path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
