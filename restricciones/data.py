import json
import pyplot as plt
from scipy import stats

########### CONSTANTES ###########
#Ruta al archivo de los datos
FILE="restricciones/data_ccaa.json"
########### VARIABLES ###########
total_quimera=0
total_pegasus=0
total_quimera_time=0
total_pegasus_time=0
qubits_sol_quimera=[]
qubits_sol_pegasus=[]
total_quimera_sols=0
total_pegasus_sols=0

########### Main ###########
with open(FILE) as f:
    data_ccaa = json.load(f)

for architecture, time, qubits, num_sol in data_ccaa(['architecture','qpu_time','qubits','num_sol']):
    if(architecture=='QUIMERA'):
        total_quimera +=1
        total_quimera_time+=time
        total_quimera_sols+=num_sol
        qubits_sol_quimera.append((qubits,num_sol))
    else:
        total_pegasus +=1
        total_pegasus_time+=time
        total_pegasus_sols+=num_sol
        qubits_sol_pegasus.append((qubits,num_sol))

print(qubits_sol_pegasus)

        