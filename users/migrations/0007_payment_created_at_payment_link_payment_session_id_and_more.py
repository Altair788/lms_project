# Generated by Django 4.2.2 on 2024-11-10 17:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0011_delete_coursepayment"),
        ("users", "0006_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(
                blank=True,
                help_text="укажите ссылку на оплату",
                max_length=400,
                null=True,
                verbose_name="ссылка на оплату",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True,
                help_text="укажите идентификатор сессии",
                max_length=255,
                null=True,
                verbose_name="идентификатор сессии",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="paid_course",
            field=models.ForeignKey(
                blank=True,
                help_text="укажите оплаченный курс",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="payment",
                to="lms.course",
                verbose_name="оплаченный курс",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="paid_lesson",
            field=models.ForeignKey(
                blank=True,
                help_text="укажите оплаченный урок",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="payment",
                to="lms.lesson",
                verbose_name="оплаченный урок",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="payment_amount",
            field=models.PositiveIntegerField(
                help_text="укажите сумму оплаты", verbose_name="cумма оплаты"
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="payment_method",
            field=models.CharField(
                choices=[("cash", "Наличными"), ("bank_transfer", "Перевод на счет")],
                help_text="укажите способ оплаты",
                max_length=20,
                verbose_name="способ оплаты",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="укажите покупателя",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="покупатель",
            ),
        ),
    ]
