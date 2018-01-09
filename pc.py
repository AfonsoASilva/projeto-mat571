#entrada
f = open('uni4x8', 'r')
print 'arquivo:'
#while(f.read())
#print list(f)#.readline()
for line in f:
	if line[0] != '#':
		lista = line.split(': ')
		informacoes = lista[0].split(' ')
		informacoes2 = filter(None, informacoes)
		#informacoes = re.compile('/s|/s/s/s').split(lista[0])
		#informacoes = lista[0].split('/s|/s/s/s')
		tarefas = lista[1].split(';')
		tarefas = tarefas[:-1]
		
		for tarefa in tarefas:
			tarefa = tarefa[1:-1]
			tarefa = tarefa.split(',')
			print tarefa


		#print(tarefas)
#print type(line[0])

	#print line


#processamento


#saida