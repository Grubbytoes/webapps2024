from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import User

CURRENCIES = {
    "USD": "American Dollar",
    "GBP": "Pound Sterling",
    "EUR": "Euro"
}


class UserAccount(AbstractBaseUser):
    """
    A user's account

    Yes' I know there's an inbuilt user base class - I wanted to do as much of this myself as I could
    for education's sake. Maybe I will change it later

    Also, if you're reading this marker, it was never mentioned in the labs or in the project description
    """
    # The essentials added at account creation
    username = models.TextField(max_length=32, unique=True)
    password = models.TextField(max_length=32, null=True)
    email = models.TextField(max_length=64, null=True)

    # Further details and verification
    fname = models.TextField(name="first_name", max_length=32, null=1)
    lname = models.TextField(name="last_name", max_length=32, null=1)
    v = models.BooleanField(name="verified", default=False)

    @staticmethod
    def create_new(new_username: str, new_password: str, new_email: str) -> int:
        """
        Creates a new user account, provided the given username is unique.
        Also creates a new account holding
        :param new_username:
        :param new_password:
        :param new_email:
        :return: The ID of the newly created user, if successful, otherwise:
            -1: username already exists
            -2: bad password
        """
        if UserAccount.objects.filter(username=new_username).exists():
            return -1

        new_account: UserAccount = UserAccount(username=new_username, email=new_email)
        new_account.password = make_password(new_password)
        new_account.holding = Holding(account=new_account, balance=1000)
        new_account.save()
        return new_account.id

    def authenticate_password(self, input_password: str) -> int:
        if check_password(input_password, self.password):
            return self.id
        else:
            return -1


class Holding(models.Model):
    """
    The amount of money an account has
    """
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="GBP")


class Transaction(models.Model):
    sender = models.ForeignKey(Holding, name="sender", on_delete=models.CASCADE, related_name="sent_from")
    recipient = models.ForeignKey(Holding, name="recipient", on_delete=models.CASCADE, related_name="received_by")
    value = models.PositiveIntegerField(verbose_name="Value (as outgoing)")
    date_made = models.DateTimeField(auto_now_add=1)

# STATIC FUNCTION

def account_factory(new_username: str, new_password: str) -> UserAccount:
    """
    Instances a new account with the given username and password, and creates an account with a default
    balance of 1000

    it does NOT save the account
    :param new_username: Username
    :param new_password: Password
    :return: the new account
    """
    new_account: UserAccount = UserAccount(username=new_username, bad_password=new_password)
    new_account.holding = Holding(account=new_account, balance=1000)
    return new_account
