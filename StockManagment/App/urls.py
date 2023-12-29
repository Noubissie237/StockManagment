from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop page"),
    path('panier/', views.panier, name="panier page"),
    path('commande/', views.commande, name="commande page"),
    path('update_article/', views.update_article, name="update-article"),
    path('traitement_commande/', views.traitementCommande, name="traitement_commande")
]
