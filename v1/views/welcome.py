from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def welcome(request):
    user = request.user
    return render(request, 'welcome.html', {'user': user})
