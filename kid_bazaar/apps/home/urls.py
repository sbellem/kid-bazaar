from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'items/add', views.AddItemView.as_view(), name="new_item"),
    url(r'items/(?P<item_id>\d+)', views.EditItemView.as_view(), name="edit_item"),
    url(r'items/mine', views.MyItemsView.as_view(), name="my_items"),
    url(r'items/search', views.SearchItemsView.as_view(), name="search_items"),
    url(r'kid/add', views.AddKidView.as_view(), name="new_kid"),
    url(r'kid/(?P<item_id>\d+)', views.EditKidView.as_view(), name="edit_kid"),
    url(r'logout', views.LogoutView.as_view(), name="logout"),
    url(r'register', views.RegisterView.as_view()),
    url(r'items/(?P<item_id>\d+)/bookit',
        views.BookingRequestView.as_view(),
        name='bookit'),
    url(r'items/(?P<item_id>\d+)/confirm_booking',
        views.ConfirmBookingView.as_view(),
        name='confirm_booking'),
    url(r'', views.IndexView.as_view()),
)
