from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('staff', views.staff, name='staff'),
    path('add_staff', views.add_staff, name='add_staff'),
    path('new_group', views.new_group, name='new_group'),
    path('view_group', views.view_group, name='view_group'),
    path('print_profiles', views.print_profiles, name='print_profiles'),
    path('edit_group', views.edit_group, name='edit_group'),
    path('enter_points', views.enter_points, name='enter_points'),
    path('edit_points', views.edit_points, name='edit_points'),
    path('overall_points', views.overall_points, name='overall_points'),
    path('detail_points', views.detail_points, name='detail_points'),
    path('weekly_chart', views.weekly_chart, name='weekly_chart'),
    path('make_sheets', views.make_sheets, name='make_sheets'),
    path('message', views.message, name='message'),
    path('email', views.email, name='email'),
    path('info', views.info, name='info'),
    path('send_message', views.send_message, name='send_message'),
    path('enter_sheets', views.enter_sheets, name='enter_sheets'),
    path('last_week', views.last_week, name='last_week'),
    path('offline_forms', views.offline_forms, name='offline_forms'),
    path('profile/<str:id>', views.profile, name='profile'),
]

# path to media folder with camper pics
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)