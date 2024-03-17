from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    A user's account
    """
    username = models.TextField(max_length=32, unique=True)
    bad_password = models.TextField(max_length=32, null=True)
    email = models.TextField(max_length=64, null=True)

    @staticmethod
    def create_new(new_username: str, new_password: str, new_email: str) -> bool:
        # Check that the username exists
        if Account.objects.filter(username=new_username).exists():
            return False

        new_account: Account = Account(username=new_username, bad_password=new_password, email=new_email)
        new_account.holding = Holding(account=new_account, balance=1000)
        new_account.save()
        return True

class Holding(models.Model):
    """
    The amount of money an account has
    """
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField()


## STATIC FUNCTION

def account_factory(new_username: str, new_password: str) -> Account:
    """
    Instances a new account with the given username and password, and creates an account with a default
    balance of 1000

    it does NOT save the account
    :param new_username: Username
    :param new_password: Password
    :return: the new account
    """
    new_account: Account = Account(username=new_username, bad_password=new_password)
    new_account.holding = Holding(account=new_account, balance=1000)
    return new_account
