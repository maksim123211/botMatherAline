from app.bot import handler
from app.models import Account, AboutCompany

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


@handler.message(name='👥 О нас', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await about_company(user, bot)


async def about_company(user, bot):
    company_info = AboutCompany.objects.first()

    if company_info.image is not None:
        await sender_with_photo(user, bot, company_info)
    else:
        await user.reply(company_info.description, keyboard=IKM(inline_keyboard=[
            [IKB('👩‍💻 Связь с менеджером', url=company_info.manager)]
        ]))


async def sender_with_photo(user, bot, company_info):
    if company_info is not None:
        extension = company_info.image.name.split('.')[-1]
        if extension == 'mp4':
            await bot.send_video(
                chat_id=user.id,
                video=open(company_info.image.path, 'rb'),
                caption=company_info.description,
                parse_mode='html',
                reply_markup=IKM(inline_keyboard=[
                    [IKB('👩‍💻 Связь с менеджером', url=company_info.manager)]
                ])
            )
        elif extension in ['jpeg', 'png', 'jpg']:
            await bot.send_photo(
                chat_id=user.id,
                photo=open(company_info.image.path, 'rb'),
                caption=company_info.description,
                parse_mode='html',
                reply_markup=IKM(inline_keyboard=[
                    [IKB('👩‍💻 Связь с менеджером', url=company_info.manager)]
                ])
            )
