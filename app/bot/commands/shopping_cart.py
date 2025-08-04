from app.bot import handler
from app.models import Account, Product, Category, Order, OrderItem, AboutCompany

from django.db.models import Sum
from django.db.models import Q

import pytz
from django.utils import timezone

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

from datetime import datetime


@handler.message(name='🧺 Корзина', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await shopping_cart(user)


async def shopping_cart(user):
    await user.reply("🕹 Выберите что хотите посмотреть: ", keyboard=IKM(inline_keyboard=[
        [IKB("🖥 Активные заказы", callback_data="active_order")],
        [IKB("💾 История заказов", callback_data="archive_order")]
    ]))


@handler.callback(name='archive_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    orders = Order.objects.filter(status=Order.STATUS_COMPLETED).all()

    if not orders:
        await user.reply('✖️ У вас еще ент завершенных заказов!')
    else:
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = timezone.now().astimezone(moscow_tz)

        await user.reply("🔚 Завершенные заказы:", keyboard=IKM(inline_keyboard=[
            [IKB(f'✔️ Заказ на {order.total_price}р. от {order.updated_at.astimezone(moscow_tz).strftime("%d.%m.%Y %H:%M")}', callback_data=f'archive_order_detail {order.id}')] for order in orders] + [
                [IKB('◀️ Назад', callback_data='back_shopping_cart')]
            ]))


@handler.callback(name='archive_order_detail', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.get(id=int(path_args[1]))
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = timezone.now().astimezone(moscow_tz)

    await user.reply(f'⚙️ Детальная информация по заказу:\n\n{order.items_name}\n💷 Итоговая сумма: {order.total_price} рублей\n📅 Дата оплаты: {order.updated_at.astimezone(moscow_tz).strftime("%d.%m.%Y %H:%M")}', keyboard=IKM(inline_keyboard=[
        [IKB('◀️ Назад', callback_data='archive_order')]
        ]))


@handler.callback(name='active_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.filter(Q(status=Order.STATUS_NEW, user=user) | Q(status=Order.STATUS_IN_PROGRESS, user=user)).first()

    if not order:
        await user.reply('В данный момент активных заказов нет!')
    else:
        user_order = OrderItem.objects.filter(buyer=user).all()

        await user.reply("🛍 Продукты в корзине:", keyboard=IKM(inline_keyboard=[
            [IKB(f'🖊 {order_item}', callback_data=f'update_order {order_item.id}')] for order_item in user_order] + [
                [IKB('💷 Оформить заказ', callback_data=f'create_an_order {order.id}')],
                [IKB('◀️ Назад', callback_data=f'back_shopping_cart')]
            ]))


@handler.callback(name='create_an_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.get(id=int(path_args[1]))
    order_items = OrderItem.objects.filter(order__id=order.id)
    total_price = order_items.aggregate(total=Sum('price'))['total']
    order.total_price = total_price
    order.status = Order.STATUS_IN_PROGRESS
    order.save()

    await user.reply(f"📲 Выберите способ получения:", keyboard=IKM(inline_keyboard=[
        [IKB('📦 Доставка почтой', callback_data=f'select_type_receiving {order.id} {Order.DELIVERY}')],
        [IKB('🧰 Самовывоз Тула', callback_data=f'select_type_receiving {order.id} {Order.RECEIVING_POINT}')],
        [IKB('◀️ Назад', callback_data=f'active_order')]
    ])) 


@handler.callback(name='select_type_receiving', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.filter(id=int(path_args[1])).first()
    delivery_text = ''

    if Order.DELIVERY == path_args[2]:
        order.receiving = Order.DELIVERY
        order.save()
        delivery_text = "\n\n❗️ Стоимость не учитывает доставку\nПо вопросам доставки обращайтесь к менеджеру!"
    elif Order.RECEIVING_POINT == path_args[2]:
        order.receiving = Order.RECEIVING_POINT
        order.save()

    await user.reply(f"💵 Стоимость заказа: {order.total_price} рублей\n🧰 Способ получения: {order.get_receiving_display()}{delivery_text}", keyboard=IKM(inline_keyboard=[
        [IKB('💷 Оплатить', callback_data=f'payment_for_the_order {order.id}')],
        [IKB('◀️ Назад', callback_data=f'create_an_order {order.id}')]
    ])) 


@handler.callback(name='payment_for_the_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.filter(id=int(path_args[1])).first()
    company = AboutCompany.objects.first()

    await user.reply(f"💳 Реквизиты для оплаты заказа: <code>{company.payment_details}</code>\n\n💷 Сумма заказа: {order.total_price} рублей\n🧰 Способ получения: {order.get_receiving_display()}", keyboard=IKM(inline_keyboard=[
        [IKB('✅ Оплатил', callback_data=f'successful_payment {path_args[1]}')],
        [IKB('❌ Отмена', callback_data=f'select_type_receiving {path_args[1]} {order.receiving}')]
    ]))


@handler.callback(name='successful_payment', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await user.reply("💻 Ваш заказ на проверке, ожидайте")
    manager = Account.objects.filter(username="maxmotinm").first()
    order = Order.objects.filter(id=int(path_args[1])).first()

    await manager.reply(f"➕ Поступил заказ №{order.id}\nОт пользователя {order.user.first_name} " +
        f"{order.user.last_name}\n@{order.user.username}\n\n💷 Сумма заказа: {order.total_price} рублей", keyboard=IKM(inline_keyboard=[
            [IKB('✅ Оплата поступила', callback_data=f'finaly_payment_order {path_args[1]} success {user.id}')],
            [IKB('❌ Деньги не пришли', callback_data=f'finaly_payment_order {path_args[1]} nonsuccess {user.id}')]
        ]))


@handler.callback(name='finaly_payment_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    order = Order.objects.filter(id=int(path_args[1])).first()
    company = AboutCompany.objects.first()
    buyer = Account.objects.filter(id=int(path_args[3])).first()
    
    if path_args[2] == "success":
        await user.reply(f"✅ Заказ подтвержден!\n👤 Покупатель: @{buyer.username}\n\n💴 Итоговая стоимость: {order.total_price} рублей")
        await buyer.return_the_keyboard(f"🥳 Заказ успешно оформлен, по всем вопросам о заказе пишите менеджеру\n\nНомер вашего заказа: {order.id}\nИтоговая стоимость: {order.total_price} рублей")
        order.status = Order.STATUS_COMPLETED
        
        order_items = OrderItem.objects.filter(buyer=buyer).all()
        print(order_items)
        order_item_objects = list(order_items)
        order_item_strings = [str(item) for item in order_item_objects]
        result_string = '\n'.join(order_item_strings)
        print(result_string)
        order.items_name = result_string
        order_items.delete()

        order.save()
    else:
        await buyer.reply(f"❌ К сожалению оплата не прошла:(\nПопробуйте еще раз\n\nРеквизиты для оплаты заказа: <code>{company.payment_details}</code>",
            keyboard=IKM(inline_keyboard=[
                [IKB('✅ Оплатил', callback_data=f'successful_payment {path_args[1]}')],
                [IKB('❌ Отмена', callback_data=f'create_an_order {path_args[1]}')]
            ]))


@handler.callback(name='update_order', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await user.reply("Выберите, что сделать с товаром: ", keyboard=IKM(inline_keyboard=[
        [IKB('🖊 Изменить количество', callback_data=f'change_the_order {path_args[1]} {"update"}')],
        [IKB('🗑 Удалить', callback_data=f'change_the_order {path_args[1]} {"delete"}')],
        [IKB('◀️ Назад', callback_data='active_order')]
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
