from tkinter import Tk, Label, Button, filedialog, messagebox
import os
from grades_processor import process_grades
import csv
import matplotlib.pyplot as plt

class GradesApp:
    def __init__(self, master):
        self.master = master
        master.title("Application de Gestion des Notes")

        self.label = Label(master, text="Sélectionnez votre fichier de notes :")
        self.label.pack(pady=10)

        self.select_button = Button(master, text="Sélectionner un fichier", command=self.select_file)
        self.select_button.pack(pady=5)

        self.process_button = Button(master, text="Générer les fichiers", command=self.generate_output, state='disabled')
        self.process_button.pack(pady=5)
        
        self.graph_button = Button(master, text="Afficher les graphiques", command=self.show_graphs, state='disabled')
        self.graph_button.pack(pady=5)

        self.notes_file = ""
        self.coeff_file = ""
        self.traitement_file = "traitement.csv"
        self.analyse_file = "analyse.csv"


    def select_files(self):
            self.notes_file = filedialog.askopenfilename(title="Sélectionnez le fichier de notes", filetypes=[("Fichiers CSV", "*.csv")])
            if not self.notes_file:
                messagebox.showwarning("Attention", "Vous devez sélectionner un fichier de notes.")
                return

            self.coeff_file = filedialog.askopenfilename(title="Sélectionnez le fichier des coefficients", filetypes=[("Fichiers CSV", "*.csv")])
            if not self.coeff_file:
                messagebox.showwarning("Attention", "Vous devez sélectionner un fichier de coefficients.")
                return

            self.label.config(text="Fichiers sélectionnés.")
            self.process_button.config(state='normal')

    def generate_output(self):
        try:
            process_grades(self.notes_file, self.coeff_file)
            messagebox.showinfo("Succès", f"Les fichiers ont été générés avec succès :\n\n- {self.traitement_file}\n- {self.analyse_file}")
            self.graph_button.config(state='normal')
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def show_graphs(self):
        try:
            # Lire les données du fichier traitement.csv
            with open(self.traitement_file, mode='r', newline='', encoding='utf-8') as fichier:
                lecteur = csv.DictReader(fichier)
                matieres = [col for col in lecteur.fieldnames if col.endswith("_Note")]
                donnees = {matiere: [] for matiere in matieres}

                for ligne in lecteur:
                    for matiere in matieres:
                        note = ligne[matiere]
                        if note:
                            donnees[matiere].append(float(note))

            # Créer des graphiques pour chaque matière
            for matiere, notes in donnees.items():
                plt.figure()
                plt.hist(notes, bins=10, color='blue', alpha=0.7)
                plt.title(f"Distribution des notes pour {matiere}")
                plt.xlabel("Notes")
                plt.ylabel("Fréquence")
                plt.grid(True)

            # Afficher les graphiques
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'affichage des graphiques : {e}")

if __name__ == "__main__":
    root = Tk()
    app = GradesApp(root)
    root.mainloop()