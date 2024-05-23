# Generated by Django 5.0.6 on 2024-05-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_orderitem_description_orderitem_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(default='Description', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default=2222, max_length=20, verbose_name='Phone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='name',
            field=models.CharField(default=111, max_length=50, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
        ),
    ]