from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [

    #Livros
    path('livros/', views.LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),

    #Autor
    path('autores/', views.AutorList.as_view(), name='autor-list'),
    path('autores/<int:pk>/', views.AutorDetail.as_view(), name='autor-detail'),

    #Categoria
    path('categorias/', views.CategoriaList.as_view(), name='categoria-list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),

    #Coleção


    path('colecoes/', views.ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('colecoes/<int:pk>/', views.ColecaoDetail.as_view(), name='colecao-detail'),

    #Token
    
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    #Doc

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),  
]

