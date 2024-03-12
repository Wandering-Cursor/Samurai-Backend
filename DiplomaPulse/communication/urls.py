from django.urls import path

from communication.views import chat as chat_views
from communication.views import message as message_views
from communication.views.base import CommunicationView

chat_patterns = [
    path(
        "chat/",
        chat_views.chat_details.ChatDetailsView.as_view(),
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
        chat_views.leave_chat.LeaveChatView.as_view(),
    ),
]

message_patterns = [
    path(
        "message/send",
        message_views.send_message.SendMessageView.as_view(),
    ),
    path(
        "message/",
        CommunicationView.as_view(),
    ),
    path(
        "message/list",
        CommunicationView.as_view(),
    ),
    path(
        "message/search",
        CommunicationView.as_view(),
    ),
]


urlpatterns = chat_patterns + message_patterns
