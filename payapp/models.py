from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction

CURRENCIES = {
    "USD": "American Dollar",
    "GBP": "Pound Sterling",
    "EUR": "Euro"
}


def format_for_currency(value, currency="GBP"):
    return "{:.2f} {}".format(value, currency)


## MODEL CLASSES

class UserAccount(AbstractUser):
    def balance_str(self) -> str:
        return format_for_currency(self.holding.balance, self.holding.currency)

    def name_str(self):
        return "{} {} [{}]".format(self.first_name, self.last_name, self.username)

    def payments_made(self):
        return Transaction.objects.filter(sender__account=self)

    def payments_received(self):
        return Transaction.objects.filter(recipient__account=self)

    def payments_all(self):
        return self.payments_received() | self.payments_made()

    def requests_sent(self):
        # As in a requests for a transaction, where the recipient would be this account
        return Request.objects.filter(recipient__account=self)

    def requests_received(self):
        # As in, requested transactions where this account WOULD be the sender
        return Request.objects.filter(sender__account=self)

    def requests_all(self):
        return self.requests_received() | self.requests_sent()

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

    def notification_list(self):
        return [n.message for n in self.get_notifications()]

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
                recipient.receive_payment(amount, self.currency, sent_from=self.account.name_str())

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

        payment_from.receive_request(amount_requested, self.currency, request_from=self.account.name_str())
        return True

    def convert_to_native_currency(self, amount, currency_from) -> float:
        if self.currency == currency_from:
            return amount
        else:
            raise Exception("YOU HAVEN'T DONE THIS YET HUGO YOU DUMB FUCK")

    def receive_payment(self, amount, currency, sent_from="Someone"):
        """
        Receives the amount of money in the given currency, and saves a notification
        """
        amount_in = self.convert_to_native_currency(amount, currency)
        self.balance += amount_in
        self.save()

        new_notification = Notification(user=self.account)
        new_notification.message = "{} sent you {} {}".format(sent_from, amount_in, self.currency)
        if currency != self.currency:
            new_notification.message += " [{} {}].".format(amount, currency)
        else:
            new_notification.message += "."
        new_notification.save()

    def receive_request(self, amount_requested, currency, request_from="Someone"):
        new_notification = Notification(user=self.account)
        amount_in_native = self.convert_to_native_currency(amount_requested, currency)
        new_notification.message = "{} has requested you send them {} {}.".format(
            request_from, amount_in_native, self.currency
        )
        new_notification.save()


class Notification(models.Model):
    user = models.ForeignKey(UserAccount, name="user", on_delete=models.CASCADE)
    message = models.TextField(max_length=256, default="Nothing happened")


class AbstractMoneyMovement(models.Model):
    sender = models.ForeignKey(Holding, name="sender", on_delete=models.CASCADE, related_name="sent_from")
    recipient = models.ForeignKey(Holding, name="recipient", on_delete=models.CASCADE, related_name="received_by")
    value = models.PositiveIntegerField(verbose_name="Value (as sent)")
    date_made = models.DateTimeField(auto_now_add=1)

    def value_str(self, format_for_recipient=False):
        if format_for_recipient and self.cross_currency():
            f = self.recipient.convert_to_native_currency(self.value, self.sender.currency)
            return format_for_currency(f, self.recipient.currency)
        else:
            return format_for_currency(value=self.value, currency=self.sender.currency)

    def cross_currency(self):
        return self.sender.currency != self.recipient.currency


class Request(AbstractMoneyMovement):
    STATUSES = {
        'PEN': 'pending',
        'ACC': 'accepted',
        'REJ': 'rejected',
        'WIT': 'withdrawn'
    }
    status = models.CharField(max_length=3, choices=STATUSES, default='PEN')

    def is_possible(self):
        return self.value <= self.sender.balance

    def reject(self) -> bool:
        if self.status == 'PEN':
            self.status = 'REJ'
            self.save()
            return True
        return False

    def accept(self) -> bool:
        success = False
        if self.is_possible() and self.status == 'PEN':
            success = self.sender.send_payment(self.recipient, self.value)
        if success:
            self.status = 'ACC'
            self.save()
        return success



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
