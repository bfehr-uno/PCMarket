# Generated by Django 3.1.3 on 2020-11-30 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Listings', '0002_remove_soldlisting_date_of_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_listings',
            field=models.ManyToManyField(to='Listings.CurrentListing'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(to='Listings.FollowedListing'),
        ),
    ]