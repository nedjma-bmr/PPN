from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class Graphe:

    def __init__(self,gdict=None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict


# Get les clés du dictionnaire gdict
    def getSommets(self):
        return list(self.gdict.keys())
# Ajouter un sommet
    def addSommet(self, somm):
        if somm not in self.gdict:
            self.gdict[somm] = []
# Get les arcs du graphe
    def getArcs(self):
        arcs = []
        for somm in self.gdict:
            for nxtsomm in self.gdict[somm]:
                if {nxtsomm, somm} not in arcs:
                    arcs.append({somm, nxtsomm})
        return arcs

    def addArc(self,arc):
    	arc = set(arc)
    	(somm1, somm2) = tuple(arc)
    	if somm1 in self.gdict:
    		self.gdict[somm1].add(somm2)
    	else:
    		self.gdict[somm1] = {somm2}
    	if somm2 in self.gdict:
    		self.gdict[somm2].add(somm1)
    	else:
    		self.gdict[somm2] = {somm1}

# calculer les degrés des noeuds
    def calculate_degrees(self):
    	degrees = defaultdict(int)
    	for somm in self.gdict:
    		for neighbor in self.gdict[somm]:
    			degrees[somm] += 1
    			
    	return degrees

# calculer l'ordre de dégénérescence
    def degeneracy_ordering(self):
        ordering = []
        degrees = g.calculate_degrees()
        sorted_vertices = sorted(degrees, key=lambda x: degrees[x], reverse=False)      
     # Compute the degeneracy ordering
        while len(sorted_vertices) > 0:
     # Remove the first node from the queue
            somm = sorted_vertices.pop(0)
     # Append it to the ordering
            ordering.append(somm)
     # Decrease the degrees of its neighbors
            for u in self.gdict:
                degrees[u] -= 1       
                          
        return ordering

#compute degeneracy
    def degeneracy(self):
        degrees = self.calculate_degrees()
        sorted_vertices = sorted(degrees, key=lambda x: degrees[x], reverse=True)
        k = 0
        for vertex in sorted_vertices:
            if degrees[vertex] > k:
                k += 1
            else:
                break
        return k

#graph GJ
    def find_Gj(self,j):
       gj= Graphe()
       list_voisinage = []
       Vi = []
       vertex_order = -1
       # calcul N[vi]
       list_voisinage.append(self.getSommets()[j])
       for s in self.gdict[self.getSommets()[j]]:
        list_voisinage.append(s)
       #calcul Vi
       ordre = self.degeneracy_ordering()
       for i in range(len(self.degeneracy_ordering())):
        if( ordre[i] == self.getSommets()[j]):
            vertex_order = i
        if(vertex_order != -1):
            Vi.append(ordre[i] )
        
        #N[vi] inter Vi
        for v1 in list_voisinage:
            for v2 in Vi:
                if v1 == v2 :
                    gj.addSommet(v1)
        #ajout des arcs reliants            
        for som in gj.getSommets():
            for som_voisin in self.gdict[som]:
                if (som_voisin in gj.getSommets()) and (som_voisin not in gj.gdict[som]):
                    gj.gdict[som].append(som_voisin)
                    
                  
       return gj
              

#graphe test
graph_elements = { 
   "1" : {"2","3"},
   "2" : {"1","3"},
   "3" : {"1","2","4"},
   "4" : {"3"} 
}
g = Graphe(graph_elements)
liste = g.find_Gj(3)
print(g.degeneracy())
"""
g2 = Graphe()
file = open("facebook_combined.txt")
for arc in file:
    arc = arc.splitlines()
    sommet = arc[0].split(" ")
    g2.addArc({sommet[0],sommet[1]})
"""




#print(g.degeneracy_ordering())
print(liste.gdict)








"""
plt.subplot()
plt.title('Full')
nx.draw(liste,with_labels=True)"""

    
