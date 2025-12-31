import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin
from one_book_scraper import extract_book_data
from category_books_scraper import get_books_urls_from_category


def get_all_categories_links(base_url):
    """
    Récupère la liste de toutes les catégories du site depuis la barre latérale.
    """
    categories = []
    # Requête vers la page d'accueil
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de charger la page (Code {response.status_code})")
        # la page inaccessible  donc le meilleur est de retourner une liste actuelle vide
        return categories
        
    # Parse HTML de la page d'accueil
    soup = BeautifulSoup(response.content, 'html.parser')
    # On cherche le conteneur des catégories dans la barre de navigation à gauche qui est dans une <ul class='nav-list'>
    nav_list = soup.find('ul', class_='nav-list').find('ul')
    # On récupère tous les liens de catégories
    links = nav_list.find_all('a')
    # On parcourt chaque lien pour extraire le nom et l'URL
    for link in links:
        category_name = link.text.strip()
        category_link = urljoin(base_url, link.get('href'))
        categories.append({"name": category_name, "url": category_link})
        print(f" {len(categories)} catégories trouvées au total.")

    return categories

def save_to_csv(books_data, filename):
    headers = [
        "product_page_url", "universal_product_code", "title",
        "price_including_tax", "price_excluding_tax", "number_available",
        "product_description", "category", "review_rating", "image_url"
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(books_data)

if __name__ == "__main__":
    BASE_URL = "http://books.toscrape.com/"
    # On récupère la liste des catégories
    categories_list = get_all_categories_links(BASE_URL)
    # On boucle sur chaque catégorie
    for category in categories_list:
        # Récupération des liens des livres dans la catégorie
        books_urls = get_books_urls_from_category(category['url'])
        # Extraction des données
        books_data = []
        for index, url in enumerate(books_urls, 1):
            print(f" [{index}/{len(books_urls)}] Extraction de : {url}")
            extracted_data = extract_book_data(url)
            if extracted_data: 
                books_data.append(extracted_data)

        # Sauvegarde dans un CSV séparé par catégorie
        if books_data:
            file_name= f"{category['name'].lower().replace(' ', '_')}.csv"
            save_to_csv(books_data, file_name)
            print(f" Phase 3 terminée : fichiers des toutes les len({categories_list})catégories avec leur contenu créés avec succès.")

