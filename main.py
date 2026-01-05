# Importation  des constantes nécessaires
from scraper_utils import (
    DEFAULT_BOOK_URL,
    DEFAULT_CATEGORY_URL,
    BASE_URL
)
# Importation des modules de phase (Chaque fichier gère une étape spécifique du scraping)
from one_book_scraper import run_phase1
from category_books_scraper import run_phase2
from all_categories_scraper import run_phase3
from scraper_images import run_phase4

def main():
    # Préparation des noms pour l'affichage dynamique dans le menu
    # On extrait le nom du livre et de la catégorie à partir des URLs par défaut
    book_name = DEFAULT_BOOK_URL.split('/')[-2].replace('-', ' ').title()
    cat_name = DEFAULT_CATEGORY_URL.split('/')[-2].split('_')[0].title()

    # Boucle infinie pour maintenir le menu affiché tant que l'utilisateur ne quitte pas
    while True:
        # Affichage du menu principal
        print("\n=== Système de surveillance des prix Books Online ===")
        print(f"1. Phase 1 : Extraire le livre '{book_name}'")
        print(f"2. Phase 2 : Extraire la catégorie '{cat_name}'")
        print(f"3. Phase 3 : Extraire TOUTES les catégories (CSV uniquement)")
        print(f"4. Phase 4 : Télécharger TOUTES les images")
        print("q. Quitter")

        # Récupération du choix utilisateur
        choice = input("\nChoisissez une option : ").strip().lower()
        
        # Traitement du choix
        if choice == '1':
            run_phase1(DEFAULT_BOOK_URL)
        elif choice == '2':
            run_phase2(DEFAULT_CATEGORY_URL)
        elif choice == '3':
            run_phase3()
        elif choice == '4':
            run_phase4()
        elif choice == 'q':
            # Sortie  du programme
            print("no more scraping =====! !")
            break
        else:
            # Gestion d'une saisie erronée
            print("Option invalide, veuillez réessayer.")
# Vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    # Lance la fonction principale qui gère le menu et les phases
    main()
