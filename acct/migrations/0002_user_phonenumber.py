# Generated by Django 4.1.5 on 2023-01-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acct', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
