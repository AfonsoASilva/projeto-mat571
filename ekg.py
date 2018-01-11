import sys
from math import floor
#entrada
class Tarefa:
    """docstring for Tarefa."""
    def __init__(self, arg, titulo):
        self.titulo = titulo
        self.liberacao = int(arg[0])
        self.execucao = float(arg[1])
        self.execucoes_restantes = self.execucao
        self.periodo = int(arg[2])
        self.deadline = self.periodo
        self.utilizacao = self.execucao / self.periodo
        self.parte = 0
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
        return "Tarefa " + self.titulo + ": Tempo de Execucao: " + str(self.execucao) + "; Periodo: " + str(self.periodo) + "; Utilizacao: " + str(self.utilizacao) + ";"

class Processador:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.identificacao = arg
        self.tarefas = []
        self.utilizacao = 0
        self.execucao = []
    def adicionar_tarefa(self, tarefa):
        self.utilizacao = self.utilizacao + tarefa.utilizacao
        self.tarefas.append(tarefa)
    def print_processador(self):
        print "...Processador " + str(self.identificacao) + ": Utilizacao: " + str(self.utilizacao) + "; Tarefas: "
        for tarefa in self.tarefas:
            print "......." + tarefa.return_tarefa()
    def limpar_processador(self):
        self.utilizacao = 0
        self.tarefas = []
    def atualizar_historico_execucao(self, executado):
        self.execucao.append()
    def atualizar_deadlines(self, deadline):
        for index, tarefa in enumerate(self.tarefas):
            if self.tarefas[index].deadline == deadline:
                self.tarefas[index].atualizar_deadline()

def limpar_processadores(lista_processadores):
    for processador in lista_processadores:
        if (processador != ''):
            processador.limpar_processador()

def print_processadores(lista_processadores):
    for processador in lista_processadores:
        if not type(processador) is str:
            processador.print_processador()

def retorna_lista_tarefas(linha):
    tarefas_str = linha.split(';')
    tarefas_str = tarefas_str[:-1]
    lista_tarefas = []
    for tarefa_str in tarefas_str:
        tarefa_str = tarefa_str[1:-1]
        tarefa_lst = tarefa_str.split(',')
        tarefa_id = "t" + str(len(lista_tarefas))
        tarefa = Tarefa(tarefa_lst, tarefa_id)
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

def retorna_menor_deadline(lista_tarefas):
    menor_deadline = lista_tarefas[0].deadline
    for tarefa in lista_tarefas:
        if tarefa.deadline < menor_deadline:
            menor_deadline = tarefa.deadline
            menor_tarefa = tarefa

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

def execucao_tarefas_pesadas(lista_processadores, tempo, indice_mudanca):
    for processador in lista_processadores:
        for tempo in range(1, (tempo + 1)):
            if processador.tarefas[0].executar_tarefa():
                processador.execucao.append(processador.tarefas[0].titulo)
            else:
                processador.execucao.append('-')
            processador.atualizar_deadlines(retorna_menor_deadline(processador.tarefas))


def calcular_sep(k, num_processadores):
    if (k < int(num_processadores)):
        return float(k) / (float(k) + 1)
    else:
        return 1

def verifica_escalonabilidade_ekg(lista_tarefas, lista_processadores, meta_dados, variavel_K):
    tarefas_pesadas = []
    tarefas_leves = []
    K = variavel_K
    SEP = calcular_sep(K, meta_dados['qtd_processadores'])
    for tarefa in lista_tarefas:
        if float(tarefa.utilizacao) > float(SEP):
            tarefas_pesadas.append(tarefa)
        else:
            tarefas_leves.append(tarefa)
    L = len(tarefas_pesadas)
    meta_dados['indice_mudanca'] = L
    lista_tarefas = tarefas_pesadas + tarefas_leves
    lista_tarefas.insert(0, '')
    if len(tarefas_pesadas) <= int(meta_dados['qtd_processadores']):
        for index in range(1,L+1):
            lista_processadores[index].adicionar_tarefa(lista_tarefas[index])
        if len(tarefas_leves) > 0:
            if L + 1 <= int(meta_dados['qtd_processadores']):
                p = L + 1
                for i in range(L + 1, int(meta_dados['qtd_tarefas']) + 1):
                    if (lista_processadores[p].utilizacao + lista_tarefas[i].utilizacao) <= 1:
                        lista_processadores[p].adicionar_tarefa(lista_tarefas[i])
                    else:
                        if (p + 1) <= int(meta_dados['qtd_processadores']):
                            if ((p-L) % K) == 0:
                                p = p + 1
                                lista_processadores[p].adicionar_tarefa(lista_tarefas[i])
                            else:
                                periodo = lista_tarefas[i].periodo
                                titulo = lista_tarefas[i].titulo
                                execucao_1 = (1 - lista_processadores[p].utilizacao) * periodo
                                execucao_2 = lista_tarefas[i].execucao - execucao_1
                                tarefa_1 = Tarefa([0,execucao_1,periodo], titulo + '-1')
                                tarefa_1.parte = 1
                                tarefa_2 = Tarefa([0,execucao_2,periodo], titulo + '-2')
                                tarefa_2.parte = 2
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

def main():
    arquivo = raw_input("Nome do arquivo a ser lido: ")
    variavel_K = int(raw_input("Determine o K do EKG: "))
    f = open(arquivo, 'r')
    flag = False
    for line in f:
        if line[0] != '#':
            entrada = line.split(': ')
            meta_dados = retorna_meta_dados(entrada[0])
            lista_tarefas = retorna_lista_tarefas(entrada[1])
            lista_processadores = retorna_lista_processadores(int(meta_dados['qtd_processadores']))
            flag = True

            while flag:
                if verifica_escalonabilidade_ekg(lista_tarefas, lista_processadores, meta_dados, variavel_K):
                    flag = False
                    string = "Linha " + meta_dados['linha'] + ": Escalonavel por EKG com: "
                    for tarefa in lista_tarefas:
                        string += tarefa.titulo + ", "
                    string = string[:-2]
                    print string
                else:
                    limpar_processadores(lista_processadores)
                    meta_dados['qtd_tarefas'] = int(meta_dados['qtd_tarefas']) - 1
                    if meta_dados['qtd_tarefas'] == 0:
                        print "Nenhuma tarefa e escalonavel por EKG"
                        return 0
                    else:
                        del lista_tarefas[-1]
            del lista_processadores[0]
            print "...Escalonamento: "
            print_processadores(lista_processadores)

if __name__ == "__main__":
    main()

#processamento


#saida
