# Generated by Django 4.2.3 on 2023-10-11 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0025_remove_mask_idphoto_alter_imagesegmentation_idphoto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesegmentation',
            name='idphoto',
            field=models.CharField(db_column='idPhoto', max_length=10, primary_key=True, serialize=False),
        ),
    ]
