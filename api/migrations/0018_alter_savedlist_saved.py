# Generated by Django 5.0.1 on 2024-02-05 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_saved_savedlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedlist',
            name='saved',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_list_details', to='api.saved'),
        ),
    ]
