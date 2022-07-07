from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount

# Create your views here.
def Home(request):
    return render(request, 'review/Home.html', {})


# fb_id = SocialAccount.objects.filter(user=user)

def Dashboard(request, any):
    return render(request, 'DashboardClient.html')
