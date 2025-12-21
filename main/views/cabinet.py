from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.http import HttpResponse

from main.forms import (
    CorporateRegisterForm,
    CorporateLoginForm,
    CorporatePasswordChangeForm,
)
from main.models import Order


def get_user_orders(user):
    if not user or not user.is_authenticated:
        return []
    return Order.objects.filter(user=user).order_by("-order_date")


def handle_register(request):
    if request.method == "POST":
        form = CorporateRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/cabinet?section=login")
    else:
        form = CorporateRegisterForm()

    return {"form": form}


def handle_login(request):
    if request.method == "POST":
        form = CorporateLoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("/cabinet?section=orders")
    else:
        form = CorporateLoginForm()

    return {"form": form}


def handle_change_password(request, user):
    if request.method == "POST":
        form = CorporatePasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return {
                "form": form,
                "success": True,
            }
    else:
        form = CorporatePasswordChangeForm(user)

    return {"form": form}


SECTION_HANDLERS = {
    "register": handle_register,
    "login": handle_login,
    "change_password": handle_change_password,
}


def cabinet_page(request):
    section = request.GET.get("section", "orders")
    user = request.user if request.user.is_authenticated else None

    context = {
        "section": section,
        "user": user,
        "orders": get_user_orders(user),
        "success": False,
        "form": None,
    }

    handler = SECTION_HANDLERS.get(section)

    if handler:
        if section == "change_password":
            if not user:
                return redirect("/cabinet?section=login")
            result = handler(request, user)
        else:
            result = handler(request)

        if isinstance(result, HttpResponse):
            return result

        context.update(result)

    return render(request, "cabinet.html", context)
