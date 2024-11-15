import tkinter as tk
from tkinter import ttk, messagebox
import csv
import heapq
from math import inf

class MetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Réseau Métro")
        self.root.geometry("800x600")
        
        self.graphe = self.creerGraphe()
        self.stations = self.lecture_stations()
        
        # Vérification de la connexité dès le démarrage
        connexite = "connexe" if self.est_connexe(self.graphe) else "non connexe"
        
        # Interface
        self.create_widgets(connexite)
        
    def create_widgets(self, connexite):
        # Label pour la connexité
        tk.Label(self.root, text=f"Le réseau est {connexite}", font=('Arial', 14)).pack(pady=10)
        
        # Frame pour la recherche d'itinéraire
        frame = ttk.LabelFrame(self.root, text="Recherche d'itinéraire", padding=10)
        frame.pack(padx=10, pady=5, fill="x")
        
        # Combobox pour les stations
        stations_noms = sorted([data['nom'] for data in self.stations.values()])
        
        # Départ
        tk.Label(frame, text="Station de départ:").grid(row=0, column=0, padx=5, pady=5)
        self.depart_var = tk.StringVar()
        self.depart_combo = ttk.Combobox(frame, textvariable=self.depart_var, values=stations_noms)
        self.depart_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Arrivée
        tk.Label(frame, text="Station d'arrivée:").grid(row=1, column=0, padx=5, pady=5)
        self.arrivee_var = tk.StringVar()
        self.arrivee_combo = ttk.Combobox(frame, textvariable=self.arrivee_var, values=stations_noms)
        self.arrivee_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Bouton recherche
        ttk.Button(frame, text="Rechercher itinéraire", command=self.rechercher_itineraire).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Zone de résultat
        self.result_text = tk.Text(self.root, height=15, width=70)
        self.result_text.pack(padx=10, pady=10)
        
        # Bouton ACM
        ttk.Button(self.root, text="Afficher l'arbre couvrant minimum", command=self.afficher_acm).pack(pady=5)

    def rechercher_itineraire(self):
        depart = self.depart_var.get()
        arrivee = self.arrivee_var.get()
        
        debut_id = next((id for id, data in self.stations.items() if data['nom'] == depart), None)
        fin_id = next((id for id, data in self.stations.items() if data['nom'] == arrivee), None)
        
        if not debut_id or not fin_id:
            messagebox.showerror("Erreur", "Stations invalides")
            return
            
        chemin, temps = self.belmann(self.graphe, self.stations, debut_id, fin_id)
        self.afficher_itineraire(chemin, temps)

    def afficher_itineraire(self, chemin, temps):
        self.result_text.delete(1.0, tk.END)
        if chemin is None:
            self.result_text.insert(tk.END, "Aucun chemin trouvé.")
            return

        ligne_courante = self.stations[chemin[0]]['ligne']
        self.result_text.insert(tk.END, f"Itinéraire :\n")
        self.result_text.insert(tk.END, f"- Départ : {self.stations[chemin[0]]['nom']} (Ligne {ligne_courante})\n")

        for i in range(1, len(chemin)):
            station = chemin[i]
            nouvelle_ligne = self.stations[station]['ligne']
            if nouvelle_ligne != ligne_courante:
                self.result_text.insert(tk.END, f"- Changement à {self.stations[chemin[i-1]]['nom']}\n")
                self.result_text.insert(tk.END, f"  Prendre la ligne {nouvelle_ligne}\n")
                ligne_courante = nouvelle_ligne

        self.result_text.insert(tk.END, f"- Arrivée : {self.stations[chemin[-1]]['nom']} (Ligne {ligne_courante})\n")
        self.result_text.insert(tk.END, f"Temps de trajet : {self.formater_temps(temps)}")

    def afficher_acm(self):
        self.result_text.delete(1.0, tk.END)
        poids = self.arbre_couvrant_prim(self.graphe, self.stations)
        self.result_text.insert(tk.END, f"\nPoids total de l'arbre couvrant minimum : {poids}")

    # Méthodes utilitaires reprises du code original
    def creerGraphe(self):
        graph = {}
        with open('utils/connections.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                Station1, Station2, temps = row
                temps = int(temps)
                if Station1 not in graph:
                    graph[Station1] = []
                if Station2 not in graph:
                    graph[Station2] = []
                graph[Station1].append((Station2, temps))
                graph[Station2].append((Station1, temps))
        return graph

    def lecture_stations(self):
        stations = {}
        with open('utils/stations.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                id_station = str(int(row[0]))
                stations[id_station] = {'nom': row[1], 'ligne': row[2]}
        return stations

    def dfs(self, graph, debut, visite=None):
        if visite is None:
            visite = set()
        visite.add(debut)
        for voisin, _ in graph.get(debut, []):
            if voisin not in visite:
                self.dfs(graph, voisin, visite)
        return visite

    def est_connexe(self, graph):
        station_depart = next(iter(graph))
        stations_visitees = self.dfs(graph, station_depart)
        return len(stations_visitees) == len(graph)

    def arbre_couvrant_prim(self, graph, stations):
        sommet_depart = next(iter(graph))
        visite = set([sommet_depart])
        edges = [(cost, sommet_depart, to) for to, cost in graph[sommet_depart]]
        heapq.heapify(edges)
        poids = 0
        mst_edges = []

        while edges:
            cost, frm, to = heapq.heappop(edges)
            if to not in visite:
                visite.add(to)
                poids += cost
                mst_edges.append((frm, to, cost))
                for to_next, cost in graph[to]:
                    if to_next not in visite:
                        heapq.heappush(edges, (cost, to, to_next))

        self.result_text.insert(tk.END, "Liaisons de l'arbre couvrant minimum :\n")
        for frm, to, cost in mst_edges:
            self.result_text.insert(tk.END, f"- {stations[frm]['nom']} -> {stations[to]['nom']} avec coût {cost}\n")

        return poids

    def belmann(self, graph, stations, debut_id, fin_id):
        distances = {node: inf for node in graph}
        predecesseurs = {node: None for node in graph}
        distances[debut_id] = 0

        for _ in range(len(graph) - 1):
            for node in graph:
                for voisin, poids in graph[node]:
                    if distances[node] + poids < distances[voisin]:
                        distances[voisin] = distances[node] + poids
                        predecesseurs[voisin] = node

        if distances[fin_id] == inf:
            return None, inf

        chemin = []
        current = fin_id
        while current is not None:
            chemin.insert(0, current)
            current = predecesseurs[current]

        return chemin, distances[fin_id]

    def formater_temps(self, secondes):
        minutes = (secondes % 3600) // 60
        return f"{minutes}min"

if __name__ == "__main__":
    root = tk.Tk()
    app = MetroApp(root)
    root.mainloop()