from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from Rentals import views
from rest_framework.authtoken import views as rest_views

# Patterns that have associated models and serializers
urlpatterns = format_suffix_patterns([
    # Root URL
    url(r'^$', views.api_root),

    url(r'^location/$',
        views.LocationList.as_view(),
        name='location-list'),
    url(r'^location/(?P<pk>[0-9]+)/$',
        views.LocationDetail.as_view(),
        name='location-detail'),

    url(r'^game/$',
        views.GameList.as_view(),
        name='game-list'),
    url(r'^game/(?P<pk>[0-9]+)/$',
        views.GameDetail.as_view(),
        name='game-detail'),

    url(r'^message/$',
        views.MessageList.as_view(),
        name='message-list'),
    url(r'^message/(?P<pk>[0-9]+)/$',
        views.MessageDetail.as_view(),
        name='message-detail'),

    url(r'^profile/$',
        views.ProfileList.as_view(),
        name='profile-list'),
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.ProfileDetail.as_view(),
        name='profile-detail'),

    # User URLs
    url(r'^user/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
])

# Login and logout view for the browseable API
urlpatterns += [
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Account creation views
urlpatterns += [
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
]

# View for goalies to apply to games
urlpatterns += [
    url(r'^apply/$', views.ApplyForGame.as_view(), name='apply'),
    url(r'^check-username/$', views.CheckUsernameUnique.as_view(), name='check-username'),
    url(r'^check-email/$', views.CheckEmailUnique.as_view(), name='check-email'),
]

# Password reset views
urlpatterns += [
    url(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
]
