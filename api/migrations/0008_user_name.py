# Generated by Django 5.0 on 2024-01-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_url_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
