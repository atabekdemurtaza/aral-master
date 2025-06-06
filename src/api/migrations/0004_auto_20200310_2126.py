# Generated by Django 3.0.2 on 2020-03-10 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_classytransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classytransaction',
            name='created_at',
            field=models.DateTimeField(db_index=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='classytransaction',
            name='member_email_address',
            field=models.EmailField(blank=True, max_length=80, verbose_name='member_email_address'),
        ),
    ]
