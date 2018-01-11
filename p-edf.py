import sys
#entrada
class Tarefa:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.liberacao = int(arg[0])
        self.execucao = float(arg[1])
        self.execucoes_restantes = self.execucao
        self.periodo = int(arg[2])
        self.deadline = self.periodo
        self.utilizacao = self.execucao / self.periodo
        self.identificacao = str(arg[3])
    def atualizar_deadline(self):
        self.deadline = self.deadline + self.periodo
        self.execucoes_restantes = self.execucao
    def executar_tarefa(self):
        if self.execucoes_restantes > 0:
            self.execucoes_restantes = self.execucoes_restantes - 1
            return True
        else:
            return False
    def return_tarefa(self):
        return self.identificacao+" = Tempo de Execucao: " + str(self.execucao) + ", Periodo: " + str(self.periodo) + ", Utilizacao: " + str(self.utilizacao) + ";"

class Processador:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.identificacao = arg
        self.tarefas = []
        self.utilizacao = 0.0
    def adicionar_tarefa(self, tarefa):
        self.utilizacao = self.utilizacao + tarefa.utilizacao
        self.tarefas.append(tarefa)
    def print_processador(self):
        print "Identificacao: " + str(self.identificacao) + ", Utilizacao: " + str(self.utilizacao) + ", Tarefas: "
        for tarefa in self.tarefas:
            print "......." + tarefa.return_tarefa()
    def limpar_processador(self):
        self.utilizacao = 0
        self.tarefas = []

def limpar_processadores(lista_processadores):
    for processador in lista_processadores:
        if (processador != ''):
            processador.limpar_processador()

def retorna_lista_tarefas(linha):
    tarefas_str = linha.split(';')
    tarefas_str = tarefas_str[:-1]
    count = 0
    lista_tarefas = []
    for tarefa_str in tarefas_str:
        tarefa_str = tarefa_str[1:-1]
        tarefa_lst = tarefa_str.split(',')
        tarefa_lst.append('t'+str(count))
        tarefa = Tarefa(tarefa_lst)
        lista_tarefas.append(tarefa)
        count = count + 1
    return lista_tarefas

def retorna_lista_processadores(qtd):
    lista_processadores = ['']
    for index in range(qtd):
        processador = Processador(index + 1)
        lista_processadores.append(processador)
    return lista_processadores

def retorna_meta_dados(linha):
    metadata = linha.split(' ')
    metadata = filter(None, metadata)
    mapa = {}
    mapa['linha'] = metadata[0]
    mapa['qtd_processadores'] = metadata[1]
    mapa['qtd_tarefas'] = metadata[2]
    mapa['tempo_simulacao'] = metadata[3]
    return mapa

def verifica_escalonabilidade_edf(lista_tarefas):
    soma = 0
    for tarefa in lista_tarefas:
        soma = soma + tarefa.utilizacao
    if soma > 1:
        return False
    else:
        return True

def ordenar_tarefas_deadline(lista_tarefas):
    lista_tarefas.sort(key=lambda x: x.deadline)
    return lista_tarefas

def execucao_edf(lista_tarefas, tempo):
    lista_tarefas = ordenar_tarefas_deadline(lista_tarefas)
    for index in range(tempo):
        flagAD = True
        while flagAD:
            if lista_tarefas[0].deadline == index:
                lista_tarefas[0].atualizar_deadline()
                lista_tarefas = ordenar_tarefas_deadline(lista_tarefas)
            else:
                flagAD = False
        flagET = True
        i = 0
        while flagET:
            if lista_tarefas[i].executar_tarefa():
                print "Tempo: " + str(index + 1) + " - Tarefa: " + lista_tarefas[i].identificacao
                flagET = False
            else:
                i = i + 1
                if i >= len(lista_tarefas):
                    flagET = False

def calcular_sep(k, num_processadores):
    if (k < int(num_processadores)):
        return float(k) / (float(k) + 1)
    else:
        return 1

def verifica_escalonabilidade_pedf(lista_processadores, lista_tarefas):    
    for tarefa in lista_tarefas:
        flagEP = True    
        index = 0        
        while flagEP: 
            #lista_processadores[index].print_processador()
            if (lista_processadores[index].utilizacao + tarefa.utilizacao <= 1):
                lista_processadores[index].adicionar_tarefa(tarefa)
                flagEP = False                
            else:
                index = index + 1                
                if(index >= len(lista_processadores)):                	
                    return False
    return True	

def log_execucao(lista_processadores, lista_tarefas):
    for processador in lista_processadores:
        processador.print_processador()


f = open('uni4x8', 'r')
count = 0
for line in f:	
    if line[0] != '#':
        entrada = line.split(': ')
        meta_dados = retorna_meta_dados(entrada[0])
        lista_tarefas = retorna_lista_tarefas(entrada[1])
        lista_processadores = retorna_lista_processadores(int(meta_dados['qtd_processadores']))
        del lista_processadores[0]   
        print line             
        flag = True    
        while flag:
            if verifica_escalonabilidade_pedf(lista_processadores, lista_tarefas):
                flag = False                
            else:                
            	print line
                limpar_processadores(lista_processadores)                
                meta_dados['qtd_tarefas'] = int(meta_dados['qtd_tarefas']) - 1                
                del lista_tarefas[-1]
        for processador in lista_processadores:
        	processador.print_processador()
        	execucao_edf(processador.tarefas, 20)
        break

        
