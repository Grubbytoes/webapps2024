from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    """
    A user's account
    """
    username = models.TextField(max_length=32, unique=True)
    password = models.TextField(max_length=32, null=True)
    email = models.TextField(max_length=64, null=True)

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


class Holding(models.Model):
    """
    The amount of money an account has
    """
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField()


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
