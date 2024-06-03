import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import datetime
# Create your models here.

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= ('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups'  # Provide a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Provide a unique related_name
    )
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(null=False, blank=False, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)

    def generate_unique_referral_code(self):
        length = 10
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters, k=length))
            if not User.objects.filter(referral_code=code).exists():
                return code
            
class Challenge(models.Model):
    taken_by = models.ManyToManyField(User, related_name='challenges')
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    target_steps = models.IntegerField(default=0)
    start_date = models.DateField(default=datetime.datetime.today)
    end_date = models.DateField(default=datetime.datetime.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class HealthData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    steps = models.IntegerField(default=0)
    calories = models.FloatField(default=0.0)
    distance = models.FloatField(default=0.0)
    percentage_steps = models.FloatField(default=0.0)
    percentage_calories = models.FloatField(default=0.0)
    percentage_distance = models.FloatField(default=0.0)
    earned_coin = models.IntegerField(default=0)
    week_steps = models.CharField(max_length=10, default="0")
    week_cal = models.FloatField(default=0.0)
    week_dis = models.FloatField(default=0.0)
    week_percentage_steps = models.FloatField(default=0.0)
    week_percentage_calories = models.FloatField(default=0.0)
    week_percentage_distance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.steps} steps'

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_friend_set', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_friend_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('from_user', 'to_user'),)

    def __str__(self):
        return f"{self.from_user.username} is friends with {self.to_user.username}"

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals_made', on_delete=models.CASCADE)
    referred = models.ForeignKey(User, related_name='referrals_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('referrer', 'referred'),)

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username}"

class CoinsData(models.Model):
    earned_today = models.PositiveIntegerField(default=0)
    total_coins = models.PositiveIntegerField(default=0, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.name}'s Coin Data"
    
class PrivacyPolicy(models.Model):
    content = models.TextField(default="")
    title = models.CharField(max_length=20, default="Privacy Policy")

    def __str__(self) -> str:
        return f"{self.title}"
