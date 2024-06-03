from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(User)
admin.site.register(HealthData)
admin.site.register(Challenge)
admin.site.register(CoinsData)
admin.site.register(Friendship)
admin.site.register(Referral)
admin.site.register(PrivacyPolicy)