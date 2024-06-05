import sys
from matplotlib import pyplot as plt
from matplotlib.widgets import Button, Slider
import random
import numpy as np

class TSP_GEN:
    # Initialisation des variables
    nb_villes = int
    taille_population = int
    villes = []

    # Constructeur de la classe
    def __init__(self):
        self.nb_villes = 10
        self.taille_population = 2500
        self.villes = self.generation_villes()

    # Fonction pour générer les coordonnées des villes
    def generation_villes(self):
        return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(self.nb_villes)]

    # Fonction pour calculer la distance entre deux villes
    def distance_villes(self, ville1, ville2):
        return np.linalg.norm(np.array(ville1) - np.array(ville2))

    # Fonction pour calculer la longueur d'un chemin
    def longueur_chemin(self, chemin, dist_villes):
        distance = 0
        # Parcours de chaque paire successive de villes dans le chemin
        for i in range(0, len(chemin)):
            # Ajout de la distance entre les deux villes à la distance totale
            distance += dist_villes[chemin[i - 1]][chemin[i]]
        return distance

    # Fonction pour initialiser une population d'individus (chemins)
    def initialiser_population(self):
        population = []
        for _ in range(self.taille_population):
            # Création d'une liste des villes (individu/chemin)
            chemin = list(range(self.nb_villes))
            # Mélange de la liste
            random.shuffle(chemin)
            # Ajout de la liste/chemin/individu à la population
            population.append(chemin)
        return population

    # Fonction pour sélectionner les parents en utilisant la méthode de tournoi
    def selection_tournoi(self, population, dist_villes, taille_tournoi):
        meilleurs_parents = []
        # Sélection de deux parents
        for _ in range(2):  
            # Sélection d'un sous-ensemble aléatoire d'individus
            tournoi = random.sample(population, taille_tournoi)
            # Sélection de l'individu le plus performant du sous-ensemble (chemin le plus court)
            parent = min(tournoi, key=lambda chemin: self.longueur_chemin(chemin, dist_villes))
            meilleurs_parents.append(parent)
        return meilleurs_parents[0], meilleurs_parents[1]

    # Fonction pour croiser deux parents afin de produire des enfants
    def croisement(self, parent1, parent2):
        # Définition du point de croisement de manière aléatoire
        point_de_croisement = random.randint(0, len(parent1) - 1)
        # Concaténation des gènes des parents pour créer les enfants
        enfant1 = parent1[:point_de_croisement] + [gene for gene in parent2 if gene not in parent1[:point_de_croisement]]
        enfant2 = parent2[:point_de_croisement] + [gene for gene in parent1 if gene not in parent2[:point_de_croisement]]
        return enfant1, enfant2

    # Fonction pour effectuer une mutation sur un chemin
    def mutation(self, chemin, mutation_prob):
        # Test de probabilité pour savoir si une mutation doit avoir lieue
        if random.random() < mutation_prob:
            # Sélection aléatoire des 2 villes à interchanger
            indices = random.sample(range(len(chemin)), 2)
            # Interchangement des villes sélectionnées
            chemin[indices[0]], chemin[indices[1]] = chemin[indices[1]], chemin[indices[0]]
        return chemin

    # Fonction pour résoudre le TSP en utilisant un algorithme génétique
    def tsp_genetique(self, nb_generations, taille_tournoi, ax, button_renouv, button_meme, mutation_prob=0.05):
        # Création de la matrice des distances entre chaques villes
        dist_villes = np.array([[self.distance_villes(v1, v2) for v2 in self.villes] for v1 in self.villes])
        # Affichage de la matrice
        print(dist_villes)
        # Création de la première génération d'individus
        population = self.initialiser_population()
        # Initialisation des variables de résultat
        meilleur_chemin = population[0]
        meilleure_longueur = self.longueur_chemin(meilleur_chemin, dist_villes)

        # Actions du bouton "Nouvelles villes"
        def action_renouv(event):
            # Génération des nouvelles villes
            self.villes = self.generation_villes()
            # On relance la fonction avec les paramètres mis à jour
            self.tsp_genetique(nb_generations, taille_tournoi, ax, button_renouv, button_meme)

        # Actions du bouton "Mêmes villes"
        def action_meme(event):
            # On relance la fonction
            self.tsp_genetique(nb_generations, taille_tournoi, ax, button_renouv, button_meme)

        # Fonction d'arrêt du programme à la fermeture
        def on_close(event):
            # Fermeture de Pyplot et du programme
            plt.close()
            sys.exit()
        # Capture de l'événement de fermeture de la fenêtre
        fig.canvas.mpl_connect('close_event', on_close)

        # Capture des évènements de bouton cliqué
        button_renouv.on_clicked(action_renouv)
        button_meme.on_clicked(action_meme)


        for generation in range(nb_generations):
            nouvelle_population = []
            # On génère des individus jusqu'à ce que la nouvelle population ait la taille souhaitée
            while len(nouvelle_population) < self.taille_population:
                # Sélection des parents
                parent1, parent2 = self.selection_tournoi(population, dist_villes, taille_tournoi)
                # Création des enfants
                enfant1, enfant2 = self.croisement(parent1, parent2)
                # Mutation des enfant avec probabilité
                enfant1 = self.mutation(enfant1, mutation_prob)
                enfant2 = self.mutation(enfant2, mutation_prob)
                # Ajout des enfants à la nouvelle population
                nouvelle_population.extend([enfant1, enfant2])
            # remplacement de la population actuelle par la nouvelle population
            population = nouvelle_population

            # Parcours de tous les chemins de la population
            for chemin in population:
                # Calcul de la longueur du chemin
                longueur = self.longueur_chemin(chemin, dist_villes)
                # Comparaison de la longueur du chemin avec le meilleur chemin trouvé
                if longueur < meilleure_longueur:
                    # Remplacement du meilleur chemin
                    meilleur_chemin = chemin
                    meilleure_longueur = longueur

            # Affichage des résultats
            # Nettoyage du graphique
            ax.clear()
            # Affichage des villes en bleu
            for ville in self.villes:
                ax.plot(ville[0], ville[1], 'bo')
            # # Affichage du premier chemin de la population actuelle
            # for i in range(0, len(population[0])):
            #     ville1 = self.villes[population[0][i - 1]]
            #     ville2 = self.villes[population[0][i]]
            #     ax.plot([ville1[0], ville2[0]], [ville1[1], ville2[1]], 'g--')
            # Affichage du meilleur chemin en rouge
            for i in range(0, len(meilleur_chemin)):
                ville1 = self.villes[meilleur_chemin[i - 1]]
                ville2 = self.villes[meilleur_chemin[i]]
                ax.plot([ville1[0], ville2[0]], [ville1[1], ville2[1]], 'r-')
            # Mise en forme de l'affichage
            # masquage des axes du graphique
            ax.axis('off')
            # Affichage du titre du graphique
            ax.set_title(f'Génération {generation + 1} - Longueur du meilleur chemin : {meilleure_longueur:.2f}')
            
            plt.draw()
            plt.pause(0.001)

# Fonction pour mettre à jour le nombre de villes
def update_nb_villes(val):
    tsp_gen.nb_villes = int(val)
    slider_nb_villes.valtext.set_text(str(int(val)))
    button_meme.set_active(False)  # Désactiver le bouton "button_meme"

# Fonction pour mettre à jour la taille de la population
def update_taille_population(val):
    tsp_gen.taille_population = int(val)
    slider_taille_population.valtext.set_text(str(int(val)))

# Fonction pour activer le bouton "button_meme"
def activate_button_meme(event):
    button_meme.set_active(True)

# Créer une instance de TSP_GEN
tsp_gen = TSP_GEN()

# Paramètres
nb_generations = 100000  # Nombre de générations
taille_tournoi = 5  # Taille du tournoi pour la sélection

# Créer la figure pyplot
fig, ax = plt.subplots(figsize=(8, 8))
button_renouv = Button(plt.axes([0.02, 0.02, 0.15, 0.075]), 'Nouvelles villes')
button_meme = Button(plt.axes([0.2, 0.02, 0.15, 0.075]), 'Mêmes villes')

# Ajouter les sliders pour modifier le nombre de villes et la taille de la population
ax_nb_villes = plt.axes([0.45, 0.02, 0.15, 0.03])
ax_taille_population = plt.axes([0.75, 0.02, 0.15, 0.03])
slider_nb_villes = Slider(ax_nb_villes, 'Nb Villes', 5, 50, valinit=tsp_gen.nb_villes, valstep=1)
slider_taille_population = Slider(ax_taille_population, 'Taille Pop', 10, 5000, valinit=tsp_gen.taille_population, valstep=10)

# Lier les sliders aux fonctions de mise à jour
slider_nb_villes.on_changed(update_nb_villes)
slider_taille_population.on_changed(update_taille_population)

# Lier le bouton "Nouvelles villes" à la fonction pour activer le bouton "button_meme"
button_renouv.on_clicked(activate_button_meme)

# Résoudre le TSP en utilisant un algorithme génétique
meilleur_chemin, meilleure_longueur = tsp_gen.tsp_genetique(nb_generations, taille_tournoi, ax, button_renouv, button_meme)

plt.show()