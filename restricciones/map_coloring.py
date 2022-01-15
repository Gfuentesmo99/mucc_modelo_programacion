import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from dimod import BinaryQuadraticModel
from dwave.system.samplers import LeapHybridBQMSampler
import dwave.inspector


########### CONSTANTES ###########
#Ponemos las posiciones del nodo para representar el mapa de espana de una manera mas organizada
node_positions = {"can": (0, 0),
                  "ceu": (2, 0),
                  "mel": (4, 0),
                  "and": (3, 1),
                  "ext": (0, 2),
                  "clm": (3, 2),
                  "mur": (6, 2),
                  "cyl": (1, 3),
                  "mad": (3, 3),
                  "rio": (3, 4),
                  "ar": (5, 5),
                  "vlc": (6, 3),
                  "cat": (6, 6),
                  "bal": (7, 3),
                  "nav": (4, 6),
                  "pv": (3, 6),
                  "ca": (2, 6),
                  "ast": (1, 6),
                  "gal": (0,6)}


#Lista de CCAA
ccaa = ['can','and','ext','clm','cyl','mur','vlc','mad','ar',
'cat','rio','pv','nav','ca','ast','gal',
'bal','ceu','mel']
#Lista de vecinos
neighbours = [('and','ext'),('and','clm'),('and','mur'),
('ext','cyl'),('clm','ext'),('clm','mad'),('clm','mur'),('clm','vlc'),
('clm','ar'),('clm','cyl'),('vlc','mur'),('cyl','mad'),('cyl','ar'),
('cyl','rio'),('cyl','pv'),('cyl','ca'),('cyl','ast'),('cyl','gal'),
('cat','ar'),('nav','ar'),('rio','ar'), ('rio','nav'),
('rio','pv'),('pv','nav'),('pv','ca'),('ca','ast'),
('ast','gal'),('ar','vlc'),('cat','vlc')
]

########### Funciones ###########
#Funcion para que ccaa vecinas no tengan igual color
def different_colours(ca1, ca2):
    return not (ca1 and ca2)

#Funcion para crear el grafo del mapa coloreado
def plot_map(sample):
    # Creamos el grafo con todos los que son vecinos
    G = nx.Graph(neighbours)
    #Obtenemos las comunidades sin vecinos
    lone_nodes = set(ccaa) - set(G.nodes) 
    #Con este bucle las add al grafo
    for lone_node in lone_nodes:
        G.add_node(lone_node)
    #Recorremos la respuesta para coger el color escogido 
    color_labels = [k for k, v in sample.items() if v == 1]
    # Get color order to match that of the graph nodes
    #Para cada ccaa
    for label in color_labels:
        #Obtenemos su nombre y color escogido
        name, color = label.split("_")
        #Convertimos el string de color en un entero
        color = int(color)
        #Add color al nodo
        G.nodes[name]["color"] = color
    #Obtenemos todos los colores
    color_map = [color for name, color in G.nodes(data="color")]

    #Y dibujamos el grafo con los nombres, las posicones asignadas y los colores
    nx.draw_networkx(G, with_labels=True, pos = node_positions,
                     node_color=color_map, font_color="w", node_size=500)

    # Guardamos
    filename = "restricciones/espana_ccaa.png"
    plt.savefig(filename)

########### Main ###########
#Segun el teorema de los 4 colores podremos pintar cualquier mapa planar con 4 colores
one_color_configurations = {(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)}
#Obtenemos la longitud de los posibles colores
colours = len(one_color_configurations)
# Creamos un CSP
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
#A cada comunidad autonoma le add los 4 posibles que pueda tener (0,1,2,3) luego se pasaran a colroes
for ca in ccaa:
    variables = [ca+"_"+str(i) for i in range(colours)]
    #Y add a las restricciones de que solamente puede tener un color
    csp.add_constraint(one_color_configurations, variables)
#Para cada pareja de vecinos les asignamos una posible combinacion de colores y add la restriccion
for neighbour in neighbours:
    ca1, ca2 = neighbour
    for i in range(colours):
        variables = [ca1+"_"+str(i), ca2+"_"+str(i)]
        csp.add_constraint(different_colours, variables)

#Creamos el BQM a traves del CSP
bqm = dwavebinarycsp.stitch(csp)


#Cogemos un sampler en este caso probaremos con Pegasus
sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'pegasus'}))  
#Realizamos 100 lecturas
response = sampler.sample(bqm, num_reads=100)    
sample = response.first.sample
#Comprobamos si la de menor energia cumple con nuestras restricciones y si las cumple pintamos
if not csp.check(sample):          
    print("Failed to color map")
else:
    print("Problema resuelto, guardando el mapa..")
    print(response)
    dwave.inspector.show(response)
    plot_map(sample)






