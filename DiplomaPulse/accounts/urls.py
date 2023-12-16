from django.urls import path
from . import views

urlpatterns = [
    path(
        route="token/",
        view=views.token.obtain_token_view.DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        route="token/refresh/",
        view=views.token.refresh_token_view.DecoratedTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        route="sign-up/",
        view=views.account.sign_up.SignUpView.as_view(),
        name="sign_up",
    ),
    path(
        route="account-info/",
        view=views.account.account_info.AccountInfoView.as_view(),
        name="account_info",
    ),
]
