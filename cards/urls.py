from django.urls import path
from django.contrib.auth.views import LogoutView
from .api import views as api_views
from .views import flashcards, register, LoginView, user_words


urlpatterns = [
    path("", flashcards, name="flashcards"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", register, name="register"),
    path("user_words/", user_words, name="user_words"),
    path("api/review_word/", api_views.ReviewWordView.as_view(), name="review_word"),
    path("api/words/", api_views.WordListCreateView.as_view(), name="word-list-create"),
    path(
        "api/words/<int:pk>/",
        api_views.WordRetrieveUpdateDestroyView.as_view(),
        name="word-retrieve-update-destroy",
    ),
]
