from django.urls import path
from . import views

app_name = 'vacations'

urlpatterns = [
    # Template-based views
    path('', views.VacationListView.as_view(), name='vacation_list'),
    path('create/', views.VacationCreateView.as_view(), name='vacation_create'),
    path('<int:pk>/', views.VacationDetailView.as_view(), name='vacation_detail'),
    path('<int:pk>/update/', views.VacationUpdateView.as_view(),
         name='vacation_update'),
    path('<int:pk>/delete/', views.VacationDeleteView.as_view(),
         name='vacation_delete'),
    path('<int:pk>/delete-direct/', views.vacation_delete_direct,
         name='vacation_delete_direct'),
    path('<int:pk>/like/', views.vacation_like, name='vacation_like'),
    path('coming-soon/', views.ComingSoonView.as_view(), name='coming_soon'),

    # API views
    path('api/', views.VacationListAPIView.as_view(), name='vacation_list_api'),
    path('api/<int:pk>/', views.VacationDetailAPIView.as_view(),
         name='vacation_detail_api'),
    path('api/<int:pk>/like/', views.LikeVacationAPIView.as_view(),
         name='vacation_like_api'),
    path('api/<int:pk>/unlike/', views.UnlikeVacationAPIView.as_view(),
         name='vacation_unlike_api'),
    path('api/countries/', views.CountryListAPIView.as_view(),
         name='country_list_api'),
]
