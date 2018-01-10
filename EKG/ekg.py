#entrada
class Tarefa:
    """docstring for Tarefa."""
    def __init__(self, arg):
        self.liberacao = int(arg[0])
        self.execucao = float(arg[1])
        self.periodo = int(arg[2])
        self.utilizacao = self.execucao / self.periodo

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

def retorna_meta_dados(linha):
    metadata = linha.split(' ')
    metadata = filter(None, metadata)
    mapa = {}
    mapa['linha'] = metadata[0]
    mapa['qtd_processadores'] = metadata[1]
    mapa['qtd_tarefas'] = metadata[2]
    mapa['tempo_simulacao'] = metadata[3]
    return mapa

f = open('../uni4x8', 'r')
for line in f:
    if line[0] != '#':
        entrada = line.split(': ')
        meta_dados = retorna_meta_dados(entrada[0])
        lista_tarefas = retorna_lista_tarefas(entrada[1])
        
        break



#processamento


#saida
