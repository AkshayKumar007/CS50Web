# Generated by Django 2.2.5 on 2020-01-12 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('pasta_name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('pizza_type', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Salads',
            fields=[
                ('salad_name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('top_name', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subs',
            fields=[
                ('sub_name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('size', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'unique_together': {('sub_name', 'size', 'price')},
            },
        ),
        migrations.CreateModel(
            name='DinnerPlaters',
            fields=[
                ('dinner_name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('size', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'unique_together': {('dinner_name', 'size', 'price')},
            },
        ),
    ]