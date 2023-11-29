import django_filters
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Station, Temporaryseries, Volcano \
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



class VolcanoFilter(django_filters.FilterSet):
    class Meta:
        model = Volcano
        fields = ['shortnamevol', 
                  'longnamevol', 
                  'descriptionvol', 
                  'altitudevol', 'pwavespeedvol', 'densityvol', 'attcorrectfactorvol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                field.lookup_expr = 'icontains'

class StationFilter(django_filters.FilterSet):
    class Meta:
        model = Station
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                field.lookup_expr = 'icontains'

class AlertFilter(django_filters.FilterSet):
    class Meta:
        model = Alert
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                field.lookup_expr = 'icontains'