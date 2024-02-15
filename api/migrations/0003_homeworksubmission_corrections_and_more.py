# Generated by Django 5.0.1 on 2024-01-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_answer_homework_homeworksubmission_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworksubmission',
            name='corrections',
            field=models.ManyToManyField(related_name='corrections', to='api.answer'),
        ),
        migrations.AddField(
            model_name='homeworksubmission',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.DeleteModel(
            name='HomeworkCorrection',
        ),
    ]