import dwavebinarycsp
from dimod.reference.samplers import ExactSolver
from dwave.system.samplers import DWaveSampler
from dwave.system.samplers import DWaveCliqueSampler
from dwave.system.composites import EmbeddingComposite
from dimod import BinaryQuadraticModel
from dwave.system.samplers import LeapHybridSampler

##############-- CONSTANTES --##############
SEPARATOR = "------------------ "
SHOW_ALL = True
##############################################################
## horario (h)--> 1: Trabajo 0: fuera de horario
## ubicacion (u) --> 1: Presencial 0: Remoto
## duracion (d)--> 1: Corta 0: Larga
## asistencia(a) --> 1: Obligatoria 1: Opcional
##############################################################

##############-- FUNCIONES --##############

#Funcion para mostrar separador
def print_separator(name):
    print("\n\n",SEPARATOR,name,SEPARATOR)

#Función planificar 
def planifica(h, u, d, a):
    if h: 
        # En horas de Oficina
        return (u and a)
    else:
        # Fuera de horario
        return (not u and not d)

#Funcion para mostrar los resultados
def print_results(response, show_all):
    min_energy = next(response.data(['energy']))[0]
    #print(response)
    total = 0
    for sample, energy, occurences in response.data(['sample', 'energy', 'num_occurrences']):
        total = total + occurences
        if (energy == min_energy or show_all):
            horario = 'Horario de trabajo' if sample['h'] else 'Fuera de horario'
            ubicacion = 'presencial' if sample['u'] else 'remota'
            duracion = 'corta' if sample['d'] else 'larga'
            asistencia = 'obligatoria' if sample['a'] else 'opcional'
            print("{}: {} sesion de tipo {}, de duracion {} con asistencia {}"
                        .format(occurences, horario, ubicacion, duracion, asistencia))  

def execute_quantum(sampler, reads):
    response = sampler.sample(bqm, num_reads = reads)
    print_results(response, SHOW_ALL)

##############-- MAIN --##############
#Obtenemos los constraints
bqm = BinaryQuadraticModel({'h':1,'u':1,'d':-1},{'hu':-2,'ha':-1,'hd':1},1,'BINARY')
## Otra forma de obtener el bqm
#csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
#csp.add_constraint(planifica, ['horario', 'ubicacion', 'duracion', 'asistencia'])
#bqm = dwavebinarycsp.stitch(csp)
#

#Solución con ordenador clásico
print_separator("Solucion con ordenador clasico")
sampler = ExactSolver()
sampleset = sampler.sample(bqm)
print(sampleset.lowest(atol=.5))

#Solucion con ordenador cuantico - DWave Sampler
print_separator("Solucion con ordenador cuantico DWave Sampler")
sampler = EmbeddingComposite(DWaveSampler())
execute_quantum(sampler,5000)

#Solucion con ordenador cuantico - DwaveCliqueSampler -NO FUNCIONA
#print_separator("Solucion con ordenador cuantico DWave Clique Sampler")
#sampler = DWaveCliqueSampler() 
#execute_quantum(sampler,100)

##Solucion con ordenador cuantico - DW 2000Q
print_separator("Solucion con ordenador cuantico DW 2000Q")
sampler = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6'))
execute_quantum(sampler,5000)

##Solucion con ordenador cuantico - Dw Pegasus
print_separator("Solucion con ordenador cuantico Dwave Pegasus")
sampler = EmbeddingComposite(DWaveSampler(solver=dict(topology__type='pegasus')))
execute_quantum(sampler,5000)

##Solucion con ordenador cuantico - Dw Hybrid
print_separator("Solucion con ordenador cuantico Dwave Hybrid")
sampler = LeapHybridSampler()
#execute_quantum(sampler,5000)
response = sampler.sample(bqm)
print(response)


