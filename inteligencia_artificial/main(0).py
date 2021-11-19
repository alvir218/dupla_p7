from PIL import Image

image = Image.open('imagem.png' )
image_converter = image.convert("RGB")
count = 0
red = []
green = []
blue = []
vetor_rgb=[]
for i in range (0,90):
    for j in range (0,90):
        image_valor = image_converter.getpixel((i,j))
        count+=1
        red.append(image_valor[0])
        green.append(image_valor[1])
        blue.append(image_valor[2])
for cor in red:
    vetor_rgb.append(cor)
for cor in blue:
    vetor_rgb.append(cor)
for cor in green:
    vetor_rgb.append(cor)

