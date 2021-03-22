from django.shortcuts import render
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()

    context = {"form": form}
    return render(request, "users/register.html", context)
