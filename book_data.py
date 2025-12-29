import requests
from bs4 import BeautifulSoup
import csv

# URL du livre choisi
url = "https://books.toscrape.com/catalogue/wuthering-heights_307/index.html"
response = requests.get(url)

# On vérifie si la requête a réussi (code 200)
if response.status_code != 200:
    print(f"Erreur : Impossible de charger la page (Code d'erreur : {response.status_code})")
else:
# Page chargée avec succès. Début du 'parsing' (analyse du HTML).
# BeautifulSoup transforme le texte brut HTML en un objet structuré facile à manipuler
    soup = BeautifulSoup(response.content, 'html.parser')

# Extraction des données
product_page_url = url

# Titre du livre
# On cherche la balise <h1> qui contient le titre du livre
title = soup.find("h1").text.strip()
print(f"Titre du livre trouvé : '{title}'")

# Prix du livre
#  Le tableau 'Product Information' contient l'UPC, les prix et le stock
# On cherche la balise <table> avec la classe 'table-striped'
table = soup.find('table', class_='table-striped')
rows = table.find_all('tr')  # On récupère toutes les lignes (tr = table row)

# Dans ce tableau, chaque donnée est dans une ligne spécifique :
upc = rows[0].find('td').text.strip()             # 1ère ligne : UPC
price_excl_tax = rows[2].find('td').text.strip()  # 3ème ligne : Prix Hors Taxe
price_incl_tax = rows[3].find('td').text.strip()  # 4ème ligne : Prix TTC
# 6ème ligne : Nombre de livres disponibles in stock
number_available = rows[5].find("td").text.strip()
print(f" UPC: {upc},\n Prix HT: {price_excl_tax},\n Prix TTC: {price_incl_tax},\n Disponibilité: {number_available}")

# Description du livre
description_tag = soup.find('div', id='product_description')
if description_tag:
    # find_next('p') cherche la première balise <p> après celle-ci
    product_description = description_tag.find_next('p').text
    print(f"Description du livre : {product_description}")
else:
    product_description = "Pas de description disponible."

# Catégorie du livre
# On la trouve dans le 'breadcrumb' (fil d'ariane) en haut de page
breadcrumb = soup.find('ul', class_='breadcrumb')
links = breadcrumb.find_all('a')
# Les liens sont : Home -> Books -> [Nom de la Catégorie] 
# Vérifie si le breadcrumb existe
if breadcrumb:
    links = breadcrumb.find_all('a')  # Récupère tous les liens <a>
    # La catégorie est normalement le 3ème lien (index 2)
    if len(links) >= 3:
        category = links[2].text.strip()
    else:
        category = "Inconnue"  # Valeur par défaut si pas de catégorie
else:
    category = "Inconnue"  # Valeur par défaut si breadcrumb absent
print(f" Catégorie : {category}")

# Évaluation du livre (Review Rating)
# Elle est définie par une classe CSS "star-rating Three"
rating_tag = soup.find('p', class_='star-rating')
rating_classes = rating_tag.get('class') # Retourne une liste : ['star-rating', 'Three']
review_rating = rating_classes[1] # On prend le 2ème élément qui indique l'évaluation
# Évaluation (Review Rating)
print(f" Review Rating : {review_rating} étoiles")

#IMAGE URL
# On cherche l'image principale dans le conteneur 'item active'
image_tag = soup.find('div', class_='item active').find('img')
image_src = image_tag.get('src')
# L'URL est relative (ex: ../../media/...), on la transforme en URL complète
image_url = f"http://books.toscrape.com/{image_src.replace('../../', '')}"
print(f" URL de l'image : {image_url}")

# Écriture des données dans un fichier CSV
with open("book_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # En-têtes = champs extraits
    writer.writerow([
        "product_page_url",
        "upc",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ])

    # Données extraites
    writer.writerow([
        product_page_url,
        upc,
        title,
        price_incl_tax,
        price_excl_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url
    ])


print("Phase 1 terminée : book_data.csv créé avec succès.")