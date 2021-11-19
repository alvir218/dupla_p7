from PIL import Image #lib tratamento de imagens
import os #manipulação diretorios e arquivos

def pega_rgb(list_dir,filename): #função que retorna rgb total da imagem
    image = Image.open(list_dir+'\\'+filename) #abrindo o diretorio \ arquivo
    image_converter = image.convert("RGB") #convertendo em combinação rbg
    red = [] #vetores para pegar primeiramente os valores separados
    green = []
    blue = []
    vetor_rgb=[] #vetor de rgb total, ordem [todos os reds, todos os greens, todos os blues]
    for i in range (0,90):
        for j in range (0,90): #caminhando pela matriz 90x90
            image_valor = image_converter.getpixel((i,j)) #pegando o pixel referente
            red.append(image_valor[0]) #posição 0 = R, 1 = G, 2 = B
            green.append(image_valor[1])
            blue.append(image_valor[2])
    for cor in red: #colocando na ordem já descrita
        vetor_rgb.append(cor)
    for cor in blue:
        vetor_rgb.append(cor)
    for cor in green:
        vetor_rgb.append(cor)
    print('retornado vetor, arquivo: '+filename) #confirmação de processamento
    return vetor_rgb #retorno
    



def main():
    diretorio = 'c:\\Users\\isaia\\OneDrive\\Documentos\\imagenpython\\imagens' #diretorio das imagens
    for filename in os.listdir(diretorio): #para arquivo em diretorio...
        pega_rgb(diretorio,filename) #chama função

main() #inicio
    


