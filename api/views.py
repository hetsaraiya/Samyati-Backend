from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
import jwt
from .models import *
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from .serializers import HealthDataSerializer
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
CLIENT_ID = "428886898955-qt8kr12km3398041tqfoubid991vk8gj.apps.googleusercontent.com"
CLIENT_SECRET = "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"

GOOGLE_ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

@csrf_exempt
def googleSignInAcc(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        redirect_uri = 'google.com'            
        if code:
            token_data = code
            
            user_info_response = requests.get(GOOGLE_USER_INFO_URL, params={'access_token': token_data})
            if user_info_response.ok:
                user_info = user_info_response.json()
                
                # Retrieve or create the user in your database
                user, created = User.objects.get_or_create(
                    email=user_info['email'],
                    defaults={
                        'username': user_info['name'],
                        'first_name': user_info.get('given_name'),
                        'last_name': user_info.get('family_name')
                    }
                )
                refresh = RefreshToken.for_user(user)
                resp = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                }
                print(refresh.access_token)
                return HttpResponse(json.dumps(resp))
            
            else:
                return HttpResponse(json.dumps({'error': 'Failed to retrieve user info from Google.'}))
        
        else:
            return HttpResponse(json.dumps({'error': 'Failed to obtain access token.'}))
    else:
        return HttpResponse(json.dumps({'error': 'Bad request.'}))
    

@api_view()
@permission_classes((IsAuthenticated,))
def new(request):
    return HttpResponse(json.dumps({'Login': 'SuccessfulLogin'}))

class ChallengeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        challenges = Challenge.objects.all()
        challenge_data = []
        for challenge in challenges:
            challenge_data.append({
                'id': challenge.id,
                'name': challenge.name,
                'description': challenge.description,
                'target_steps': challenge.target_steps, 
                'start_date': challenge.start_date,
                'end_date': challenge.end_date,
                'created_at': challenge.created_at,
                'updated_at': challenge.updated_at,
            })
        return Response(challenge_data)

    def post(self, request):
        challenge_data = request.data
        challenge = Challenge.objects.create(
            name=challenge_data['name'],
            description=challenge_data['description'],
            # Add other challenge fields as needed
        )
        return Response({
            'id': challenge.id,
            'name': challenge.name,
            'description': challenge.description,
            # Add other challenge fields as needed
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def healthData(request):
    if request.method == 'POST':
        data = request.data
        user = request.user

        # Extract data from request
        steps = data.get('steps')
        calories = data.get('calories')
        distance = data.get('distance')
        percentage_steps = data.get('percentage_steps')
        percentage_calories = data.get('percentage_calories')
        percentage_distance = data.get('percentage_distance')
        earned_coin = data.get('earned_coin')
        week_steps = data.get('week_steps')
        week_cal = data.get('week_cal')
        week_dis = data.get('week_dis')
        week_percentage_steps = data.get('week_percentage_steps')
        week_percentage_calories = data.get('week_percentage_calories')
        week_percentage_distance = data.get('week_percentage_distance')

        # Check if HealthData object already exists for the user
        health_data, created = HealthData.objects.get_or_create(user=user)

        # Update or create HealthData object
        health_data.steps = steps
        health_data.calories = calories
        health_data.distance = distance
        health_data.percentage_steps = percentage_steps
        health_data.percentage_calories = percentage_calories
        health_data.percentage_distance = percentage_distance
        health_data.earned_coin = earned_coin
        health_data.week_steps = week_steps
        health_data.week_cal = week_cal
        health_data.week_dis = week_dis
        health_data.week_percentage_steps = week_percentage_steps
        health_data.week_percentage_calories = week_percentage_calories
        health_data.week_percentage_distance = week_percentage_distance
        health_data.save()

        # Update or create CoinsData object
        coins_data, _ = CoinsData.objects.update_or_create(
            user=user,
            defaults={'earned_today': int(int(steps) / 1000)}
        )

        # Return response
        if created:
            return Response({'message': 'Health data created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Health data updated successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view()
@permission_classes((IsAuthenticated,))
def getUserDetails(request):
    if request.method == "GET":
        user = request.user
        resp = {
            "username" : user.username
        }
        return Response(resp, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFriends(request):
    user = request.user
    friends = Friendship.objects.filter(to_user=user)
    print(friends)
    data = []
    for friendship in friends:
        friend = friendship.from_user
        try:
            health_data = HealthData.objects.get(user=friend)
            resp = {
                "username": friend.username,
                "steps": health_data.steps,
                "coins": health_data.steps / 1000,
                "name": friend.name,
                "id" : friend.pk,
            }
            data.append(resp)
        except HealthData.DoesNotExist:
            continue
    data.append({"refer" : request.user.referral_code})
    return Response(data)

def getPrivacyPolicy(request):
    user = request.user
    if user is not None:
        p = PrivacyPolicy.objects.get(title="Privacy Policy")
        resp = {
            "content" : p.content
        }
        return Response(resp)
    else:
        resp = {
            "content" : "Invalid User Credentials"
        }
        return Response(resp)