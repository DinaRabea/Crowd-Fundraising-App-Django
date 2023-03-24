from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import userprofile, edit, More, delete_account
urlpatterns = [
    path('<int:id>/show', userprofile, name='show'),

    path('<int:pk>/edit', (edit.as_view()), name='edit'),
    path('<int:pk>/moreInfo', (More.as_view()), name='moreInfo'),
    path('<int:id>/delete_account', delete_account, name='delete_account'),
]

# path('<int:id>/userproject', userproject, name="userproject"),
# path('<int:id>/userDonation', userDonation, name="userDonation"),
