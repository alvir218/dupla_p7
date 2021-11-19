from PIL import Image
import os

def pega_rgb(list_dir,filename):
    image = Image.open(list_dir+'\\'+filename)
    image_converter = image.convert("RGB")
    red = []
    green = []
    blue = []
    vetor_rgb=[]
    for i in range (0,90):
        for j in range (0,90):
            image_valor = image_converter.getpixel((i,j))
            red.append(image_valor[0])
            green.append(image_valor[1])
            blue.append(image_valor[2])
    for cor in red:
        vetor_rgb.append(cor)
    for cor in blue:
        vetor_rgb.append(cor)
    for cor in green:
        vetor_rgb.append(cor)
    print('retornado vetor, arquivo: '+filename)
    return vetor_rgb
    



def main():
    diretorio = 'c:\\Users\\isaia\\OneDrive\\Documentos\\imagenpython\\imagens'
    for filename in os.listdir(diretorio):
        pega_rgb(diretorio,filename)

main()
    


