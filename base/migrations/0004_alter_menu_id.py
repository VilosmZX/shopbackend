# Generated by Django 4.0.6 on 2022-07-30 02:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_menu_user_menu_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]