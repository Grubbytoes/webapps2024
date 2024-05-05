from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction

CURRENCIES = {
    "USD": "American Dollar",
    "GBP": "Pound Sterling",
    "EUR": "Euro"
}


## MODEL CLASSES

class UserAccount(AbstractUser):
    def balance_str(self) -> str:
        _holding = self.holding
        return "{:.2f} {}".format(_holding.balance, _holding.currency)

    def payments_made(self):
        return Transaction.objects.filter(sender__account=self)

    def payments_received(self):
        return Transaction.objects.filter(recipient__account=self)

    def requests_sent(self):
        # As in a requests for a transaction, where the recipient would be this account
        return Request.objects.filter(recipient__account=self)

    def requests_received(self):
        # As in, requested transactions where this account WOULD be the sender
        return Transaction.objects.filter(sender__account=self)

    def payments_made_count(self) -> int:
        return self.payments_made().count()

    def payments_received_count(self) -> int:
        return self.payments_received().count()

    def requests_sent_count(self) -> int:
        return self.requests_sent().count()

    def requests_received_count(self) -> int:
        return self.requests_received().count()

    def clear_notifications(self):
        for n in self.get_notifications():
            n.delete()

    def get_notifications(self):
        return Notification.objects.filter(user=self)

    def notification_count(self):
        return self.get_notifications().count()

    @staticmethod
    def user_by_name(name: str):
        queryset = UserAccount.objects.filter(username=name)
        try:
            return queryset[0]
        except IndexError:
            return None


class Holding(models.Model):
    """
    The amount of money an account has
    """
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="GBP")

    def send_payment(self, recipient: 'Holding', amount) -> bool:
        """
        Sends money, and saves the transaction as a log. does NOT check to see whether balance is sufficient,
        not negative etc.

        :param recipient:
        :param amount:
        :return:
        """

        success = False
        try:
            with transaction.atomic():
                # Transfer money
                self.balance -= amount
                self.save()
                recipient.receive_payment(amount, self.currency)

                # Log the transaction
                t = Transaction(value=amount)
                t.sender = self
                t.recipient = recipient
                t.save()
                success = True
        finally:
            return success

    def send_request(self, payment_from: 'Holding', amount_requested) -> bool:
        new_request = Request(sender=payment_from, recipient=self)
        new_request.value = payment_from.convert_to_native_currency(amount_requested, self.currency)
        new_request.save()
        return True

    def convert_to_native_currency(self, amount, currency_from) -> float:
        if self.currency == currency_from:
            return amount
        else:
            raise Exception("YOU HAVEN'T DONE THIS YET HUGO YOU DUMB FUCK")

    def receive_payment(self, amount, currency, sent_from = "Someone"):
        """
        Receives the amount of money in the given currency, and saves a notification
        """
        amount_in = self.convert_to_native_currency(amount, currency)
        self.balance += amount_in
        self.save()

        new_notification = Notification(user=self.account)
        new_notification.save()


class Notification(models.Model):
    user = models.ForeignKey(UserAccount, name="user", on_delete=models.CASCADE)
    message = models.TextField(max_length=256, default="Nothing happened")


class AbstractMoneyMovement(models.Model):
    sender = models.ForeignKey(Holding, name="sender", on_delete=models.CASCADE, related_name="sent_from")
    recipient = models.ForeignKey(Holding, name="recipient", on_delete=models.CASCADE, related_name="received_by")
    value = models.PositiveIntegerField(verbose_name="Value (as sent)")
    date_made = models.DateTimeField(auto_now_add=1)


class Request(AbstractMoneyMovement):
    STATUSES = {
        'PEN': 'pending',
        'ACC': 'accepted',
        'REJ': 'rejected',
        'WIT': 'withdrawn'
    }
    status = models.CharField(max_length=3, choices=STATUSES, default='PEN')


class Transaction(AbstractMoneyMovement):
    executed = models.BooleanField(default=False)
    requested = models.OneToOneField(Request, null=True, default=None, on_delete=models.SET_NULL)

# GLOBAL FUNCTIONS

def find_user_holding(user: AbstractUser) -> Holding | None:
    query = Holding.objects.filter(account=user)
    if query.exists():
        return query[0]
    else:
        return None
