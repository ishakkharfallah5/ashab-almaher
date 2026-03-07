from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.home, name='home'),
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/<int:pk>/', views.skill_detail, name='skill_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/add-skill/', views.add_skill, name='add_skill'),
    path('request-session/<int:teacher_id>/<int:skill_id>/', views.request_session, name='request_session'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/approve/<int:session_id>/', views.approve_session, name='approve_session'),
    path('sessions/complete/<int:session_id>/', views.complete_session, name='complete_session'),
    path('sessions/review/<int:session_id>/', views.submit_review, name='submit_review'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:user_id>/', views.chat, name='chat'),
    path('videos/', views.video_feed, name='video_feed'),
    path('videos/upload/', views.upload_video, name='upload_video'),
    path('users/', views.user_list, name='user_list'),
    path('sessions/reject/<int:session_id>/', views.reject_session, name='reject_session'),
    path('sessions/cancel/<int:session_id>/', views.cancel_session, name='cancel_session'),
    path('signup/', views.signup, name='signup'),
    path('skills/delete/<int:skill_id>/', views.delete_user_skill, name='delete_user_skill'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('rules/', views.rules_page, name='rules'),
    path('report/<int:user_id>/', views.report_content, name='report_content'),
]
