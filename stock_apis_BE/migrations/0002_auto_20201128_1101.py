# Generated by Django 3.1.3 on 2020-11-28 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_apis_BE', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='labels',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
    ]
