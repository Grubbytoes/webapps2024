from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    def balance_str(self) -> str:
        _holding = self.holding
        return "{:.2f} {}".format(_holding.balance, _holding.currency)

    def get_payments_made(self) -> int:
        return Transaction.objects.filter(sender__account=self).count()

    def get_payments_received(self) -> int:
        return Transaction.objects.filter(recipient__account=self).count()

CURRENCIES = {
    "USD": "American Dollar",
    "GBP": "Pound Sterling",
    "EUR": "Euro"
}


class Holding(models.Model):
    """
    The amount of money an account has
    """
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="GBP")


class Transaction(models.Model):
    sender = models.ForeignKey(Holding, name="sender", on_delete=models.CASCADE, related_name="sent_from")
    recipient = models.ForeignKey(Holding, name="recipient", on_delete=models.CASCADE, related_name="received_by")
    value = models.PositiveIntegerField(verbose_name="Value (as outgoing)")
    date_made = models.DateTimeField(auto_now_add=1)
