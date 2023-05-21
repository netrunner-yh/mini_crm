from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('', ticket_list, name='home'),

    path('create_user/', create_user, name='create_user'),
    path('user_roles/', user_roles, name='user_roles'),
    path('update_role/<int:user_id>/', update_role, name='update_role'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),

    path('create_ticket/', create_ticket, name='create_ticket'),
    path('edit_ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),

    path('ticket_list/', ticket_list, name='ticket_list'),
    path('ticket_detail/<int:ticket_id>/', ticket_detail, name='ticket_detail'),

    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

    path('search_tickets/', search_tickets, name='search_tickets'),
]
