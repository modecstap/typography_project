from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout


def logout_view(request):
    auth_logout(request)
    return redirect("/cabinet?section=login")
