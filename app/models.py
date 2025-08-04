from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class Account(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = _("Пользователи")

    class TempData:
        bot = None

    class Dialog:
        START = 'start'
        DEFAULT = 'default'
        GET_COUNT_PRODUCTS = 'get_count_products'

    first_name = models.TextField(verbose_name='Имя')
    last_name = models.TextField(default='', null=True, blank=True, verbose_name='Фамилия')
    username = models.TextField(default=None, null=True, blank=True, verbose_name='Имя пользователя в телеграмм')
    dialog = models.TextField(default=Dialog.START)
    temp = models.TextField(default='', null=True, blank=True)

    async def reply(self, text, **kwargs):
        processed_text = '\n'.join(text) if isinstance(text, list) else text
        return await self.TempData.bot.send_message(self.id, processed_text % kwargs[
            'concate'] if 'concate' in kwargs else processed_text, parse_mode='HTML',
                                                    reply_markup=(kwargs['keyboard'] if 'keyboard' in kwargs else None))

    async def return_menu(self, text=f'👋 Добро пожаловать в магазин чая!', **kwargs):
        self.dialog = self.Dialog.DEFAULT
        self.save()
        await self.reply(f'👋 Добро пожаловать, {self.first_name}!', keyboard=RKM([
            [KB('🏪 Магазин'), KB('🧺 Корзина')],
            [KB('👥 О нас')]],
            resize_keyboard=True), **kwargs)

    async def return_the_keyboard(self, text):
        self.dialog = self.Dialog.DEFAULT
        self.save()
        await self.reply(text, keyboard=RKM([
            [KB('🏪 Магазин'), KB('🧺 Корзина')],
            [KB('👥 О нас')]],
            resize_keyboard=True))

    def __str__(self):
        return f'{self.first_name} {self.last_name if self.last_name is not None else ""}'


class Category(models.Model):
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    name = models.TextField(max_length=255, blank=False, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    name = models.TextField(verbose_name='Название товара', blank=False)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name="Цена за порцию", blank=False, max_digits=10, decimal_places=2)
    weight = models.IntegerField(verbose_name="Порция в граммах", blank=False)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, default=None, null=True, verbose_name='Фото товара')
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE, verbose_name="Категория товара")

    def __str__(self):
        return self.name


class AboutCompany(models.Model):
    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"

    description = models.TextField(verbose_name='Описание', blank=False)
    manager = models.TextField(verbose_name="Ссылка менеджера", blank=False)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, default=None, null=True, blank=False, verbose_name='Фото организации')
    receiving_address = models.TextField(verbose_name='Адрес самовывоза', blank=True)
    payment_details = models.TextField(verbose_name='Реквизиты для оплаты заказа', blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, _('Новый заказ')),
        (STATUS_IN_PROGRESS, _('В процессе')),
        (STATUS_COMPLETED, _('Оплачен')),
    )

    RECEIVING_POINT = 'receiving_point'
    DELIVERY = 'delivery'

    TYPE_RECEIVING = (
        (RECEIVING_POINT, _('Самовывоз')),
        (DELIVERY, _('Доставка')),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('Покупатель'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name=_('Статус заказа'))
    receiving = models.CharField(max_length=30, choices=TYPE_RECEIVING, default=RECEIVING_POINT, verbose_name=_('Способ получения'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Полная стоимость заказа', default=0)
    items_name = models.TextField(verbose_name='Название продуктов заказе', blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата последнего обновления'))


class OrderItem(models.Model):
    class Meta:
        verbose_name = "Составляющие заказов"
        verbose_name_plural = "Составляющие заказов"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items', verbose_name=_('Заказ'))
    buyer = models.ForeignKey(Account, on_delete=models.DO_NOTHING, verbose_name=_('Покупатель'))
    quantity = models.IntegerField(default=1, verbose_name='Количество продуктов')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
