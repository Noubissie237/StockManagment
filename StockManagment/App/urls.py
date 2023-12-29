from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop page"),
    path('panier/', views.panier, name="panier page"),
    path('commande/', views.commande, name="commande page"),
    path('update_article/', views.update_article, name="update-article"),
    path('traitement_commande/', views.traitement_commande, name="traitement_commande"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
