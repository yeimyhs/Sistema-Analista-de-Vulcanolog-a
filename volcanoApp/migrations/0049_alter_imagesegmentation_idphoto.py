# Generated by Django 4.2.3 on 2023-11-22 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0048_alter_temporaryseries_ideventtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesegmentation',
            name='idphoto',
            field=models.CharField(blank=True, db_column='idPhoto', max_length=21, primary_key=True, serialize=False),
        ),
    ]
