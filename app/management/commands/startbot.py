from django.core.management.base import BaseCommand
from django.conf import settings

from app.bot.app import TelegramBot


class Command(BaseCommand):
    help = 'Start Telegram bot'

    def handle(self, *args, **options):
        current_bot = TelegramBot(auth_token=settings.BOT_TOKEN)
        