from os import name
from django.urls import path, include
from .views import SentenceList, SentenceDetails, DiacritizationView, SentenceRequests, DiacritizationFileView
urlpatterns = [
    path('accounts/', include('users.urls')),
    path('sentences/', SentenceList.as_view()),
    path('sentences/requests/', SentenceRequests.as_view()),
    path('sentences/new/', DiacritizationView.as_view()),
    path('sentences/new-file/', DiacritizationFileView.as_view()),
    path('sentences/<int:id>/', SentenceDetails.as_view()),
]
