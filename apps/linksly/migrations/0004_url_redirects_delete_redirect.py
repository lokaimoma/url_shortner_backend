# Generated by Django 4.0.4 on 2022-06-17 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linksly', '0003_alter_url_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='redirects',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='Redirect',
        ),
    ]
