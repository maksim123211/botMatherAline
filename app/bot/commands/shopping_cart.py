from app.bot import handler
from app.models import Account, Product, Category, Order, OrderItem
from django.db.models import Sum

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


@handler.message(name='🧺 Корзина', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await shopping_cart(user)


async def shopping_cart(user):
    await user.reply("Выберите что хотите посмотреть: ", keyboard=IKM(inline_keyboard=[
        [IKB("Активные заказы", callback_data="active_order")],
        [IKB("История заказов", callback_data="archive_order")]
    ]))


@handler.callback(name='active_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    user_order = OrderItem.objects.filter(buyer=user).all()
    order = Order.objects.filter(status=Order.STATUS_NEW or Order.STATUS_IN_PROGRESS).first()
    if not user_order:
        await user.reply('В данный момент активных заказов нет!')
    else:
        await user.reply("🛍 Продукты в корзине:", keyboard=IKM(inline_keyboard=[
            [IKB(f'🖊 {order_item}', callback_data=f'update_order {order_item.id}')] for order_item in user_order] + [
                [IKB('💷 Оформить заказ', callback_data=f'create_an_order {order.id}')]
            ]))


@handler.callback(name='create_an_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order_items = OrderItem.objects.filter(order=int(path_args[1]))

    # Суммируем все поля price
    total_price = order_items.aggregate(total=Sum('price'))['total']

    # Выводим результат
    print(f"Общая сумма: {total_price}")

    await user.reply(f"Общая стоимость заказа: {total_price}")
    await user.reply("Выберите, что сделать с товаром: ", keyboard=IKM(inline_keyboard=[
        [IKB('🖊 Изменить количество', callback_data=f'change_the_order {path_args[1]} {"update"}')],
        [IKB('🗑 Удалить', callback_data=f'change_the_order {path_args[1]} {"delete"}')]
    ]))


@handler.callback(name='update_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await user.reply("Выберите, что сделать с товаром: ", keyboard=IKM(inline_keyboard=[
        [IKB('🖊 Изменить количество', callback_data=f'change_the_order {path_args[1]} {"update"}')],
        [IKB('🗑 Удалить', callback_data=f'change_the_order {path_args[1]} {"delete"}')]
    ]))


@handler.callback(name='change_the_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    if path_args[2] == "delete":
        order = OrderItem.objects.filter(id=int(path_args[1])).first()
        order.delete()
        await user.return_the_keyboard("✅ Продукт успешно удален из корзины!")
    elif path_args[2] == "update":
        await user.reply("Введите количество продукции с клавиатуры:")
        user.dialog = Account.Dialog.GET_COUNT_PRODUCTS
        user.temp = path_args[1]
        user.save()
    else:
        await user.return_the_keyboard("❌ Возникла непредвиденная ошибка!")


@handler.callback(name='back_shopping_cart', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await shopping_cart(user)
