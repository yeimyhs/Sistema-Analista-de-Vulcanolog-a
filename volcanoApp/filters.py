import django_filters
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Meteorologicaldata, Station, Temporaryseries, Volcano \
    , UserP
class UserPFilter(django_filters.FilterSet):
    names = django_filters.CharFilter(lookup_expr='icontains')
    lastname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    institution = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    datecreation = django_filters.DateFilter()
    type = django_filters.CharFilter(lookup_expr='iexact')  # Use 'iexact' for case-insensitive exact matching

    class Meta:
        model = UserP
        fields = [
            'names',
            'lastname',
            'email',
            'institution',
            'country',
            'city',
            'state',
            'datecreation',
            'type',
        ]