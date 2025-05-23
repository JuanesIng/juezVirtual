# Generated by Django 5.2 on 2025-04-27 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('input_description', models.TextField()),
                ('output_description', models.TextField()),
                ('sample_input', models.TextField()),
                ('sample_output', models.TextField()),
                ('expected_output', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_code', models.TextField()),
                ('language_id', models.IntegerField()),
                ('stdin', models.TextField(blank=True, default='')),
                ('output', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CORRECT', 'Correct'), ('WRONG', 'Wrong Answer'), ('ERROR', 'Error')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='juez.problem')),
            ],
        ),
    ]
