from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('register/', views.signup),
    path('login/', views.login),

    path('levels/', views.levels.as_view()),
    path('levels/create/', views.create_level),
    path('levels/<int:pk>/delete/', views.delete_level),


    path('user/', views.user),
    path('user/<int:pk>/update/', views.update_profile),


    path('homeworks/', views.homework_list),
    path('homeworks/<int:pk>/', views.homework_detail),
    path('homework/<int:homework_id>/', views.submit_homework),
    path('homeworks/submitted/', views.submitted_homeworks),
    # admin
    path('homeworks/create/', views.create_homework),
    path('homeworks/<int:pk>/delete/', views.delete_homework),



    path('groups/', views.groups),
    path('group/<int:pk>/', views.group),
    path('group/lesson/<int:pk>/', views.lesson),
    # admin
    path('group/create/', views.create_group),
    path('group/<int:pk>/delete/', views.delete_group),
    path('group/lesson/create/', views.create_new_lesson),
    path('group/lesson/<int:pk>/delete/', views.delete_lesson),



    path('plans/', views.plans),
    path('plans/create/', views.create_plan),
    path('plans/<int:pk>/delete/', views.delete_plan),


    path('messages_group/', views.group_messages),
    path('messages_group/<int:pk>/', views.one_group_messages),
    path('messages_group/<int:pk>/send/', views.send_group_message),
    # admin
    path('messages_group/create/', views.create_group_messages),
    path('messages_group/<int:pk>/delete/', views.delete_group_messages),



    path('saved/', views.SavedListView.as_view()),
    path('saved/all/', views.get_saved_list),
    path('saved/<int:list_pk>/delete/', views.remove_from_list),


    # admin
    path('students/', views.all_students),
    path('students/<int:student_id>/', views.get_student),
    path('students/<int:student_id>/homeworks/', views.get_student_homeworks),
    path('students/<int:student_id>/<int:homework_id>/answers/', views.get_student_homework_answers),

    path('students/<int:student_id>/saved-list/', views.get_student_saved_list),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

