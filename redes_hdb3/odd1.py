


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
    hdb3 = []
    buffer = []
    last_one = '-'
    
    # percorrer a entrada nrz
    for bit in nrz:
        buffer.append(bit)

        #se o ultimo for positivo, fica negativo, se for negativo fica positivo
        #comparacao do ultimo bit 1
        if bit == '1' and last_one == '+':
            last_one = '-'
        else:
            last_one = '+'
        
        #se o ultimo bit processado for 1, zera o buffer
        if buffer[-1] == '1':
            hdb3.append(list(buffer))
            buffer.clear()

        #se houver violacao        
        if buffer == ['0','0','0','0']:
            hdb3.append(odd(last_one))
            buffer.clear()

    return hdb3



#preencher com a entrada desejada
saida = processar(['1','1','0','0','0','0','1'])
print(saida)