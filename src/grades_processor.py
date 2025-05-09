import csv
import statistics

def lire_coefficients(fichier_coefficients):
    """Lit les coefficients des matières depuis un fichier CSV."""
    coefficients = {}
    with open(fichier_coefficients, mode='r', newline='', encoding='utf-8') as fichier_csv:
        lecteur = csv.DictReader(fichier_csv)
        for ligne in lecteur:
            if ligne['Libelle'] == 'Coeff':  # On s'intéresse uniquement à la ligne des coefficients
                for matiere, coef in ligne.items():
                    if matiere != 'Libelle':  # Ignorer la colonne "Libelle"
                        try:
                            coefficients[matiere] = int(coef)
                        except ValueError:
                            raise ValueError(f"Le coefficient pour la matière '{matiere}' n'est pas un entier valide.")
    return coefficients

def process_grades(input_file, coeff_file):
    """
    Ce script traite les données des étudiants, calcule les moyennes pondérées, les rangs et génère deux fichiers CSV :
    1. traitement.csv : Contient les notes, moyennes pondérées et rangs des étudiants.
    2. analyse.csv : Contient les statistiques par matière et pour la classe.
    """
    # Lecture des coefficients
    coefficients = lire_coefficients(coeff_file)

    # --- Étape 1 : Lire et traiter les données des étudiants ---
    etudiants_data = []
    matieres = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as fichier_csv:
        lecteur_dict = csv.DictReader(fichier_csv)

        if lecteur_dict.fieldnames:
            for colonne in lecteur_dict.fieldnames:
                if colonne not in ('Nom', 'Prenom', 'ID_Etudiant'):
                    matieres.append(colonne)

        for ligne_dict in lecteur_dict:
            etudiant = {'Nom': ligne_dict['Nom'], 'Prenom': ligne_dict['Prenom'], 'ID_Etudiant': ligne_dict['ID_Etudiant']}
            notes_numeriques = []

            for matiere in matieres:
                note_str = ligne_dict.get(matiere)
                try:
                    note_float = float(note_str)
                    etudiant[matiere] = note_float
                    notes_numeriques.append(note_float)
                except ValueError:
                    etudiant[matiere] = None

            etudiant['notes_valides'] = notes_numeriques
            etudiants_data.append(etudiant)

    # --- Étape 2 : Calculer les moyennes pondérées et les rangs ---
    for etudiant in etudiants_data:
        somme_notes_ponderees = 0
        somme_coefficients = 0
        for matiere in matieres:
            note = etudiant.get(matiere)
            coef = coefficients.get(matiere, 0)  # Récupère le coefficient ou 0 si absent
            if note is not None:
                somme_notes_ponderees += note * coef
                somme_coefficients += coef
        etudiant['Moyenne_Generale'] = round(somme_notes_ponderees / somme_coefficients, 2) if somme_coefficients > 0 else None

    # Calcul des rangs par matière
    for matiere in matieres:
        notes_matiere = [etudiant.get(matiere) for etudiant in etudiants_data]
        rangs_matiere = calculer_rangs(notes_matiere)
        for i, etudiant in enumerate(etudiants_data):
            etudiant[f'{matiere}_Rang'] = rangs_matiere[i]

    moyennes_generales = [e.get('Moyenne_Generale') for e in etudiants_data]
    rangs_generaux = calculer_rangs(moyennes_generales)
    
    for i, etudiant in enumerate(etudiants_data):
        etudiant['Rang_General'] = rangs_generaux[i]

    moyennes_classe_par_matiere = {}
    for matiere in matieres:
        notes_valides = [e.get(matiere) for e in etudiants_data if e.get(matiere) is not None]
        moyennes_classe_par_matiere[matiere] = round(statistics.mean(notes_valides), 2) if notes_valides else 0

    moyenne_generale_classe = round(statistics.mean([e['Moyenne_Generale'] for e in etudiants_data if e['Moyenne_Generale'] is not None]), 2)

    # --- Étape 3 : Générer les fichiers de sortie ---
    traitement_file = 'traitement.csv'
    analyse_file = 'analyse.csv'

    # Générer traitement.csv
    with open(traitement_file, mode='w', newline='', encoding='utf-8') as fichier_sortie:
        writer = csv.writer(fichier_sortie)
        # header = ['ID_Etudiant', 'Nom', 'Prenom'] + [f'{matiere}_Note' for matiere in matieres] + ['Moyenne_Generale', 'Rang_General']
        header = ['ID_Etudiant', 'Nom', 'Prenom']
        for matiere in matieres:
            header.append(f'{matiere}_Note')  # Colonne pour la note
            header.append(f'{matiere}_Rang')  # Colonne pour le rang
        header += ['Moyenne_Generale', 'Rang_General']
        writer.writerow(header)

        for etudiant in etudiants_data:
            # ligne = [etudiant['ID_Etudiant'], etudiant['Nom'], etudiant['Prenom']] + [etudiant.get(matiere) for matiere in matieres] + [etudiant.get('Moyenne_Generale'), etudiant.get('Rang_General')]
            ligne = [etudiant['ID_Etudiant'], etudiant['Nom'], etudiant['Prenom']]
            for matiere in matieres:
                # Ajouter la note
                note = etudiant.get(matiere)
                ligne.append(f"{note:.2f}" if note is not None else "")
                # Ajouter le rang
                rang = etudiant.get(f'{matiere}_Rang')
                ligne.append(rang if rang is not None else "")
            # Ajouter la moyenne générale et le rang général
            moyenne_generale = etudiant.get('Moyenne_Generale')
            ligne.append(f"{moyenne_generale:.2f}" if moyenne_generale is not None else "")
            ligne.append(etudiant.get('Rang_General', ""))
            writer.writerow(ligne)

        # --- NOUVELLE Partie : Ajouter la ligne des moyennes de classe ---
        ligne_classe = []
        ligne_classe.append("")  # Colonne ID_Etudiant vide
        ligne_classe.append("Classe")  # Colonne Nom
        ligne_classe.append("")  # Colonne Prenom vide

        for matiere in matieres:
            moy_classe_mat = moyennes_classe_par_matiere.get(matiere, 0)
            ligne_classe.append(f"{moy_classe_mat:.2f}")
            ligne_classe.append("-")  # Placeholder pour le rang de la classe dans la matière
        ligne_classe.append(f"{moyenne_generale_classe:.2f}")  # Moyenne générale de la classe
        ligne_classe.append("-")  # Placeholder pour le rang général de la classe
        writer.writerow(ligne_classe)

    # Générer analyse.csv
    analyse_par_matiere = []
    for matiere in matieres:
        stats_matiere = {'Matière': matiere}  # Dictionnaire pour cette matière
        notes_valides = [e.get(matiere) for e in etudiants_data if e.get(matiere) is not None]  # Récupère les notes valides
        moyenne_classe_actuelle = moyennes_classe_par_matiere.get(matiere, 0)  # Récupère la moyenne déjà calculée

        # Initialiser les stats avec une valeur par défaut ('-')
        stats_matiere['Note min'] = '-'
        stats_matiere['Note Max'] = '-'
        stats_matiere['Moyenne Classe'] = '-'
        stats_matiere['Effectif Moyenne>10'] = 0  # Commencer le comptage à 0
        stats_matiere['Effectif Moyenne > Moyenne Classe'] = 0  # Commencer le comptage à 0
        stats_matiere['Médiane'] = '-'
        stats_matiere['Écart Type'] = '-'

        if notes_valides:  # Effectuer les calculs uniquement si des notes valides existent
            # Calculs Min/Max
            min_note = min(notes_valides)
            max_note = max(notes_valides)
            stats_matiere['Note min'] = f"{min_note:.2f}"
            stats_matiere['Note Max'] = f"{max_note:.2f}"

            # Moyenne
            stats_matiere['Moyenne Classe'] = f"{moyenne_classe_actuelle:.2f}"

            # Effectifs
            eff_sup_10 = sum(1 for note in notes_valides if note >= 10)
            stats_matiere['Effectif Moyenne>10'] = eff_sup_10

            eff_sup_moy = sum(1 for note in notes_valides if note >= moyenne_classe_actuelle)
            stats_matiere['Effectif Moyenne > Moyenne Classe'] = eff_sup_moy

            # Médiane
            median_note = statistics.median(notes_valides)
            stats_matiere['Médiane'] = f"{median_note:.2f}"

            # Écart Type
            if len(notes_valides) > 1:  # L'écart type nécessite au moins deux valeurs
                stdev_note = statistics.stdev(notes_valides)
                stats_matiere['Écart Type'] = f"{stdev_note:.2f}"

        analyse_par_matiere.append(stats_matiere)  # Ajoute les stats de cette matière à la liste

    # --- NOUVELLE PARTIE : Calcul des Statistiques Globales de la Classe ---
    stats_classe_generale = {
        'Matière': "Classe",
        'Note min': '-',
        'Note Max': '-',
        'Moyenne Classe': '-',
        'Médiane': '-',
        'Écart Type': '-',
        'Effectif Moyenne>10': '-',
        'Effectif Moyenne > Moyenne Classe': '-'
    }

    # Ajouter la moyenne générale de la classe à la liste des moyennes valides
    moyennes_generales_valides = [e['Moyenne_Generale'] for e in etudiants_data if e['Moyenne_Generale'] is not None]
    moyennes_generales_valides.append(moyenne_generale_classe)

    if moyennes_generales_valides:
        # Min / Max
        min_moy_gen = min(moyennes_generales_valides)
        max_moy_gen = max(moyennes_generales_valides)
        stats_classe_generale['Note min'] = f"{min_moy_gen:.2f}"
        stats_classe_generale['Note Max'] = f"{max_moy_gen:.2f}"

        # Moyenne (déjà calculée : moyenne_generale_classe)
        stats_classe_generale['Moyenne Classe'] = f"{moyenne_generale_classe:.2f}"

        # Effectifs
        eff_gen_sup_10 = sum(1 for moy in moyennes_generales_valides if moy >= 10)
        stats_classe_generale['Effectif Moyenne>10'] = eff_gen_sup_10

        eff_gen_sup_moy_classe = sum(1 for moy in moyennes_generales_valides if moy >= moyenne_generale_classe)
        stats_classe_generale['Effectif Moyenne > Moyenne Classe'] = eff_gen_sup_moy_classe

        # Médiane
        median_moy_gen = statistics.median(moyennes_generales_valides)
        stats_classe_generale['Médiane'] = f"{median_moy_gen:.2f}"

        # Écart Type
        if len(moyennes_generales_valides) > 1:
            stdev_moy_gen = statistics.stdev(moyennes_generales_valides)
            stats_classe_generale['Écart Type'] = f"{stdev_moy_gen:.2f}"

    # Ajouter le dictionnaire des stats globales à la liste principale
    analyse_par_matiere.append(stats_classe_generale)

    # Générer analyse.csv
    with open(analyse_file, mode='w', newline='', encoding='utf-8') as fichier_analyse:
        writer = csv.DictWriter(fichier_analyse, fieldnames=['Matière', 'Note min', 'Note Max', 'Moyenne Classe', 'Médiane', 'Écart Type', 'Effectif Moyenne>10', 'Effectif Moyenne > Moyenne Classe'])
        writer.writeheader()
        writer.writerows(analyse_par_matiere)

    return traitement_file, analyse_file


def calculer_rangs(liste_moyennes):
    """
    Calcule les rangs pour une liste de moyennes (ou autres valeurs numériques).
    La moyenne la plus élevée obtient le rang "1er".
    Gère les égalités en ajoutant " ex" (ex: "2e", "3e ex", "3e ex", "5e").
    
    Args:
        liste_moyennes: Une liste de nombres (int ou float) représentant les moyennes.

    Returns:
        Une liste de chaînes de caractères représentant les rangs formatés.
    """
    # Associer chaque moyenne à son index original
    moyennes_avec_index = [(moyenne, index) for index, moyenne in enumerate(liste_moyennes)]

    # Trier les moyennes par ordre décroissant
    moyennes_triees = sorted(moyennes_avec_index, key=lambda item: item[0], reverse=True)

    # Initialiser la liste des rangs finaux
    rangs_finaux = [""] * len(liste_moyennes)

    # Parcourir les moyennes triées pour calculer les rangs
    i = 0  # Indice dans la liste triée
    while i < len(moyennes_triees):
        # Moyenne actuelle et rang numérique
        moyenne_actuelle = moyennes_triees[i][0]
        rang_numerique = i + 1

        # Compter les ex aequo
        j = i
        while j < len(moyennes_triees) and moyennes_triees[j][0] == moyenne_actuelle:
            j += 1
        nombre_ex_aequo = j - i

        # Construire le texte du rang
        if rang_numerique == 1:
            suffixe = "er"
        else:
            suffixe = "e"
        if nombre_ex_aequo > 1:
            suffixe += " ex"
        rang_formate = f"{rang_numerique}{suffixe}"

        # Assigner le rang formaté aux indices originaux
        for k in range(i, j):
            index_original = moyennes_triees[k][1]
            rangs_finaux[index_original] = rang_formate

        # Passer au groupe suivant
        i = j

    return rangs_finaux