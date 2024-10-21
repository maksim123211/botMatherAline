from app.bot import handler
from app.models import Account


@handler.message(name='/start', dialog=Account.Dialog.START, with_args=True)
async def _(message, path_args, bot, user):
	await user.return_menu()
