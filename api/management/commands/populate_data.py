import random
import string
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from api.models import User, Challenge, HealthData, Friendship, Referral, CoinsData

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample users with unique email addresses
        users = []
        for i in range(3):
            email = f'user{i}@example.com'
            while User.objects.filter(email=email).exists():
                email = f'user{i}_{random.randint(1, 10000)}@example.com'
            
            user = User(
                username=f'user{i}',
                name=f'User {i}',
                email=email,
                gender=random.choice([User.MALE, User.FEMALE]),
            )
            user.set_password('password')  # Set a default password
            user.save()
            users.append(user)

        # Create sample challenges
        challenges_data = [
            {
                "name": "10,000 Steps a Day Challenge",
                "description": "Commit to walking 10,000 steps every day for a healthier lifestyle. Track your progress and stay motivated with daily reminders.",
                "target_steps": 10000,
                "start_date": datetime.today().date(),
                "end_date": (datetime.today() + timedelta(days=30)).date(),
            },
            {
                "name": "Weekend Warrior Challenge",
                "description": "Stay active over the weekend by hitting 15,000 steps on both Saturday and Sunday. A perfect way to keep fit and enjoy the outdoors!",
                "target_steps": 15000,
                "start_date": (datetime.today() + timedelta(days=5)).date(),
                "end_date": (datetime.today() + timedelta(days=7)).date(),
            },
            {
                "name": "Month-Long Marathon",
                "description": "Challenge yourself to reach a total of 300,000 steps over the course of a month. A great way to maintain a steady fitness routine.",
                "target_steps": 300000,
                "start_date": datetime.today().date(),
                "end_date": (datetime.today() + timedelta(days=30)).date(),
            },
        ]

        for challenge_data in challenges_data:
            challenge = Challenge(**challenge_data)
            challenge.save()
            for user in users:
                challenge.taken_by.add(user)
            challenge.save()

        # Create sample health data
        for user in users:
            health_data = HealthData(
                user=user,
                steps=random.randint(1000, 10000),
                calories=random.uniform(50.0, 500.0),
                distance=random.uniform(0.5, 5.0),
                percentage_steps=random.uniform(0.0, 100.0),
                percentage_calories=random.uniform(0.0, 100.0),
                percentage_distance=random.uniform(0.0, 100.0),
                earned_coin=random.randint(0, 100),
                week_steps=str(random.randint(10000, 70000)),
                week_cal=random.uniform(500.0, 3500.0),
                week_dis=random.uniform(5.0, 35.0),
                week_percentage_steps=random.uniform(0.0, 100.0),
                week_percentage_calories=random.uniform(0.0, 100.0),
                week_percentage_distance=random.uniform(0.0, 100.0),
            )
            health_data.save()

        # Create sample friendships
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                friendship = Friendship(from_user=users[i], to_user=users[j])
                friendship.save()

        # Create sample referrals
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                referral = Referral(referrer=users[i], referred=users[j])
                referral.save()

        # Create sample coin data
        for user in users:
            coins_data = CoinsData(
                user=user,
                earned_today=random.randint(0, 100),
                total_coins=random.randint(100, 1000),
            )
            coins_data.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
