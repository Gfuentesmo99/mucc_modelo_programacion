import dwavebinarycsp
from dimod.reference.samplers import ExactSolver
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dimod import BinaryQuadraticModel

SEPARATOR = "------------------ "
##############################################################
## horario --> 1: Trabajo 0: fuera de horario
## ubicacion --> 1: Presencial 0: Remoto
## duracion --> 1: Corta 0: Larga
## asistencia --> 1: Obligatoria 1: Opcional
##############################################################

def print_separator(name):
    print("\n\n",SEPARATOR,name,SEPARATOR)
#Función planificar 
def planifica(horario, ubicacion, duracion, asistencia):
    if horario: 
        # En horas de Oficina
        return (ubicacion and asistencia)
    else:
        # Fuera de horario
        return (not ubicacion and not duracion)

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(planifica, ['horario', 'ubicacion', 'duracion', 'asistencia'])
#Solución con ordenador clásico
print_separator("Solucion con ordenador clasico")
bqm = BinaryQuadraticModel({'h':1,'u':1,'d':-1},{'hu':-2,'ha':-1,'hd':1},1,'BINARY')
## Otra forma de obtener el bqm
#bqm = dwavebinarycsp.stitch(csp)
#
##
sampler = ExactSolver()
sampleset = sampler.sample(bqm)
print(sampleset.lowest(atol=.5))

#Solucion con ordenador cuantico
print_separator("Solucion con ordenador cuantico")
sampler = EmbeddingComposite(DWaveSampler())

response = sampler.sample(bqm, num_reads = 5000)
min_energy = next(response.data(['energy']))[0]

print(response)

total = 0
for sample, energy, occurences in response.data(['sample', 'energy', 'num_occurrences']):
    total = total + occurences
    horario = 'Horario de trabajo' if sample['h'] else 'Fuera de horario'
    ubicacion = 'presencial' if sample['u'] else 'remota'
    duracion = 'corta' if sample['d'] else 'larga'
    asistencia = 'obligatoria' if sample['a'] else 'opcional'
    print("{}: {} sesion de tipo {}, de duracion {} con asistencia {}"
                .format(occurences, horario, ubicacion, duracion, asistencia))

