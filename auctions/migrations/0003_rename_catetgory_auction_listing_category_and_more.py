# Generated by Django 4.0.5 on 2022-08-10 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing_comment_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listing',
            old_name='catetgory',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
    ]
