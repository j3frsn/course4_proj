# Generated by Django 3.2.6 on 2025-07-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SearchTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.TextField(unique=True)),
                ('last_search', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('runtime_minutes', models.PositiveIntegerField(null=True)),
                ('imdb_id', models.SlugField(unique=True)),
                ('plot', models.TextField(blank=True, null=True)),
                ('is_full_record', models.BooleanField(default=False)),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.Genre')),
            ],
            options={
                'ordering': ['title', 'year'],
            },
        ),
    ]
