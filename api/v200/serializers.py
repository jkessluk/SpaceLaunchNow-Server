from api.models import SpacecraftConfiguration, Agency, Events, LauncherConfig
from drf_queryfields import QueryFieldsMixin

from rest_framework import serializers


class LauncherModelSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    agency = serializers.ReadOnlyField(allow_null=True, read_only=True, source="manufacturer.name")
    id = serializers.ReadOnlyField(read_only=True, source="launch_library_id")

    class Meta:
        model = LauncherConfig
        fields = ('id', 'url', 'name', 'description', 'agency', 'variant',  'image_url',
                  'info_url', 'wiki_url')
        extra_kwargs = {
            'url': {'lookup_field': 'launch_library_id'},
        }


class OrbiterSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    agency = serializers.ReadOnlyField(read_only=True, source="manufacturer.name")

    class Meta:
        model = SpacecraftConfiguration
        fields = ('id', 'url', 'name', 'agency', 'history', 'details', 'image_url',
                  'nation_url', 'wiki_link', 'in_use', 'capability')


class OrbiterModelSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    agency = serializers.ReadOnlyField(read_only=True, source="manufacturer.name")

    class Meta:
        model = SpacecraftConfiguration
        fields = ('id', 'url', 'name', 'agency', 'image_url',  'nation_url')


class AgencyHyperlinkedSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    launcher_list = LauncherModelSerializer(many=True, read_only=True)
    orbiter_list = OrbiterModelSerializer(many=True, read_only=True, source='spacecraft_list')
    ceo = serializers.SerializerMethodField('get_administrator')
    orbiters = serializers.ReadOnlyField(read_only=True, source="spacecraft")

    class Meta:
        model = Agency
        fields = ('id', 'url', 'name', 'featured', 'launchers', 'orbiters', 'launcher_list', 'orbiter_list',
                  'description', 'legacy_image_url', 'image_url', 'legacy_nation_url', 'nation_url', 'ceo',
                  'founding_year', 'logo_url', 'launch_library_url',)

    @staticmethod
    def get_administrator(obj):
        return obj.administrator


# class AgencyModelSerializer(QueryFieldsMixin, serializers.ModelSerializer):
#     launcher_list = LauncherModelSerializer(many=True, read_only=True)
#     orbiter_list = OrbiterModelSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Agency
#         fields = ('id', 'url', 'name', 'featured', 'launchers', 'orbiters', 'launcher_list', 'orbiter_list',
#                   'description', 'legacy_image_url', 'image_url', 'legacy_nation_url', 'nation_url', 'ceo',
#                   'founding_year', 'logo_url', 'launch_library_url', 'launch_library_id')


class LauncherDetailSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
    agency = serializers.ReadOnlyField(allow_null=True, read_only=True, source="manufacturer.name")
    id = serializers.ReadOnlyField(read_only=True, source="launch_library_id")

    class Meta:
        model = LauncherConfig
        fields = ('id', 'url', 'name', 'description', 'family', 'full_name', 'agency',
                  'variant', 'alias', 'min_stage', 'max_stage', 'length', 'diameter',
                  'launch_mass', 'leo_capacity', 'gto_capacity', 'to_thrust',
                  'apogee', 'vehicle_range', 'image_url', 'info_url', 'wiki_url')
        extra_kwargs = {
            'url': {'lookup_field': 'launch_library_id'},
        }


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'name', 'description', 'location', 'feature_image', 'date')
