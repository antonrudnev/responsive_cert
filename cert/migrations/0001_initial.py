# Generated by Django 2.1.3 on 2018-11-14 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_content', models.TextField()),
                ('transaction_id', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('public_key', models.CharField(max_length=256, null=True)),
                ('private_key', models.CharField(max_length=256, null=True)),
                ('cert_template', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='credential',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issuers', to='cert.User'),
        ),
        migrations.AddField(
            model_name='credential',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='cert.User'),
        ),
    ]