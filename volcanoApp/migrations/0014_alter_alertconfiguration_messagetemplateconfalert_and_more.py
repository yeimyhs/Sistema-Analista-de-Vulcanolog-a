# Generated by Django 4.2.3 on 2023-09-06 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0013_mask_indmask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertconfiguration',
            name='messagetemplateconfalert',
            field=models.TextField(blank=True, db_column='messageTemplateConfAlert', null=True),
        ),
        migrations.AlterField(
            model_name='volcano',
            name='datecreationvol',
            field=models.DateTimeField(auto_now_add=True, db_column='DateCreationVol'),
        ),
    ]
