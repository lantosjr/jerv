from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Home page view for JERV ERP
    """
    context = {
        'title': 'JERV ERP - Kezdőlap',
        'user': request.user,
    }
    return render(request, 'core/home.html', context)