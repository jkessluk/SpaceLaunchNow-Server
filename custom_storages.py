from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):

    location = settings.STATICFILES_LOCATION


class LogoStorage(S3Boto3Storage):

    location = settings.LOGO_LOCATION
    file_overwrite = True


class AgencyImageStorage(S3Boto3Storage):

    location = settings.AGENCY_IMAGE_LOCATION
    file_overwrite = True


class AgencyNationStorage(S3Boto3Storage):

    location = settings.AGENCY_NATION_LOCATION
    file_overwrite = True


class OrbiterImageStorage(S3Boto3Storage):

    location = settings.ORBITER_IMAGE_LOCATION
    file_overwrite = True


class LauncherImageStorage(S3Boto3Storage):

    location = settings.LAUNCHER_IMAGE_LOCATION
    file_overwrite = True


class EventImageStorage(S3Boto3Storage):

    location = settings.EVENT_IMAGE_LOCATION
    file_overwrite = True
