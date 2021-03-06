import asyncio
import logging

from datetime import datetime, timedelta

import discord
import pytz
import requests
from discord import Colour
from discord.ext import commands
from goose3 import Goose

from api.models import Launch
from bot.app.repository.launches_repository import LaunchRepository
from bot.models import NewsNotificationChannel, NewsItem, LaunchNotificationRecord

logger = logging.getLogger('bot.discord')
daily_send_time = '12:00'  # time is in 24hr format
hourly_send_time = '00'  # time is in 24hr format


def stale_to_embed(stale):
    title = "Found %s stale launches..." % len(stale)
    color = Colour.orange()
    description = ""
    for launch in stale:
        description = description + "%s\n [Launch Library](https://launchlibrary.net/1.4/launch/%s) | [Admin](%s)\n\n" % (
            launch.name,
            launch.launch_library_id,
            launch.get_admin_url())
    embed = discord.Embed(type="rich", title=title,
                          description=description,
                          color=color)
    return embed


def get_news():
    response = requests.get(url='https://api.spaceflightnewsapi.net/articles?limit=5')
    if response.status_code == 200:
        for item in response.json():
            news, created = NewsItem.objects.get_or_create(id=item['_id'])
            if created:
                news.title = item['title']
                news.link = item['url']
                news.featured_image = item['featured_image']
                news.news_site = item['news_site_long']
                news.created_at = datetime.utcfromtimestamp(item['date_published']).replace(tzinfo=pytz.utc)
                news.read = False
                try:
                    g = Goose()
                    article = g.extract(url=news.link)
                    if article.meta_description is not None and article.meta_description is not "":
                        text = article.meta_description
                    elif article.cleaned_text is not None:
                        text = (article.cleaned_text[:300] + '...') if len(
                            article.cleaned_text) > 300 else article.cleaned_text
                    else:
                        text = None
                    news.description = text
                except Exception as e:
                    logger.error(e)
                logger.info("Added News (%s) - %s - %s" % (news.id, news.title, news.news_site))
                news.save()
    return


class SLNAdmin:
    bot = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='checkStale', pass_context=True, hidden=True)
    async def check_stale(self, context):
        """Checks for stale launches.

        Usage: ?checkStale

        Examples: ?checkStale
        """
        if "staff" in [y.name.lower() for y in context.message.author.roles]:
            await self.bot.send_message(context.message.channel, "Checking...")
            await self.check_daily()
        else:
            await self.bot.send_message(context.message.channel, "This is a staff only command.")

    async def check_daily(self):
        stale = self.check_for_orphaned_launches()
        await self.bot.send_message(self.bot.get_channel(id="484371128232706049"), "Checking for stale launches...")
        if len(stale) > 0:
            await self.bot.send_message(self.bot.get_channel(id="484371128232706049"), embed=stale_to_embed(stale))
        else:
            await self.bot.send_message(self.bot.get_channel(id="484371128232706049"), "No stale Launches found!")

    async def check_hourly(self):
        pass

    def check_for_orphaned_launches(self):
        logger.info('Task - Get Upcoming launches!')

        # Delete notification records from old launches.
        three_days_threshhold = datetime.today() - timedelta(days=3)
        notifications = LaunchNotificationRecord.objects.filter(launch__net__lte=three_days_threshhold)
        notifications.delete()

        # Check for stale launches.
        three_days_past = datetime.today() - timedelta(days=3)
        launches = Launch.objects.filter(last_updated__lte=three_days_past, launch_library=True)
        stale = []
        if len(launches) > 0:
            logger.info("Found stale launches - checking to see if they are deleted from Launch Library")
            repository = LaunchRepository()
            for launch in launches:
                logger.debug("Stale - %s" % launch.name)
                if repository.is_launch_deleted(launch.launch_library_id):
                    stale.append(launch)
                    logger.error("Delete this launch! - %s ID: %d" % (launch.name, launch.launch_library_id))
        return stale

    async def event_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            daily = datetime.strftime(datetime.now(), '%H:%M')
            hourly = datetime.strftime(datetime.now(), '%M')
            if daily == daily_send_time:
                await self.check_daily()
            if hourly == hourly_send_time:
                await self.check_hourly()
            await asyncio.sleep(60)


def setup(bot):
    admin_bot = SLNAdmin(bot)
    bot.add_cog(admin_bot)
    bot.loop.create_task(admin_bot.event_loop())
