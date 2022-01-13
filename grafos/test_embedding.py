from dwave.system.samplers import DWaveSampler

#Resolvemos el problema a mano:
###################
#Pesos nodo: a=b=c=-1
#Pesos vertices: ab=ac=bc=2
#Al usar una arquitectura Quimera -> Agrupamos en 4 qubits (Nodo C representado en 2 qubits)
#Pesos qubits q0=q5=0.5 q1=-1 q4=-1
#Pesos couplers q04=q14=q15=2, q05=-3 para acoplamiento fuerte
#Add 1.5 al peso bias q0 y q5 para compensar: q0=q5=1
#Normalizamos
###################

bias = {(0,0): 0.333, (1,1): -0.333,(4,4): -0.333, (5,5): 0.333} 
couplers = {(0,4): 0.667, (0,5): -1, (4,1): 0.667, (1,5): 0.667}
qubo = dict(bias)
qubo.update(couplers)
#Resolvermos con chimera
response = DWaveSampler(solver='DW_2000Q_6').sample_qubo(qubo, num_reads=1000)
print(response)
