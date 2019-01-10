from drf_queryfields import QueryFieldsMixin

from api.models import *
from rest_framework import serializers


class SpaceStationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceStationStatus
        fields = ('id', 'name',)


class AgencyListSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'url', 'name', 'abbrev',)


class LaunchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchStatus
        fields = ('id', 'name',)


class AstronautStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronautStatus
        fields = ('id', 'name',)


class AstronautSerializer(serializers.HyperlinkedModelSerializer):
    status = AstronautStatusSerializer(read_only=True)
    agency = serializers.StringRelatedField(read_only=True, source='agency.name')

    class Meta:
        model = Astronauts
        fields = ('id', 'url', 'name', 'status', 'agency', 'profile_image')


class AgencySerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    parent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Agency
        fields = ('id', 'url', 'name', 'featured', 'type', 'country_code', 'abbrev', 'description', 'administrator',
                  'founding_year', 'launchers', 'spacecraft', 'parent',)


class AgencySerializerMini(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'url', 'name', 'type')


class SpacecraftConfigurationDetailSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    agency = AgencySerializerMini(read_only=True, source="launch_agency")

    class Meta:
        model = SpacecraftConfiguration
        fields = ('id', 'url', 'name', 'agency', 'in_use', 'capability', 'history', 'details', 'maiden_flight',
                  'height', 'diameter', 'human_rated', 'crew_capacity', 'payload_capacity', 'flight_life',
                  'image_url', 'nation_url', 'wiki_link', 'info_link')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'country_code',)


class PadSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Pad
        fields = ('id', 'agency_id', 'name', 'info_url', 'wiki_url', 'map_url', 'latitude', 'longitude', 'location')


class LocationSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name',)


class PadSerializerMini(serializers.ModelSerializer):
    location = LocationSerializerMini(many=False)

    class Meta:
        model = Pad
        fields = ('id', 'name', 'location')


class RocketConfigurationSerializerMini(serializers.ModelSerializer):
    launch_service_provider = AgencySerializerMini(many=False, source='launch_agency')

    class Meta:
        model = LauncherConfig
        fields = ('id', 'url', 'name', 'full_name', 'launch_service_provider', 'image_url')


class RocketSerializerMini(serializers.ModelSerializer):
    configuration = RocketConfigurationSerializerMini(many=False)

    class Meta:
        model = Rocket
        fields = ('id', 'configuration',)


class LandingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingType
        fields = ('name', 'abbrev', 'description',)


class LandingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingLocation
        fields = ('name', 'abbrev', 'description',)


class MissionSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(many=False, source='mission_type')
    orbit = serializers.StringRelatedField(many=False)
    orbit_abbrev = serializers.StringRelatedField(many=False, source='orbit.abbrev')

    class Meta:
        model = Mission
        fields = ('id', 'launch_library_id', 'name', 'description', 'type', 'orbit', 'orbit_abbrev')


class MissionSerializerMini(serializers.ModelSerializer):
    type = serializers.StringRelatedField(many=False, source='mission_type')

    class Meta:
        model = Mission
        fields = ('id', 'launch_library_id', 'name', 'type')


class AstronautDetailedSerializerNoFlights(serializers.HyperlinkedModelSerializer):
    status = AstronautStatusSerializer(read_only=True)
    agency = AgencySerializerMini(read_only=True, many=False)

    class Meta:
        model = Astronauts
        # fields = ('name',)
        fields = ('id', 'url', 'name', 'status', 'agency', 'date_of_birth', 'date_of_death', 'nationality',
                  'twitter', 'instagram', 'bio', 'profile_image', 'wiki',)


class AstronautFlightSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True, source='role.role')
    astronaut = AstronautDetailedSerializerNoFlights(read_only=True, many=False)

    class Meta:
        model = AstronautFlight
        fields = ('role', 'astronaut')


class SpacecraftDetailedNoFlightsSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.StringRelatedField(source='status.name', read_only=True, many=False)
    spacecraft_config = SpacecraftConfigurationDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Spacecraft
        fields = ('id', 'url', 'name', 'serial_number', 'status', 'spacecraft_config',)


class SpaceStationSerializerForDockingEvent(serializers.HyperlinkedModelSerializer):
    status = SpaceStationStatusSerializer(read_only=True, many=False)
    orbit = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = SpaceStation
        fields = ('id', 'url', 'name', 'status', 'founded', 'description', 'orbit',)


class DockingEventSerializerForSpacecraftFlight(serializers.ModelSerializer):
    docking_location = serializers.StringRelatedField(many=False, read_only=True)
    spacestation = SpaceStationSerializerForDockingEvent(many=False, read_only=True, source='space_station')

    class Meta:
        model = DockingEvent
        fields = ('spacestation', 'docking', 'departure', 'docking_location')


class LaunchListSerializer(serializers.ModelSerializer):
    pad = serializers.StringRelatedField()
    location = serializers.StringRelatedField(source='pad.location')
    status = LaunchStatusSerializer(many=False, read_only=True)
    landing = serializers.SerializerMethodField()
    landing_success = serializers.SerializerMethodField()
    launcher = serializers.SerializerMethodField()
    orbit = serializers.SerializerMethodField()
    mission = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()
    mission_type = serializers.StringRelatedField(source='mission.mission_type.name')
    slug = serializers.SlugField(source='get_full_absolute_url')

    class Meta:
        model = Launch
        fields = (
            'id', 'url', 'launch_library_id', 'slug', 'name', 'status', 'net', 'window_end', 'window_start', 'mission',
            'mission_type', 'pad', 'location', 'landing', 'landing_success', 'launcher', 'orbit', 'image')

    def get_image(self, obj):
        try:
            cache_key = "%s-%s" % (obj.id, "launch-list-image")
            image = cache.get(cache_key)
            if image is not None:
                return image

            image_url = obj.rocket.configuration.image_url

            if image_url is None:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None
            elif image_url:
                cache.set(cache_key, image_url.url, CACHE_TIMEOUT_ONE_DAY)
                return image_url.url
            else:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None

        except Exception as ex:
            return None

    def get_landing(self, obj):
        try:
            cache_key = "%s-%s" % (obj.id, "launch-list-landing")
            landing = cache.get(cache_key)
            if landing is not None:
                return landing

            landings = []
            for stage in obj.rocket.firststage.all():
                if stage.landing is not None:
                    landings.append(stage.landing)

            if len(landings) == 0:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None
            elif len(landings) == 1:
                cache.set(cache_key, landings[0].landing_location.abbrev, CACHE_TIMEOUT_ONE_DAY)
                return landings[0].landing_location.abbrev
            elif len(landings) > 1:
                cache.set(cache_key, "MX Landing", CACHE_TIMEOUT_ONE_DAY)
                return "MX Landing"
            else:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None

        except Exception as ex:
            return None

    def get_landing_success(self, obj):
        try:
            cache_key = "%s-%s" % (obj.id, "launch-list-landing-success")
            landing = cache.get(cache_key)
            if landing is not None:
                return landing

            landings = []
            for stage in obj.rocket.firststage.all():
                if stage.landing is not None:
                    landings.append(stage.landing)

            if len(landings) == 0:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None
            elif len(landings) == 1:
                landing_status = 0
                if landings[0].success is None:
                    landing_status = 0
                elif landings[0].success:
                    landing_status = 1
                elif not landings[0].success:
                    landing_status = 2
                cache.set(cache_key, landing_status, CACHE_TIMEOUT_ONE_DAY)
                return landing_status
            elif len(landings) > 1:
                landing_successes = 0
                landing_failures = 0
                landing_null = 0

                for landing in landings:
                    if landing.success is None:
                        landing_null += 1
                    elif landing.success:
                        landing_successes += 1
                    elif not landing.success:
                        landing_failures += 1

                landing_status = 0
                if (landing_failures > 0 or landing_null > 0) and landing_successes > 0:
                    landing_status = 3
                elif landing_failures > 0 and landing_successes == 0:
                    landing_status = 2
                elif landing_failures == 0 and landing_null == 0 and landing_successes > 0:
                    landing_status = 1
                cache.set(cache_key, landing_status, CACHE_TIMEOUT_ONE_DAY)
                return landing_status
            else:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None

        except Exception as ex:
            return None

    def get_launcher(self, obj):
        try:
            cache_key = "%s-%s" % (obj.id, "launch-list-launcher")
            launcher = cache.get(cache_key)
            if launcher is not None:
                return launcher

            launchers = []
            for stage in obj.rocket.firststage.all():
                if stage.launcher is not None:
                    launchers.append(stage.launcher)

            if len(launchers) == 0:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None
            elif len(launchers) == 1:
                cache.set(cache_key, launchers[0].serial_number, CACHE_TIMEOUT_ONE_DAY)
                return launchers[0].serial_number
            elif len(launchers) > 1:
                cache.set(cache_key, "MX Launchers", CACHE_TIMEOUT_ONE_DAY)
                return "MX Launchers"
            else:
                cache.set(cache_key, None, CACHE_TIMEOUT_ONE_DAY)
                return None

        except Exception as ex:
            return None

    def get_orbit(self, obj):
        try:
            cache_key = "%s-%s" % (obj.id, "launch-list-orbit")
            orbit = cache.get(cache_key)
            if orbit is not None:
                return orbit

            if obj.mission.orbit is not None and obj.mission.orbit.abbrev is not None:
                cache.set(cache_key, obj.mission.orbit.abbrev, CACHE_TIMEOUT_ONE_DAY)
                return obj.mission.orbit.abbrev

        except Exception as ex:
            return None


class SpacecraftStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpacecraftStatus
        fields = ('id', 'name',)


class SpacecraftConfigSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpacecraftConfiguration
        fields = ('id', 'url', 'name', 'in_use')


class SpacecraftSerializer(serializers.HyperlinkedModelSerializer):
    status = SpacecraftStatusSerializer(read_only=True, many=False)
    configuration = SpacecraftConfigSerializer(read_only=True, many=False, source='spacecraft_config')

    class Meta:
        model = Spacecraft
        fields = ('id', 'url', 'name', 'serial_number', 'status', 'configuration')


class SpacecraftFlightSerializer(serializers.HyperlinkedModelSerializer):
    spacecraft = SpacecraftSerializer(read_only=True, many=False)
    launch = LaunchListSerializer(read_only=True, many=False, source='rocket.launch')

    class Meta:
        model = SpacecraftFlight
        fields = ('id', 'url', 'destination', 'splashdown', 'spacecraft', 'launch')


class SpacecraftFlightDetailedSerializer(serializers.HyperlinkedModelSerializer):
    launch_crew = AstronautFlightSerializer(read_only=True, many=True)
    onboard_crew = AstronautFlightSerializer(read_only=True, many=True)
    landing_crew = AstronautFlightSerializer(read_only=True, many=True)
    spacecraft = SpacecraftDetailedNoFlightsSerializer(read_only=True, many=False)
    docking_events = DockingEventSerializerForSpacecraftFlight(read_only=True, many=True)
    launch = LaunchListSerializer(read_only=True, many=False, source='rocket.launch')
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = SpacecraftFlight
        fields = (
        'id', 'url', 'splashdown', 'destination', 'launch_crew', 'onboard_crew', 'landing_crew', 'spacecraft', 'launch',
        'docking_events')


class AgencySerializerDetailedForLaunches(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'url', 'name', 'featured', 'type', 'country_code', 'abbrev', 'description', 'administrator',
                  'founding_year', 'launchers', 'spacecraft', 'launch_library_url', 'successful_launches',
                  'failed_launches', 'pending_launches', 'info_url', 'wiki_url', 'logo_url', 'image_url', 'nation_url',)


class LauncherConfigListSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LauncherConfig
        fields = ('id', 'launch_library_id', 'url', 'name', 'family', 'full_name', 'variant',)


class LauncherConfigSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    launch_service_provider = serializers.ReadOnlyField(read_only=True, source="launch_agency.name")

    class Meta:
        model = LauncherConfig
        fields = ('id', 'launch_library_id', 'url', 'name', 'family', 'full_name', 'variant', 'reusable',
                  'launch_service_provider',)


class LauncherConfigDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    launch_service_provider = AgencySerializerDetailedForLaunches(many=False, read_only=True, source='launch_agency')

    def get_rep(self, obj):
        rep = obj.rep
        serializer_context = {'request': self.context.get('request'),
                              'id': obj.id}
        serializer = AgencySerializer(rep, context=serializer_context)
        return serializer.data

    class Meta:
        model = LauncherConfig
        fields = ('id', 'launch_library_id', 'url', 'name', 'description', 'family', 'full_name',
                  'launch_service_provider', 'variant', 'alias', 'min_stage', 'max_stage', 'length', 'diameter',
                  'maiden_flight', 'launch_mass', 'leo_capacity', 'gto_capacity', 'to_thrust', 'apogee',
                  'vehicle_range', 'image_url', 'info_url', 'wiki_url',)
