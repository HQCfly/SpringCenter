# Generated by Django 2.1.7 on 2019-03-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20190320_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfor',
            name='avatar',
            field=models.FileField(blank=True, default='avatars/default.png', upload_to='avatars/', verbose_name='头像'),
        ),
    ]