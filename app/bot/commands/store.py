from app.bot import handler
from app.models import Account, Product, Category, Order, OrderItem

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


@handler.message(name='🏪 Магазин', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await store_menu(user)


async def store_menu(user):
    categories = Category.objects.all()

    if categories is not None:
        await user.reply('📔 Категории продукции:', keyboard=IKM(inline_keyboard=[
            [IKB('{}'.format(category.name),
                 callback_data=f'category_select {category.id}')] for category in categories
        ]))
    else:
        await user.reply('❌ В данный момент продукция отсутствует!')


@handler.callback(name='back_store', dialog=Account.Dialog.DEFAULT)
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await store_menu(user)


@handler.callback(name='category_select')
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    category = Category.objects.filter(id=path_args[1]).first()
    products = Product.objects.filter(category=category).all()
    if products:
        await user.reply(f'👜 Товары в категории {category.name}:', keyboard=IKM(inline_keyboard=[
            [IKB('{}'.format(product.name),
                 callback_data=f'product_select {product.id}')] for product in products] +
                [[IKB('◀️ Назад', callback_data='back_store')]]))
    else:
        await user.reply(f"❌ На данный момент товары в категории {category.name} отсутствуют",
                         keyboard=IKM(inline_keyboard=[[IKB('◀️ Назад', callback_data='back_store')]]))


@handler.callback(name="product_select")
async def _(callback, path_args, bot, user):
    product = Product.objects.filter(id=path_args[1]).first()
    await callback.message.delete()

    if product is not None:
        extension = product.image.name.split('.')[-1]
        if extension == 'mp4':
            await bot.send_video(
                chat_id=user.id,
                video=open(product.image.path, 'rb'),
                caption=f"{product.description}\n\nПорция по {product.weight} грамм\n💵 Цена за порцию {product.price} рублей",
                parse_mode='html',
                reply_markup=IKM(inline_keyboard=[
                    [IKB('💷 Добавить в корзину', callback_data='order {}'.format(product.id))],
                    [IKB('◀️ Назад', callback_data=f'category_select {product.category.id}')]
                ])
            )
        elif extension in ['jpeg', 'png', 'jpg']:
            await bot.send_photo(
                chat_id=user.id,
                photo=open(product.image.path, 'rb'),
                caption=f"{product.description}\n\nПорция по {product.weight} грамм\n💵 Цена за порцию {product.price} рублей",
                parse_mode='html',
                reply_markup=IKM(inline_keyboard=[
                    [IKB('💷 Добавить в корзину', callback_data='order {}'.format(product.id))],
                    [IKB('◀️ Назад', callback_data=f'category_select {product.category.id}')]
                ])
            )


@handler.callback(name='order')
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await user.reply("Выберите количество порций:", keyboard=IKM(inline_keyboard=[
        [IKB('{}'.format(count),
             callback_data=f'create_order {count} {path_args[1]}')] for count in range(1, 6)] +
        [[IKB('Свой вариант', callback_data=f'select_product_count {path_args[1]}')] +
            [IKB('◀️ Назад', callback_data=f'product_select {path_args[1]}')]]))


@handler.callback(name='select_product_count')
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await user.reply("Введите количество продукции с клавиатуры:")
    user.dialog = Account.Dialog.GET_COUNT_PRODUCTS
    user.temp = path_args[1]
    user.save()


@handler.message(name='', dialog=Account.Dialog.GET_COUNT_PRODUCTS)
async def _(message, path_args, bot, user):
    user.dialog = Account.Dialog.DEFAULT
    user.save()
    product_count = int(message.text)
    if product_count <= 0:
        await user.reply("❌ Вы ввели отрицательное число!\nДиапазон ввода от 1 до 1000\nВведите количество продукции:")
        user.dialog = Account.Dialog.GET_COUNT_PRODUCTS
        user.save()
    elif product_count > 1000:
        await user.reply("❌ Вы ввели слишком большое число!\nДиапазон ввода от 1 до 1000\nВведите количество продукции:")
        user.dialog = Account.Dialog.GET_COUNT_PRODUCTS
        user.save()
    else:
        path_args = ["", product_count, user.temp]
        user.temp = ''
        user.save()
        await create_and_update_order_with_count(path_args, bot, user)


@handler.callback(name='create_order')
async def _(callback, path_args, bot, user):
    await callback.message.delete()
    await create_and_update_order_with_count(path_args, bot, user)


async def create_and_update_order_with_count(path_args, bot, user):
    order = Order.objects.filter(status=Order.STATUS_NEW or Order.STATUS_IN_PROGRESS, user=user).first()
    part_of_the_order = OrderItem.objects.filter(id=int(path_args[2]), buyer=user).first()

    if part_of_the_order is not None:
        part_of_the_order.quantity = int(path_args[1])
        part_of_the_order.price = part_of_the_order.product.price * int(path_args[1])
        part_of_the_order.save()

        await user.reply(f"✅ Продукт: {part_of_the_order} успешно изменен!")
    else:
        product = Product.objects.filter(id=int(path_args[2])).first()
        if order is None:
            order = Order(
                user=user
            )
            order.save()

        order_item = OrderItem(
            product=product,
            order=order,
            buyer=user,
            quantity=int(path_args[1]),
            price=product.price * int(path_args[1]),
        )
        order_item.save()

        await user.return_the_keyboard(f"✅ Продукт: {order_item} успешно добавлен в корзину!")
