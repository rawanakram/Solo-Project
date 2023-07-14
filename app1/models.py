from django.db import models
import re
import bcrypt

# Create your models here.
class ContractorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["first_name"]) < 2 or not postData["first_name"].isalpha():
            errors["first_name"] = "The first name should be at least 2 characters and contains letters only!"
        if len(postData["last_name"]) < 2 or not postData["last_name"].isalpha():
            errors["last_name"] = "The last name should be at least 2 characters and contains letters only!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address!!!"
        if len(postData["password"]) < 8:
            errors['password'] = "Your password should be at least 8 characters"
        if postData["password"] != postData["pwdconfirm"]:
            errors['password'] = "The passwords are not the same!!!"
        return errors


    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors2 = {}
        email2 = postData['email2']
        inputPassword2 = postData['inputPassword2']
        contractor = Contractor.objects.filter(email=email2)
        if len(email2) < 1:
            errors2["email2"] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(email2):
            errors2["email2"] = "Invalid Email Address!"
        elif not bcrypt.checkpw(inputPassword2.encode(), contractor[0].password.encode()):
            errors2["inputPassword2"] = "Incorrect password. Try again!"
        return errors2

class Contractor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    spcialized_in = models.CharField(max_length=255)
    phone_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContractorManager()


class Material(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    added_by = models.ForeignKey(Contractor, related_name="materials", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
