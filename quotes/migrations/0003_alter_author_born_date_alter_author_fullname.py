# Generated by Django 5.0.4 on 2024-05-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='born_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='author',
            name='fullname',
            field=models.CharField(max_length=100),
        ),
    ]
