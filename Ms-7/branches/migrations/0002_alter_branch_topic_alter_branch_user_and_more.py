# Generated by Django 4.2.9 on 2024-02-27 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topiconbranch', to='branches.topic'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='useronbranch', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leaf',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branchonleaf', to='branches.branch'),
        ),
        migrations.AlterField(
            model_name='leaf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='useronleaf', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='politician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='politicianonrating', to='branches.politician'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='useronrating', to=settings.AUTH_USER_MODEL),
        ),
    ]
