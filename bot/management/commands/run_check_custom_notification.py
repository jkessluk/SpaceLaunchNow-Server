import datetime

import pytz
from django.core.management import BaseCommand
from celery.utils.log import get_task_logger

from api.models import Events
from bot.app.events.notification_handler import EventNotificationHandler
from bot.app.events.social_handler import SocialHandler
from bot.app.notifications.launch_event_tracker import LaunchEventTracker

logger = get_task_logger('bot.events')

TAG = 'Digest Server'


class Command(BaseCommand):
    help = 'Run check custom notifications manually.'

    def handle(self, *args, **options):
        logger.info('Check Custom notifications.')
        tracker = LaunchEventTracker()
        tracker.check_custom()
