# Generated by Django 5.1.3 on 2024-11-08 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_collectionitems_image_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectionitems',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='collectionitems',
            name='product_url',
        ),
    ]