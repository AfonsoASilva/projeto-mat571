import sys
#entrada
class Tarefa:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.identificacao = arg[3]
        self.liberacao = int(arg[0])
        self.execucao = float(arg[1])
        self.execucoes_restantes = self.execucao
        self.periodo = int(arg[2])
        self.deadline = self.periodo
        self.utilizacao = self.execucao / self.periodo
    def atualizar_deadline(self):
        self.deadline = self.deadline + self.periodo
        self.execucoes_restantes = self.execucao
    def executar_tarefa(self):
        if self.execucoes_restantes > 0:
            self.execucoes_restantes = self.execucoes_restantes - 1
            return True
        else:
            return False

def retorna_lista_tarefas(linha):
    tarefas_str = linha.split(';')
    tarefas_str = tarefas_str[:-1]
    lista_tarefas = []
    for tarefa_str in tarefas_str:
        tarefa_str = tarefa_str[1:-1]
        tarefa_lst = tarefa_str.split(',')
        tamanho_lista = "t" + str(len(lista_tarefas))
        tarefa_lst.append(tamanho_lista)
        tarefa = Tarefa(tarefa_lst)
        lista_tarefas.append(tarefa)
    return lista_tarefas

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


f = open('uni4x8', 'r')
for line in f:
    if line[0] != '#':
        entrada = line.split(': ')
        meta_dados = retorna_meta_dados(entrada[0])
        lista_tarefas = retorna_lista_tarefas(entrada[1])
        #tarefa1 = Tarefa(["0", "2", "4", "t1"])
        #tarefa2 = Tarefa(["0", "1", "5", "t2"])
        #tarefa3 = Tarefa(["0", "2", "10", "t3"])
        #lista_escalonavel = []
        #lista_escalonavel.append(tarefa1)
        #lista_escalonavel.append(tarefa2)
        #lista_escalonavel.append(tarefa3)
        #if verifica_escalonabilidade_edf(lista_escalonavel):
        #    lista_escalonavel = ordenar_tarefas_deadline(lista_escalonavel)
        #    execucao_edf(lista_escalonavel, 30)
        #break
