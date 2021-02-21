from django.urls import path,include
from . import views


urlpatterns = [
    path('<int:hos_id>/employee/<int:u_id>/', views.dashboard),
    path('health_minister/', views.health_minister_dashboard),
    path('<int:hos_id>/create-employee/', views.create_employee),
    path('<int:hos_id>/list-employee/', views.list_employee),
    path('<int:hos_id>/list-medicine/', views.list_medicine),
    path('<int:hos_id>/create-medicine/', views.create_medicine),
    path('<int:hos_id>/info-medicine/<int:med_ID>/',views.read_medicine),
    path('<int:hos_id>/edit-medicine/<int:med_ID>/',views.edit_medicine),
    path('<int:hos_id>/delete-medicine/<int:med_ID>/',views.delete_medicine),
    path('<int:hos_id>/info-employee/<int:u_id>/',views.read_employee),
    path('<int:hos_id>/delete-employee/<int:u_id>/',views.delete_employee),
    path('<int:hos_id>/edit-employee/<int:u_id>/',views.edit_employee),
    path('<int:doc_id>/create-casefile/',views.create_casefile),
    path('edit-casefile/<int:case_id>/',views.edit_casefile),
    path('casefile/<int:case_id>/',views.read_casefile),
    path('doctor-casefile/',views.list_casefile),
    path('delete-casefile/<int:case_id>/',views.delete_casefile),
    path('recommend-disease-doctor/',views.recommend_disease_doctor),
    path('disease-list/<int:hos_id>/',views.disease_list_director),
    path('<int:hos_id>/disease-action-director/<str:action>/<int:dd_id>/',views.recommend_disease_director),
    path('issue_medicine/<int:case_id>/',views.issue_medicine),
    path('edit_issue_medicine/<int:issue_id>/',views.edit_issue_medicine),
    path('delete_issue_medicine/<int:issue_id>/',views.delete_issue_medicine),
]