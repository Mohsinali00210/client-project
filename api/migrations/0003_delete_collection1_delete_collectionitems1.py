# Generated by Django 5.1.2 on 2024-11-07 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_collection1_collectionitems1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Collection1',
        ),
        migrations.DeleteModel(
            name='CollectionItems1',
        ),
    ]
