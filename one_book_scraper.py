# Importation de la fonction de base et de l'URL par défaut depuis le module utilitaire
from scraper_utils import (
        extract_book_data,
        save_to_csv,
        DEFAULT_BOOK_URL
    )

def run_phase1(url=DEFAULT_BOOK_URL):
    """
    Extraction des informations d'un livre unique.
    Récupère les données, puis les sauvegarde dans un fichier CSV dédié.
    """
    
    print(f"\n--- Phase 1 : Extraction d'un seul livre ---")
    print(f"Cible: {url}")

    #Extraction des données du livre
    data = extract_book_data(url)
    
    #Sauvegarde si l'extraction a réussi
    if data:
        save_to_csv([data], "book.csv")
        print(f"Succès ! Livre '{data['title']}' sauvegardé dans book.csv")
    return data
