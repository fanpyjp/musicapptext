# Generated by Django 4.2.6 on 2023-11-02 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('music_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('music_name', models.CharField(max_length=30)),
                ('singer', models.CharField(max_length=30)),
                ('longtime', models.DurationField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MusicType',
            fields=[
                ('type_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('User_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('User_name', models.CharField(max_length=20, unique=True)),
                ('Password', models.IntegerField(max_length=30)),
                ('collect', models.ManyToManyField(to='App.music')),
            ],
        ),
        migrations.AddField(
            model_name='music',
            name='music_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.musictype'),
        ),
    ]