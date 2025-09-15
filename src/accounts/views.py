# Accounts app views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """User profile view"""
    return render(request, 'profile.html', {
        'user': request.user,
    })

# Authentication views are handled by Django's built-in auth views
# Custom views will be added here as needed