from django.urls import path
from .views import set_cookie_view, get_cookie_view, set_session_view, get_session_view, \
    MyLogoutView, MyLoginView, ProfileView, RegisterView, UserListView, \
    AboutMeView, ProfileDetailView, ProfileUpdateView

app_name = "myauth"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("users/<int:pk>/edit", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("about-me/", AboutMeView.as_view(), name="about_me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("session/set/", set_session_view, name="session_set"),
    path("session/get/", get_session_view, name="session_get"),
]