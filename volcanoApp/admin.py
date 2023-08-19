from django.contrib import admin
from django.apps import apps
# Register your models here.

# Obtén una lista de los nombres de los modelos que deseas registrar
model_names = ['Alert', 'Alertconfiguration', 'Blob', 'Eventtype', 'History', 'Imagesegmentation', 'Mask', 'Meteorologicaldata', 'Station', 'Temporaryseries', 'Volcano', 'UserP']

# Registra los modelos en el admin
for model_name in model_names:
    model = apps.get_model(app_label='volcanoApp', model_name=model_name)
    admin.site.register(model)




