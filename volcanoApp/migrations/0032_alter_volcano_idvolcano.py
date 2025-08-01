# Generated by Django 4.2.3 on 2023-10-12 02:19

from django.db import migrations, models
import volcanoApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0031_alter_volcano_idvolcano'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volcano',
            name='idvolcano',
            field=models.CharField(db_column='idVolcano', default=volcanoApp.models.Volcano.generate_default_idvolcano, max_length=9, primary_key=True, serialize=False),
        ),
    ]
