# Generated by Django 4.2.3 on 2023-11-21 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0046_meteorologicaldata_jsonmet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meteorologicaldata',
            name='jsonidmet',
        ),
    ]
