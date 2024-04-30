from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction


## MODEL CLASSES

class UserAccount(AbstractUser):
    def balance_str(self) -> str:
        _holding = self.holding
        return "{:.2f} {}".format(_holding.balance, _holding.currency)

    def get_payments_made(self) -> int:
        return Transaction.objects.filter(sender__account=self).count()

    def get_payments_received(self) -> int:
        return Transaction.objects.filter(recipient__account=self).count()

    @staticmethod
    def user_by_name(name: str):
        queryset = UserAccount.objects.filter(username=name)
        try:
            return queryset[0]
        except IndexError:
            return None


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

    def send_payment(self, recipient_name: str, amount) -> int:
        """
        Makes a payment
        :param recipient: Account to receive money
        :param amount: Amount it be sent, in sender's native currency
        :return:
        * 1 if successful
        * 0 if transaction was aborted:
        * -1 if insufficient funds
        * -2 if recipient cannot be found
        * -3 Attempt to send money to yourself
        * -4 Attempt to send negative money or zero
        """
        # Do we have enough money?
        if amount > self.balance:
            return -1

        # Attempt to sent negative or zero money
        if amount <= 0:
            return -4

        # Get the recipient
        recipient = UserAccount.user_by_name(recipient_name)
        if recipient is None:
            return -2
        recipient = recipient.holding

        if recipient == self:
            return -3

        # Do the thing
        code = 0
        try:
            with transaction.atomic():
                # Transfer money
                self.balance -= amount
                self.save()
                recipient.balance += amount
                recipient.save()

                # Log the transaction
                t = Transaction(value=amount)
                t.sender = self
                t.recipient = recipient
                t.save()
                code = 1
        finally:
            return code

    def send_request(self, recipient, amount):
        pass


class Transaction(models.Model):
    sender = models.ForeignKey(Holding, name="sender", on_delete=models.CASCADE, related_name="sent_from")
    recipient = models.ForeignKey(Holding, name="recipient", on_delete=models.CASCADE, related_name="received_by")
    value = models.PositiveIntegerField(verbose_name="Value (as outgoing)")
    date_made = models.DateTimeField(auto_now_add=1)


class Request(models.Model):
    STATUSES = {
        'PEN': 'pending',
        'ACC': 'accepted',
        'REJ': 'rejected',
        'WIT': 'withdrawn'
    }

    transaction_requested = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=3, choices=STATUSES, default='PEN')

# GLOBAL FUNCTIONS

def find_user_holding(user: AbstractUser) -> Holding | None:
    query = Holding.objects.filter(account=user)
    if query.exists():
        return query[0]
    else:
        return None
