# Generated by Django 5.1.3 on 2024-11-12 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_collectionitems_sku_collectionitems_updateprice_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collectionitems',
            old_name='UpdatePrice',
            new_name='oldPrice',
        ),
    ]
