from rest_framework import serializers

from App.models import Client, Category, Produit, Commande, CommandeArticle, AddressChipping

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProduitSerializer(serializers.ModelSerializer):
    # Utilisez la CategorySerializer pour sérialiser la catégorie
    categorie = CategorySerializer()

    class Meta:
        model = Produit
        fields = ['id', 'categorie', 'name', 'price', 'digital', 'image', 'date_ajout', 'imageUrl']


class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = ['id', 'client', 'date_commande', 'complete', 'transaction_id', 'status', 'total_trans']


class CommandeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeArticle
        fields = ['id', 'produit', 'commande', 'quantite', 'date_added', 'get_total']


class AddressChippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressChipping
        fields = ['id', 'client', 'commande', 'addresse', 'ville', 'zipcode', 'date_ajout']

# serializers.py

