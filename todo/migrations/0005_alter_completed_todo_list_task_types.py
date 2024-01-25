# Generated by Django 5.0.1 on 2024-01-20 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_completed_todo_list_task_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completed_todo_list',
            name='task_types',
            field=models.CharField(blank=True, choices=[('Regular', 'Regular'), ('Important', 'Urgent')], max_length=50, null=True),
        ),
    ]
