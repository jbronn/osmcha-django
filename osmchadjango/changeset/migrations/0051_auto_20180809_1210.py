# Generated by Django 2.0.6 on 2018-08-09 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changeset', '0050_changeset_new_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changeset',
            name='uid',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='User ID'),
        ),
    ]
