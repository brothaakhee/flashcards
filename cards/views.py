from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, authenticate, login


@login_required
def flashcards(request):
    return render(request, "flashcards.html")


@login_required
def user_words(request):
    return render(request, "user_words.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("flashcards")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


class LoginView(auth_views.LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse("flashcards")
