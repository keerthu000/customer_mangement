# Generated by Django 4.1.7 on 2024-06-17 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_customerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='checker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.checker'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='maker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.maker'),
        ),
    ]
