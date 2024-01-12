
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from App.models import Client, Category, Produit, Commande, CommandeArticle, AddressChipping
from .serializers import ProduitSerializer  # Assurez-vous d'importer votre sérialiseur approprié
from App.utils import data_cookie 


class CurrenTimeView(APIView):
    def get(self, request, *args, **kwargs):
        curren_time = datetime.now().strftime("%y-%m-%d %H-%M-%S")

        return Response({"time" : curren_time},status=status.HTTP_200_OK)
    


class ShopAPIView(APIView):
    """ Vue principale en utilisant DRF """

    def get(self, request, *args, **kwargs):
        # Récupérez tous les produits
        produits = Produit.objects.all()

        # Récupérez les données à partir du cookie en utilisant votre fonction `data_cookie`
        data = data_cookie(request)
        nombre_article = data['nombre_article']

        # Sérialisez les produits si nécessaire
        serializer = ProduitSerializer(produits, many=True)

        # Construisez le contexte pour la réponse JSON
        context = {
            'produits': serializer.data,
            'nombre_article': nombre_article
        }

        # Retournez la réponse JSON
        return Response(context, status=status.HTTP_200_OK)
