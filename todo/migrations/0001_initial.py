# Generated by Django 3.2 on 2024-04-13 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accounts', models.TextField(blank=True, null=True)),
                ('filtered_accounts', models.TextField(blank=True, null=True)),
                ('name', models.CharField(max_length=244)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=244)),
                ('commentable_accounts', models.TextField(blank=True, null=True)),
                ('commentable_tweet_ids', models.TextField(blank=True, null=True)),
                ('tweet_links', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=244)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todos',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(auto_created=True, default='image', max_length=244)),
                ('image', models.ImageField(upload_to='images/')),
                ('client_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_images', to='todo.client')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='images',
            field=models.ManyToManyField(related_name='clients', to='todo.Image'),
        ),
    ]
