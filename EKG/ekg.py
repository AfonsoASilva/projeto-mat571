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
        return "Tempo de Execucao: " + str(self.execucao) + ", Periodo: " + str(self.periodo) + ", Utilizacao: " + str(self.utilizacao) + ";"

class Processador:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.identificacao = arg
        self.tarefas = []
        self.utilizacao = 0
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
    lista_tarefas = []
    for tarefa_str in tarefas_str:
        tarefa_str = tarefa_str[1:-1]
        tarefa_lst = tarefa_str.split(',')
        tarefa = Tarefa(tarefa_lst)
        lista_tarefas.append(tarefa)
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

def ordenar_tarefas_deadline(lista_tarefas, meta_dados):
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
                print "Tempo: " + str(index + 1) + " - Tarefa: t" + i
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

def verifica_escalonabilidade_ekg(lista_tarefas, lista_processadores, meta_dados):
    tarefas_pesadas = []
    tarefas_leves = []
    K = 4
    SEP = calcular_sep(K, meta_dados['qtd_processadores'])
    for tarefa in lista_tarefas:
        if float(tarefa.utilizacao) > float(SEP):
            tarefas_pesadas.append(tarefa)
        else:
            tarefas_leves.append(tarefa)
    L = len(tarefas_pesadas)
    lista_tarefas_separadas = tarefas_pesadas + tarefas_leves
    lista_tarefas_separadas.insert(0, '')
    if len(tarefas_pesadas) <= int(meta_dados['qtd_processadores']):
        for index in range(1,L+1):
            lista_processadores[index].adicionar_tarefa(lista_tarefas_separadas[index])
        if len(tarefas_leves) > 0:
            if L + 1 <= int(meta_dados['qtd_processadores']):
                p = L + 1
                for i in range(L + 1, int(meta_dados['qtd_tarefas']) + 1):
                    print i
                    print lista_processadores[p].utilizacao + lista_tarefas_separadas[i].utilizacao
                    if (lista_processadores[p].utilizacao + lista_tarefas_separadas[i].utilizacao) <= 1:
                        lista_processadores[p].adicionar_tarefa(lista_tarefas_separadas[i])
                    else:
                        if (p + 1) <= int(meta_dados['qtd_processadores']):
                            if ((p-L) % K) == 0:
                                p = p + 1
                                lista_processadores[p].adicionar_tarefa(lista_tarefas_separadas[i])
                            else:
                                periodo = lista_tarefas_separadas[i].periodo
                                execucao_1 = (1 - lista_processadores[p].utilizacao) * periodo
                                execucao_2 = lista_tarefas_separadas[i].execucao - execucao_1
                                tarefa_1 = Tarefa([0,execucao_1,periodo])
                                tarefa_2 = Tarefa([0,execucao_2,periodo])
                                lista_processadores[p].adicionar_tarefa(tarefa_1)
                                lista_processadores[p+1].adicionar_tarefa(tarefa_2)
                                p = p + 1
                        else:
                            return False
                return True
            else:
                return False
        else:
            return True
    else:
        return False

f = open('../uni4x8', 'r')
flag = False
for line in f:
    if line[0] != '#':
        entrada = line.split(': ')
        meta_dados = retorna_meta_dados(entrada[0])
        lista_tarefas = retorna_lista_tarefas(entrada[1])
        lista_processadores = retorna_lista_processadores(int(meta_dados['qtd_processadores']))
        flag = True

        while flag:
            if verifica_escalonabilidade_ekg(lista_tarefas, lista_processadores, meta_dados):
                flag = False
            else:
                limpar_processadores(lista_processadores)
                meta_dados['qtd_tarefas'] = int(meta_dados['qtd_tarefas']) - 1
                del lista_tarefas[-1]

        break

#processamento


#saida
