import datetime
import os
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from django.db import models

from custom_storages import AppImageStorage
from spacelaunchnow.base_models import SingletonModel


def image_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    name = "%s%s" % ("navigation_drawer_default", file_extension)
    return name


def language_image_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    clean_name = quote(quote(instance.name.encode('utf8')), '')
    clean_name = "%s_language_%s" % (clean_name.lower(), datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    name = "%s%s" % (str(clean_name), file_extension)
    return name


def profile_image_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    clean_name = quote(quote(instance.name.encode('utf8')), '')
    clean_name = "%s_profile_%s" % (clean_name.lower(), datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    name = "%s%s" % (str(clean_name), file_extension)
    return name


class AppConfig(SingletonModel):
    navigation_drawer_image = models.FileField(storage=AppImageStorage(), default=None, null=True, blank=True,
                                               upload_to=image_path)

    def __str__(self):
        return "Space Launch Now - Android App Config"

    def __unicode__(self):
        return u"Space Launch Now - Android App Config"

    class Meta:
        verbose_name = 'Android App Config'
        verbose_name_plural = 'Android App Config'


class Nationality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    flag = models.FileField(storage=AppImageStorage(), upload_to=language_image_path)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Nationality'
        verbose_name_plural = 'Nationalities'


class Translator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200, null=True, blank=True,)
    nationality = models.ForeignKey(Nationality, related_name='translator', null=True, blank=True,
                                    on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Translator'
        verbose_name_plural = 'Translators'


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True,)
    bio = models.CharField(max_length=2048, null=True, blank=True,)
    link = models.CharField(max_length=200, null=True, blank=True,)
    profile = models.FileField(storage=AppImageStorage(), upload_to=profile_image_path)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'


