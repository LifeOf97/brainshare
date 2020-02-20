# Generated by Django 3.0.3 on 2020-02-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, default='', help_text='The state of this post. Published or Drafted', max_length=50, null=True, verbose_name='Status'),
        ),
    ]