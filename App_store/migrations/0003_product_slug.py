# Generated by Django 4.0.3 on 2022-04-28 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_store', '0002_category_slug_alter_category_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=264, null=True, unique=True),
        ),
    ]
