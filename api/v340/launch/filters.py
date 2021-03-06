from django_filters import filters, FilterSet, Filter, ModelChoiceFilter
from django.utils.translation import ugettext as _
from django_filters.fields import Lookup

from api.models import Launch, Agency


class ListFilter(Filter):
    def filter(self, qs, value):
        value_list = value.split(u',')
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class LaunchDateFilter(FilterSet):
    net__gt = filters.DateFilter(
        field_name='net', lookup_expr='gt',
        label=_('%s is greater than' % _('NET'))
    )
    net__lt = filters.DateFilter(
        field_name='net', lookup_expr='lt',
        label=_('%s is less than' % _('NET'))
    )
    net__gte = filters.DateFilter(
        field_name='net', lookup_expr='gte',
        label=_('%s is greater than or equal to' % _('NET'))
    )
    net__lte = filters.DateFilter(
        field_name='net', lookup_expr='lte',
        label=_('%s is less than or equal to' % _('NET'))
    )
    orbit = ListFilter(name='mission__orbit')


    class Meta:
        model = Launch
        fields = {
            'name', 'rocket__configuration__name', 'rocket__configuration', 'status',
            'launch_library_id', 'rocket__spacecraftflight__spacecraft__name',
            'rocket__spacecraftflight__spacecraft__id',
            'rocket__configuration__manufacturer__name',
            'orbit'
        }


class LaunchFilter(FilterSet):
    orbit = ListFilter(name='mission__orbit')

    class Meta:
        model = Launch
        fields = {
            'name', 'rocket__configuration__name', 'rocket__configuration', 'status',
            'launch_library_id', 'rocket__spacecraftflight__spacecraft__name',
            'rocket__spacecraftflight__spacecraft__id', 'rocket__configuration__manufacturer__name',
            'orbit'
        }
