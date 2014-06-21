from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

    url(r'items/add', views.AddItemView.as_view(), name="new_item"),
    url(r'items/(?P<item_id>\d+)', views.EditItemView.as_view(), name="edit_item"),
    url(r'items/mine', views.MyItemsView.as_view(), name="my_items"),
    url(r'items/search', views.SearchItemsView.as_view(), name="search_items"),
    url(r'profile', views.ProfileView.as_view(), name="profile"),
    url(r'logout', views.LogoutView.as_view(), name="logout"),
    url(r'', views.IndexView.as_view()),
)
