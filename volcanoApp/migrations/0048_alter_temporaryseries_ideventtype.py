# Generated by Django 4.2.3 on 2023-11-21 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0047_remove_meteorologicaldata_jsonidmet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryseries',
            name='ideventtype',
            field=models.ForeignKey(db_column='idEventType', default='000', on_delete=django.db.models.deletion.DO_NOTHING, to='volcanoApp.eventtype'),
        ),
    ]
