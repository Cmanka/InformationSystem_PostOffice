from django.urls import path

from .views import *

urlpatterns = [
    path('', index_view, name='init'),
    path('start/', IndexView.as_view(), name='home'),
    path('post_offices/', PostOfficesView.as_view(), name='post_offices'),
    path('post_office/<int:pk>', PostOfficeByIdView.as_view(), name='post_office'),
    path('publishing_houses/', PublishingHousesView.as_view(), name='publishing_houses'),
    path('publishing_house/<int:pk>', PublishingHouseByIdView.as_view(), name='publishing_house'),
    path('regions/', RegionsView.as_view(), name='regions'),
    path('region/<int:pk>', RegionByIdView.as_view(), name='region'),
    path('houses/', HousesView.as_view(), name='houses'),
    path('house/<int:pk>', HouseByIdView.as_view(), name='house'),
    path('publications/', PublicationsView.as_view(), name='publications'),
    path('publication/<int:pk>', PublicationByIdView.as_view(), name='publication'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('subscription/<int:pk>', SubscriptionByIdView.as_view(), name='subscription'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('follower/<int:pk>', FollowerByIdView.as_view(), name='follower'),
    path('query/1', get_publications, name='query_1'),
    path('query/2', get_postmen, name='query_2'),
    path('query/3', get_served_address, name='query_3'),
    path('query/4', get_follower_publication, name='query_4'),
    path('report/', ReportView.as_view(), name='report'),
    path('export-pdf/', export_pdf, name='export-pdf'),
    path('manage_postmen/', PostmenView.as_view(), name='manage_postmen'),
    path('add_postman/', CreatePostmanView.as_view(), name='add_postman'),
    path('edit_postman/<int:pk>', EditPostmanView.as_view(), name='edit_postman'),
    path('delete_postman/<int:pk>', DeletePostmanView.as_view(), name='delete_postman'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
