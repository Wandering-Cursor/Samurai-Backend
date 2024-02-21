from django.urls import path

from communication.views import chat as chat_views

chat_patterns = [
    path(
        "chat/",
        # TMP
        chat_views.list_chat.CommunicationView.as_view(),
    ),
    path(
        "chat/list",
        chat_views.list_chat.ListChatView.as_view(),
    ),
    path(
        "chat/create",
        chat_views.create_chat.CreateChatView.as_view(),
    ),
    path(
        "chat/leave",
        # TMP
        chat_views.list_chat.CommunicationView.as_view(),
    ),
]


urlpatterns = chat_patterns
