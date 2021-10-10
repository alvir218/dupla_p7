


# variaveis usadas no projeto
nrz1 = ['0','0','1','1','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','1','1','0','0','0','0','0','0','0','0','1','0','0']



# funcao para aplicar pattern par
def odd(last_one):
    if last_one == '+':
        return ['0','0','0',"V+"]
    else:
        return ['0','0','0',"V-"]



#processador do codigo nrz
def processar(nrz):
    
    #variaveis da funcao
    hdb3 = ()
    buffer = []
    last_one = '-'
    ones = 0
    
    # percorrer a entrada nrz
    for bit in nrz:
        buffer.append(bit)

        #comparacao do ultimo bit 1
        #se o ultimo for positivo, fica negativo, se for negativo fica positivo
        #classificando 1 como negativo ou positivo
        if buffer[-1] == '1' and last_one == '+':
            buffer[-1] = '-1'
            last_one = '-'
            ones = ones + 1
        elif buffer[-1] == '1' and last_one == '-':
            buffer[-1] = '+1'
            last_one = '+'
            ones = ones + 1
        
        #se o ultimo bit processado for 1, zera o buffer
        if buffer[-1] == '-1' or buffer[-1] == '+1':
            hdb3 = hdb3 + tuple(buffer)
            buffer.clear()

        #se houver violacao impar ela sera processada        
        if buffer == ['0','0','0','0'] and ones % 2 > 0:
            hdb3 = hdb3 + tuple(odd(last_one))
            buffer.clear()
            ones = 0

    return hdb3



#preencher com a entrada desejada
saida1 = processar(['1','1','0','0','0','0','1'])
                #('+1', '-1', '0', '0', '0', '0', '+1')
print("saida1:")
print(saida1)

saida2 = processar(['1','1','1','0','0','0','0','1'])
                #('+1', '-1', '+1', '0', '0', '0', 'V+', '-1')
print("saida2:")
print(saida2)

