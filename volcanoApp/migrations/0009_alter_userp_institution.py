# Generated by Django 4.2.3 on 2023-08-29 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0008_userp_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userp',
            name='institution',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
