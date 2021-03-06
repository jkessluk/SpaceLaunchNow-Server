from django.core.management import BaseCommand
from celery.utils.log import get_task_logger

from bot.app.notifications.news_notification_handler import NewsNotificationHandler
from bot.app.notifications.notification_handler import NotificationHandler
from bot.libraries.launchlibrarysdk import LaunchLibrarySDK
from bot.models import LaunchNotificationRecord, NewsItem
from bot.utils.deserializer import launch_json_to_model

logger = get_task_logger('bot')

TAG = 'Notification Server'


class Command(BaseCommand):
    help = 'Run Notifications manually.'

    def add_arguments(self, parser):
        parser.add_argument('-version', dest="version", type=str)

    def handle(self, *args, **options):
        logger.info('Running Notifications...')
        notification = NewsNotificationHandler()
        article = NewsItem.objects.filter(created_at__isnull=False).latest('created_at')
        notification.send_notification(article)

