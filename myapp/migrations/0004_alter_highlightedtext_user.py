# Generated by Django 4.2 on 2023-04-30 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_highlightedtext_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlightedtext',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
    ]