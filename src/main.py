import tkinter as tk
from tkinter import filedialog, messagebox
from grades_processor import process_grades
import csv
import matplotlib.pyplot as plt
from tkinter import ttk

def select_files():
    """Permet à l'utilisateur de sélectionner les fichiers CSV de notes et de coefficients."""
    global notes_file, coeff_file  # Déclare les variables comme globales
    # Sélection du fichier de notes
    notes_file = filedialog.askopenfilename(
        title="Sélectionnez le fichier de notes",
        filetypes=[("Fichiers CSV", "*.csv")]
    )
    if not notes_file:
        messagebox.showwarning("Attention", "Vous devez sélectionner un fichier de notes.")
        return

    # Sélection du fichier de coefficients
    coeff_file = filedialog.askopenfilename(
        title="Sélectionnez le fichier des coefficients",
        filetypes=[("Fichiers CSV", "*.csv")]
    )
    if not coeff_file:
        messagebox.showwarning("Attention", "Vous devez sélectionner un fichier de coefficients.")
        return

# Activer le bouton pour générer les fichiers
    generate_button.config(state="normal")

def generate_files():
    """Génère les fichiers traitement.csv et analyse.csv avec une barre de progression."""
    try:
        progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()
        
        global traitement_file, analyse_file
        traitement_file, analyse_file = process_grades(notes_file, coeff_file)
        progress.stop()
        progress.destroy()
        # Afficher un message de succès
        messagebox.showinfo(
            "Succès",
            f"Les fichiers ont été générés avec succès :\n\n"
            f"- {traitement_file}\n- {analyse_file}"
        )
        # Activer le bouton pour afficher les graphiques
        graph_button.config(state="normal")
    except Exception as e:
        progress.stop()
        progress.destroy()
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        
def show_graphs():
    """Affiche les graphiques basés sur les données du fichier analyse.csv."""
    try:
        # Lire les données du fichier analyse.csv
        with open(analyse_file, mode='r', newline='', encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier)
            matieres = [ligne['Matière'] for ligne in lecteur]
            fichier.seek(0)  # Revenir au début du fichier pour relire les données
            next(lecteur)  # Sauter l'en-tête

            # Préparer les données pour les graphiques
            stats = {
                'Moyenne Classe': [],
                'Note min': [],
                'Note Max': [],
                'Effectif Moyenne>10': [],
                'Effectif Moyenne > Moyenne Classe': [],
                'Matières': []
            }

            for ligne in lecteur:
                stats['Matières'].append(ligne['Matière'])
                stats['Moyenne Classe'].append(float(ligne['Moyenne Classe']))
                stats['Note min'].append(float(ligne['Note min']))
                stats['Note Max'].append(float(ligne['Note Max']))
                stats['Effectif Moyenne>10'].append(int(ligne['Effectif Moyenne>10']))
                stats['Effectif Moyenne > Moyenne Classe'].append(int(ligne['Effectif Moyenne > Moyenne Classe']))

        # Créer un graphique pour les moyennes par matière
        plt.figure(figsize=(10, 6))
        plt.bar(stats['Matières'], stats['Moyenne Classe'], color='blue', alpha=0.7, label='Moyenne Classe')
        plt.plot(stats['Matières'], stats['Note min'], marker='o', color='red', label='Note Min')
        plt.plot(stats['Matières'], stats['Note Max'], marker='o', color='green', label='Note Max')
        plt.title("Statistiques par Matière")
        plt.xlabel("Matières")
        plt.ylabel("Valeurs")
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()

        # Créer un diagramme à bandes pour les effectifs
        plt.figure(figsize=(10, 6))
        bar_width = 0.4
        x = range(len(stats['Matières']))

        plt.bar(x, stats['Effectif Moyenne>10'], width=bar_width, color='purple', alpha=0.7, label='Effectif Moyenne > 10')
        plt.bar(
            [i + bar_width for i in x],
            stats['Effectif Moyenne > Moyenne Classe'],
            width=bar_width,
            color='orange',
            alpha=0.7,
            label='Effectif Moyenne > Moyenne Classe'
        )

        plt.title("Effectifs par Matière")
        plt.xlabel("Matières")
        plt.ylabel("Effectifs")
        plt.xticks([i + bar_width / 2 for i in x], stats['Matières'], rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()

        # Afficher les graphiques
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'affichage des graphiques : {e}")

def create_ui():
    """Crée l'interface utilisateur principale."""
    global root  # Déclare root comme une variable globale
    root = tk.Tk()
    root.title("Application de Gestion des Notes")
    root.geometry("500x400")
    root.resizable(False, False)

    # Titre principal
    title_label = tk.Label(
        root,
        text="Bienvenue dans l'Application de Gestion des Notes",
        font=("Helvetica", 14, "bold"),
        fg="#2c3e50"
    )
    title_label.pack(pady=20)

    # Description
    description_label = tk.Label(
        root,
        text="Cette application vous permet de traiter les fichiers de notes\n"
            "et de générer des rapports détaillés.",
        font=("Helvetica", 10),
        fg="#34495e"
    )
    description_label.pack(pady=10)

    # Bouton pour sélectionner les fichiers
    select_button = tk.Button(
        root,
        text="Sélectionner les fichiers de notes et de coefficients",
        font=("Helvetica", 12),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        command=select_files
    )
    select_button.pack(pady=10)
    # Bouton pour générer les fichiers
    global generate_button
    generate_button = tk.Button(
        root,
        text="Générer les fichiers",
        font=("Helvetica", 12),
        bg="#2ecc71",
        fg="white",
        activebackground="#27ae60",
        activeforeground="white",
        command=generate_files,
        state="disabled"
    )
    generate_button.pack(pady=10)

    # Bouton pour afficher les graphiques
    global graph_button
    graph_button = tk.Button(
        root,
        text="Afficher les graphiques",
        font=("Helvetica", 12),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        activeforeground="white",
        command=show_graphs,
        state="disabled"
    )
    graph_button.pack(pady=10)
    # Pied de page
    footer_label = tk.Label(
        root,
        text="Développé par KABLAM - 05_05_2025",
        font=("Helvetica", 8),
        fg="#7f8c8d"
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
