# Generated by Django 4.1.13 on 2024-01-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='quotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('avatar', models.BinaryField()),
            ],
        ),
    ]
