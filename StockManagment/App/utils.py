from .models import *
import json, requests, random, string
from django.contrib.auth.models import User

def panier_cookie(request):
    articles = []

    commande = {
        'get_panier_total':0,
        'get_panier_article':0,
        'produit_physique': True,
    }

    nombre_article = commande['get_panier_article']

    try:
        panier = json.loads(request.COOKIES.get('panier'))
        for obj in panier:

            nombre_article += panier[obj]['qte']

            produit = Produit.objects.get(id=obj)

            total = produit.price * panier[obj]['qte']

            commande['get_panier_article'] += panier[obj]['qte']

            commande['get_panier_total'] += total

            article = {
                'produit': {
                    'pk': produit.id,
                    'name': produit.name,
                    'price': produit.price,
                    'nombre': produit.nombre
                },
                'quantite': panier[obj]['qte'],
                'get_total': total

                }

            articles.append(article)

            if produit.digital == False:
                commande['produit_physique'] = True
                
    except:
        pass

    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return context


def data_cookie(request):

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        articles = commande.commandearticle_set.all()

        nombre_article = commande.get_panier_article

    else:

        cookie_panier = panier_cookie(request)
        articles = cookie_panier['articles']
        commande = cookie_panier['commande']
        nombre_article = cookie_panier['nombre_article']

    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return context


def getDataFromApi(request):
    try:
        url = "http://gestionpersonnel:8000/api/prescriptions/"

        response = requests.get(url)
        
        dataToSave = response.json()

        for elt in dataToSave:

            if not User.objects.filter(username=elt['email']).exists():

                user = User.objects.create_user(username=elt['email'], email=elt['email'], password=elt['Token'])

                user.save()

                
            if Prescription.objects.filter(email=elt['email']).exists():
                pass
            else:
                tmp = Prescription(nom=elt['nom'], prenom=elt['prenom'], age=elt['age'], sexe=elt['sexe'], email=elt['email'],
                                    antecedent=elt['antecedent'], prescription1=elt['prescription1'], prescription2=elt['prescription2'], 
                                    prescription3=elt['prescription3'])
                tmp.save()

            try:
                user = User.objects.get(username=elt['email'])

                client = Client.objects.create(user=user, name=elt["nom"], email=elt['email'])

                print("valid")

            except:
                print('invalid')

        return "SUCCESS"
    
    except:
        return "FAILED"


def generer_mot_de_passe():

    caracteres = string.ascii_letters + string.digits

    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(8))

    return mot_de_passe

