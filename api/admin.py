# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import BaseInlineFormSet, ModelForm
from django.urls import reverse
from django.utils.html import escape

from api.filters.UpcomingFilter import DateListFilter, EventDateListFilter
from api.forms.admin_forms import LaunchForm, LandingForm, LauncherForm, PayloadForm, MissionForm, EventsForm, \
    OrbiterForm, AgencyForm, AstronautForm, SpacecraftFlightForm, SpacecraftForm, LauncherConfigForm, SpaceStationForm
from api.models import Mission, Rocket
from api.utils.utilities import admin_link, AdminBaseWithSelectRelated
from bot.utils.admin_utils import custom_titled_filter
from . import models


@admin.register(models.LauncherConfig)
class LauncherConfigAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">extension</i>'
    list_display = ('name', 'audited', 'variant', 'full_name', 'family', 'active', 'manufacturer',)
    list_filter = ('name', 'family', 'image_url', 'manufacturer__name', 'audited',)
    ordering = ('name', 'id')
    search_fields = ('name', 'manufacturer__name')
    # readonly_fields = ['launch_library_id']
    form = LauncherConfigForm


@admin.register(models.Launcher)
class LauncherAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">extension</i>'
    list_display = ('id', 'serial_number', 'flight_proven', 'status', 'launcher_config')
    list_filter = ('id', 'serial_number', 'flight_proven', 'status', 'launcher_config')
    ordering = ('id', 'serial_number', 'flight_proven', 'status')
    search_fields = ('serial_number', 'launcher_config__name', 'status', 'details')
    form = LauncherForm


@admin.register(models.Mission)
class MissionAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment</i>'
    list_display = ('id', 'name', 'mission_type', 'orbit')
    list_filter = ('id', 'name', 'mission_type', 'orbit')
    # readonly_fields = ['launch_library_id']
    ordering = ('id',)
    search_fields = ('name', 'description')
    form = MissionForm


@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display = ('short_name', 'featured', 'launchers', 'spacecraft', 'short_description')
    list_filter = ('name', 'featured',)
    ordering = ('name',)
    search_fields = ('name',)
    form = AgencyForm


@admin.register(models.Landing)
class LandingAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display = ('name', 'attempt', 'success', 'landing_location', 'landing_type')
    form = LandingForm

    def name(self, obj):
        try:
            if obj.firststage is not None:
                return u"Landing: %s" % obj.firststage
            elif obj.secondstage is not None:
                return u"Landing: %s" % obj.secondstage
            else:
                return u"(%d) Unassigned Landing" % obj.id
        except (models.Launch.DoesNotExist, models.FirstStage.DoesNotExist) as e:
            return u"(%d) Unassigned Landing" % obj.id


class InfoURLs(admin.TabularInline):
    model = models.InfoURLs
    verbose_name = "Information URL"
    verbose_name_plural = "Information URLs"


class VideoURLs(admin.TabularInline):
    model = models.VidURLs
    verbose_name = "Video URL"
    verbose_name_plural = "Videos URLs"


class FirstStageInlineFormset(BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        super(FirstStageInlineFormset, self).__init__(data, files, instance,
                                                      save_as_new, prefix, queryset, **kwargs)
        self.queryset = models.FirstStage.objects.filter(rocket=instance) \
            .select_related('rocket__launch', 'rocket', 'launcher', 'launcher__launcher_config') \
            .prefetch_related('rocket', 'rocket__launch', 'rocket__configuration', 'launcher__launcher_config',)


class FirstStageInline(admin.StackedInline):
    model = models.FirstStage
    fields = ('type', 'launcher')
    verbose_name = "Launcher Stage"
    verbose_name_plural = "Launcher Stages"
    formset = FirstStageInlineFormset
    show_change_link = True
    max_num = 3
    raw_id_fields = ('launcher',)

    def get_queryset(self, request):
        return super(FirstStageInline, self).get_queryset(request).select_related('rocket__launch', 'rocket') \
            .select_related('rocket__launch', 'rocket', 'launcher', 'launcher__launcher_config') \
            .prefetch_related('rocket', 'rocket__launch', 'rocket__configuration', 'launcher__launcher_config',)


class DockingEventInline(admin.StackedInline):
    model = models.DockingEvent
    verbose_name = "Docking Event"
    verbose_name_plural = "Docking Events"


class SpacecraftFlightInlineFormset(BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        super(SpacecraftFlightInlineFormset, self).__init__(data, files, instance,
                                                            save_as_new, prefix, queryset, **kwargs)
        self.queryset = models.SpacecraftFlight.objects.filter(rocket=instance) \
            .prefetch_related('docking_events',
                              'rocket__launch',
                              'spacecraft__spacecraft_config',
                              'spacecraft',
                              'rocket__launch__mission',
                              'rocket__spacecraftflight',
                              'rocket__spacecraftflight__spacecraft',
                              'rocket__spacecraftflight__launch_crew',
                              'rocket__spacecraftflight__landing_crew',
                              'rocket__spacecraftflight__onboard_crew',
                              'rocket__spacecraftflight__launch_crew__astronaut',
                              'rocket__spacecraftflight__landing_crew__astronaut',
                              'rocket__spacecraftflight__onboard_crew__astronaut',
                              'rocket__spacecraftflight__launch_crew__role',
                              'rocket__spacecraftflight__landing_crew__role',
                              'rocket__spacecraftflight__onboard_crew__role'
                              )


class SpacecraftFlightInline(admin.TabularInline):
    model = models.SpacecraftFlight
    fields = ('spacecraft', 'rocket', 'destination',)
    verbose_name = "Spacecraft Stage"
    verbose_name_plural = "Spacecraft Stage"
    formset = SpacecraftFlightInlineFormset
    show_change_link = True

    def get_queryset(self, request):
        qs = super(SpacecraftFlightInline, self).get_queryset(request)
        return qs.prefetch_related(
            'docking_events',
            'rocket__launch',
            'spacecraft__spacecraft_config',
            'spacecraft',
            'rocket__launch__mission',
            'rocket__spacecraftflight',
            'rocket__spacecraftflight__spacecraft',
            'rocket__spacecraftflight__launch_crew',
            'rocket__spacecraftflight__landing_crew',
            'rocket__spacecraftflight__onboard_crew',
            'rocket__spacecraftflight__launch_crew__astronaut',
            'rocket__spacecraftflight__landing_crew__astronaut',
            'rocket__spacecraftflight__onboard_crew__astronaut',
            'rocket__spacecraftflight__launch_crew__role',
            'rocket__spacecraftflight__landing_crew__role',
            'rocket__spacecraftflight__onboard_crew__role'
        )


class SpacecraftFlightInlineForSpacecraft(admin.StackedInline):
    model = models.SpacecraftFlight
    verbose_name = "Flight"
    verbose_name_plural = "Flights"
    max_num = 1


@admin.register(models.Rocket)
class RocketAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display = ('id', 'launch',)
    search_fields = ('id', 'launch__name',)

    inlines = [FirstStageInline, SpacecraftFlightInline]

    def get_queryset(self, request):
        return super(RocketAdmin, self).get_queryset(request) \
            .prefetch_related(
            'configuration__manufacturer', 'firststage',
            'secondstage', 'spacecraftflight',
            'spacecraftflight__launch_crew',
            'spacecraftflight__onboard_crew',
            'spacecraftflight__landing_crew',
        )


@admin.register(models.FirstStage)
class FirstStageAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display = ('id', 'landing', 'launcher', 'rocket')
    list_display_links = ['rocket', 'launcher']

    list_select_related = (
        'rocket',
        'launcher',
        'type',
    )

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['rocket'].queryset = Rocket.objects.select_related(
            'configuration').prefetch_related(
            'launch__mission', 'launch', 'configuration', 'spacecraftflight', 'firststage', ).all()
        context['adminform'].form.fields['launcher'].queryset = models.Launcher.objects \
            .select_related('launcher_config') \
            .prefetch_related('launcher_config', 'firststage', 'firststage__rocket__launch',
                              'launcher_config__rocket').all()
        context['adminform'].form.fields['landing'].queryset = models.Landing.objects \
            .prefetch_related('firststage').all()
        return super(FirstStageAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_queryset(self, request):
        return super(FirstStageAdmin, self).get_queryset(request).select_related('rocket__launch', 'rocket') \
            .prefetch_related('rocket', 'rocket__launch', )


@admin.register(models.SecondStage)
class SecondStageAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display = ('id', 'landing', 'launcher', 'rocket')


@admin.register(models.SpacecraftConfiguration)
class OrbiterConfigurationAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">public</i>'
    readonly_fields = ('id',)
    list_display = ('name', 'agency')
    list_filter = ('agency',)
    ordering = ('name',)
    form = OrbiterForm


@admin.register(models.Launch)
class LaunchAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">launch</i>'
    list_display = ('name', 'net', 'rocket', 'mission', 'orbit')
    list_filter = (DateListFilter, ('status__name', custom_titled_filter('Launch Status')),
                   ('rocket__configuration__manufacturer__name', custom_titled_filter('LSP Name')),
                   ('rocket__configuration__name', custom_titled_filter('Launch Configuration Name')))
    ordering = ('net',)
    search_fields = ('name', 'rocket__configuration__manufacturer__name', 'mission__description')
    # readonly_fields = ['slug', 'launch_library_id', 'launch_library']
    form = LaunchForm
    list_select_related = (
        'rocket', 'mission'
    )
    inlines = [InfoURLs, VideoURLs]

    def orbit(self, obj):
        if obj.mission is not None and obj.mission.orbit is not None and obj.mission.orbit.name:
            return obj.mission.orbit.name
        else:
            return None

    orbit.short_description = 'Orbit'

    def get_queryset(self, request):
        return super(LaunchAdmin, self).get_queryset(request).prefetch_related(
            'info_urls').prefetch_related('vid_urls').select_related('rocket').select_related(
            'mission').select_related('pad').select_related('pad__location').prefetch_related(
            'rocket__configuration').prefetch_related('rocket__configuration__manufacturer').prefetch_related(
            'mission__mission_type').prefetch_related('rocket__firststage').select_related(
            'rocket__configuration__manufacturer').prefetch_related('rocket__firststage').prefetch_related(
            'rocket__secondstage').prefetch_related('rocket__spacecraftflight').prefetch_related(
            'rocket__spacecraftflight__launch_crew').prefetch_related(
            'rocket__spacecraftflight__onboard_crew').prefetch_related(
            'rocket__spacecraftflight__landing_crew').prefetch_related(
            'mission__orbit').prefetch_related('rocket').prefetch_related('mission')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['rocket'].queryset = Rocket.objects.prefetch_related(
            'launch__mission').prefetch_related('launch').all()
        context['adminform'].form.fields['mission'].queryset = Mission.objects.prefetch_related(
            'launch__mission').prefetch_related('launch').all()
        return super(LaunchAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(models.Events)
class EventAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">event</i>'
    list_display = ('date', 'name', 'type')
    list_filter = (EventDateListFilter, 'name',)
    search_fields = ('name',)
    ordering = ('date',)
    raw_id_fields = ('expedition', 'spacestation', 'launch')
    form = EventsForm


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">place</i>'
    list_display = ('name', 'country_code')
    list_filter = ('name', 'country_code')
    # readonly_fields = ['launch_library_id']
    readonly_fields = ('id',)
    ordering = ('name',)


@admin.register(models.Pad)
class PadAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">dashboard</i>'
    list_display = ('name', 'location')
    list_filter = ('name', 'agency_id')
    # readonly_fields = ['launch_library_id']
    ordering = ('name',)


@admin.register(models.Payload)
class PayloadAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">dashboard</i>'
    list_display = ('name', 'mission')
    list_filter = ('name', 'mission')
    ordering = ('name',)
    form = PayloadForm


@admin.register(models.VidURLs)
class VidAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">video_library</i>'
    list_display = ('vid_url', 'launch')


@admin.register(models.InfoURLs)
class InfoAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">link</i>'
    list_display = ('info_url', 'launch')


@admin.register(models.Astronaut)
class AstronautsAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'status', 'agency')
    list_filter = ('nationality', 'status', 'agency')
    search_fields = ('name', 'agency__name')
    readonly_fields = ["slug"]
    form = AstronautForm


@admin.register(models.AstronautFlight)
class AstronautFlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'astronaut', 'role')
    search_fields = ('astronaut__name', 'role__role')
    list_filter = ('astronaut', 'role')


class ExpeditionInline(admin.StackedInline):
    model = models.Expedition
    verbose_name = "Expedition"
    verbose_name_plural = "Expeditions"


@admin.register(models.Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'space_station')
    list_filter = ('space_station', 'space_station__owners__name')
    search_fields = ('name', 'space_station__name', 'crew__astronaut__name', 'space_station__owners__name')


@admin.register(models.DockingEvent)
class DockingEventAdmin(admin.ModelAdmin):
    list_display = ('space_station', 'docked', 'flight_vehicle', 'docking_location')
    list_filter = ('space_station', 'docked', 'docking_location')


@admin.register(models.SpaceStation)
class SpaceStationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = SpaceStationForm


@admin.register(models.SpacecraftFlight)
class SpacecraftFlightAdmin(admin.ModelAdmin):
    list_display = ('spacecraft_name',)
    list_filter = ('spacecraft__spacecraft_config', 'spacecraft__status',
                   'rocket__configuration__manufacturer__name')
    search_fields = ('id', 'spacecraft__name', 'spacecraft__serial_number', 'landing_crew__astronaut__name', 'launch_crew__astronaut__name',
                     'onboard_crew__astronaut__name')
    inlines = [DockingEventInline, ]

    def spacecraft_name(self, obj):
        return obj.spacecraft.name + " | " + obj.rocket.launch.name

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['launch_crew'].queryset = models.AstronautFlight.objects.prefetch_related(
            'astronaut').prefetch_related('role').all()
        context['adminform'].form.fields['landing_crew'].queryset = models.AstronautFlight.objects.prefetch_related(
            'astronaut').prefetch_related('role').all()
        context['adminform'].form.fields['onboard_crew'].queryset = models.AstronautFlight.objects.prefetch_related(
            'astronaut').prefetch_related('role').all()
        context['adminform'].form.fields['rocket'].queryset = Rocket.objects.prefetch_related(
            'launch__mission', 'launch', 'configuration', 'spacecraftflight').all()
        context['adminform'].form.fields['spacecraft'].queryset = models.Spacecraft.objects.prefetch_related(
            'spacecraft_config', 'status', ).all()
        return super(SpacecraftFlightAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('launch_crew', 'rocket',)
        return qs


@admin.register(models.Spacecraft)
class SpacecraftAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'status',)
    list_filter = ('status', 'spacecraft_config',)
    form = SpacecraftForm
    search_fields = ('name', 'spacecraft_config__name', 'serial_number', 'description')

    # inlines = [SpacecraftFlightInlineForSpacecraft, ]

    def status(self, obj):
        return obj.status.name

    # def flights(self, obj):
    #     return '<a href="/admin/api/spacecraftflight/?spacecraft__spacecraft_config__id__exact=%d">%s Flights</a>' % (obj.spacecraft_config.id, obj.name)
    #
    # flights.allow_tags = True
