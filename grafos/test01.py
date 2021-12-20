import networkx as nx
import matplotlib.pyplot as mpl
import dwave_networkx as dnx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

s5 = nx.star_graph(5)
sampler = EmbeddingComposite(DWaveSampler())

print(dnx.min_vertex_cover(s5,sampler))
nx.draw(s5, with_labels = True)
mpl.savefig("graficoestrella.png")
