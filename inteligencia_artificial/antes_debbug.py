from PIL import Image #lib tratamento de imagens
import os #manipulação diretorios e arquivos

def pega_rgb(list_dir,filename): #função que retorna rgb total da imagem
    image = Image.open(list_dir+'\\'+filename) #abrindo o diretorio \ arquivo
    image_converter = image.convert("RGB") #convertendo em combinação rbg
    red = [] #vetores para pegar primeiramente os valores separados
    green = []
    blue = []
    vetor_rgb=[] #vetor de rgb total, ordem [todos os reds, todos os greens, todos os blues]

    #obtem o tamanho da imagem em pixels
    largura, altura = image.size

    for i in range (0,altura):
        for j in range (0,largura): #caminhando pela matriz 90x90
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
    
    #confirmação de processamento
    #print('retornado vetor, arquivo: '+filename) 
    return vetor_rgb #retorno



class Entrada():
    def __init__(self, nomeDoArquivo, pixels, treinamentoEObjetoDesejado):
        #sera usado para determinar qual arquivo é o objeto desejado
        self.nomeDoArquivo = nomeDoArquivo
        
        #pixels em uma unica lista
        self.pixels = pixels

        #categoria do treinameto
        self.treinamentoEObjetoDesejado = treinamentoEObjetoDesejado

        #avaliacao da rna se é ou nao objeto desejado
        self.avaliacaoEObjetoDesejado = None



class CamadaOculta:
    def __init__(self, pesosW, pixels, ativacaoNegativa, ativacaoPositiva):
        self.pesosW = pesosW[:]
        self.xiVezesWi = []
        self.somatorioXiVezesWi = 0
        self.resultadoAtivacao = 0


        #calcular xi * wi
        for iteracao in range(len(pixels)):
            self.xiVezesWi.append(self.pesosW[iteracao]*pixels[iteracao])

        #calcular vet i j
        #somatorio de xi * wi
        for iteracao in range(len(pixels)):
            self.somatorioXiVezesWi = self.somatorioXiVezesWi + self.xiVezesWi[iteracao]
        
        #calcular funcao de ativacao
        if self.somatorioXiVezesWi >= 0:
            self.resultadoAtivacao = ativacaoPositiva
        else:
            self.resultadoAtivacao = ativacaoNegativa



class CamadaExposta:
    #todo
    def __init__(self, pesosW, camadasOcultas, valorEsperado, valorEsperadoNegativo, valorEsperadoPositivo):
        self.pesosW = pesosW[:]
        self.xiVezesWi = []
        self.somatorioDeXiVezesWi = 0
        self.saida = 0
        self.erro = 0
        self.valorEsperado=valorEsperado

        #calculando xi * wi
        for iteracao in range(len(camadasOcultas)):
            self.xiVezesWi.append(camadasOcultas[iteracao].resultadoAtivacao * pesosW[iteracao])
    
        #calculando somatorio para funcao de ativacao
        for iteracao in range(len(camadasOcultas)):
            self.somatorioDeXiVezesWi = self.somatorioDeXiVezesWi + self.xiVezesWi[iteracao]

        if self.somatorioDeXiVezesWi >= 0:
            self.saida = valorEsperadoPositivo
        else:
            self.saida = valorEsperadoNegativo

        #if self.saida == valorEsperado:
        if self.saida == self.valorEsperado:
            self.erro = 0
        else:
            #self.erro = valorEsperado - self.saida
            self.erro = self.valorEsperado - self.saida



class Recalculo():
    def __init__(self, ):
        self.deltas = []
        self.deltaMedio = 0
        self.novosPesosCamadaExposta = []
        self.novosPesosCamadaOculta = []

    def calcularDelta(self, erro, taxaDeAprendizagem, resultadoDaAtivacao):
        if erro == 0:
            return 0
        else: 
            return taxaDeAprendizagem*erro*resultadoDaAtivacao


    def calcularDeltaMedio(self):
        somaDosDeltas=0
        
        for iteracao in self.deltas:
            somaDosDeltas=somaDosDeltas+iteracao
        
        self.deltaMedio=somaDosDeltas/len(self.deltas)

        return self.deltaMedio

    def calcularNovoPesoCamadaExposta(self, erro, taxaDeAprendizagem, resultadoDaAtivacao, pesoWCamadaExposta):
        if erro == 0:
            return pesoWCamadaExposta
        else:
            return taxaDeAprendizagem*erro*resultadoDaAtivacao+pesoWCamadaExposta

    def calcularNovoPesoCamadaOculta(self, pesoWCamadaOculta, entrada):
        return pesoWCamadaOculta+self.deltaMedio*entrada

    def gerarDeltas(self, taxaDeAprendizagem, camadasExpostas, camadasOcultas):
        #o que vou precisar pra calcular
        #taxa de aprendizagem
        #o erro das camadas expostas (vou usar 1 camada exposta)
        #resultado de ativacao de cada neuronio de cada camada oculta (vou usar 3 camadas ocultas)

        #vai sair os deltas
       
        for i in range(len(camadasExpostas)):
            for j in range(len(camadasOcultas)):
                #calculo de 1 delta
                #calcularDelta(self, erro, taxaDeAprendizagem, resultadoDaAtivacao):
                self.deltas.append(
                    self.calcularDelta(
                        camadasExpostas[i].erro, 
                        taxaDeAprendizagem, 
                        camadasOcultas[j].resultadoDaAtivacao))

        self.calcularDeltaMedio();

        return self.deltas

    def gerarNovosPesos(self, entrada, camadasOcultas, camadasExpostas, taxaDeAprendizagem):
        
        #calcular novos pesos das camadas exposta
        for i in range(len(camadasExpostas)):
            self.novosPesosCamadaExposta.append([])
            for j in range(len(camadasExpostas[i].pesosW)):
                self.novosPesosCamadaExposta[i].append(
                    self.calcularNovoPesoCamadaExposta(
                        camadasExpostas[i].erro,
                        taxaDeAprendizagem,
                        camadasOcultas[i].resultadoAtivacao,
                        camadasExpostas[i].pesosW[j]
                ))

        #calcular novos pesos das camadas oculta
        for i in range(len(camadasOcultas)):
            self.novosPesosCamadaOculta.append([])
            for j in range(len(entrada.pixels)):
                self.novosPesosCamadaOculta[i].append(
                    self.calcularNovoPesoCamadaOculta(
                        camadasOcultas[i].pesosW[j],
                        entrada.pixels[j]))

        return{"novos_pesos_camada_exposta":self.novosPesosCamadaExposta, "novos_pesos_camada_oculta":self.novosPesosCamadaOculta}
                    


def checarSeTemErros(camadasExpostas):
    temErro = False

    for camadaExposta in camadasExpostas:
        if camadaExposta.erro > 0:
            temErro = True
            #todo
            #print de debug
            print('valor do erro da camada exposta:', camadaExposta.erro)

    return temErro



def main():
    #diretorio = 'c:\\Users\\isaia\\OneDrive\\Documentos\\imagenpython\\imagens' #diretorio das imagens
    
    #diretorio das imagens que sao o objeto desejado
    diretorioPositivo='.\\imagens\\positivas' 
    
    #diretorio das imagens que nao sao o objeto desejado
    diretorioNegativo='.\\imagens\\negativas' 

    #diretorio das imagens que serao avaliadas
    diretorioAvaliacao='.\\imagens\\avaliadas'

    #lista com os objetos da classe Entrada, serao as imagens computadas
    entradas = []

    #lista com os pesos w da camada oculta
    pesosWIniciaisDaCamadaOculta = []

    #sera considerado a imagem de tamanho quadrado e padrao
    larguraDaImagem = 90
    alturaDaImagem = 90

    #um neuronio na camada oculta por pixel para r, g, b.
    neuroniosDaCamadaOculta = larguraDaImagem*alturaDaImagem*3

    for iteracao in range(neuroniosDaCamadaOculta):
        pesosWIniciaisDaCamadaOculta.append((1/neuroniosDaCamadaOculta)*(iteracao+1))

    taxaDeAprendizagem = 0.3

    ativacaoPositiva = 1
    ativacaoNegativa = -1

    valorEsperadoPositivo = 1
    valorEsperadoNegativo = -1

    numeroDeCamadasOcultas = 3
    numeroDeCamadasExpostas = 1

    neuroniosDaCamadaExposta = 3

    #iniciando pesos w em cada uma das camadas exposta
    pesosWIniciaisDaCamadaExposta = []
    
    for iteracao in range(neuroniosDaCamadaExposta):
        pesosWIniciaisDaCamadaExposta.append((1/neuroniosDaCamadaExposta)*(iteracao + 1))

    #iniciando a lista de camadas ocultas
    camadasOcultas=[]

    #iniciando lista de camadas expostas
    camadasExpostas=[]



    for filename in os.listdir(diretorioPositivo): #para arquivo em diretorio...
        #criando entrada a partir do arquivo da iteracao
        entradas.append(Entrada(filename, pega_rgb(diretorioPositivo,filename), valorEsperadoPositivo))

        for iteracao in range(numeroDeCamadasOcultas):
            #construtor da camada oculta
            #pesosW, pixels, ativacaoNegativa, ativacaoPositiva
            camadasOcultas.append(
                CamadaOculta(
                    pesosWIniciaisDaCamadaOculta[:],
                    entradas[-1].pixels,
                    ativacaoNegativa,
                    ativacaoPositiva))

        for iteracao in range(numeroDeCamadasExpostas):
            #pesosW, camadasOcultas, valorEsperado, valorEsperadoNegativo, valorEsperadoPositivo
            camadasExpostas.append(
                CamadaExposta(
                    pesosWIniciaisDaCamadaExposta[:],
                    camadasOcultas,
                    valorEsperadoPositivo,
                    valorEsperadoNegativo,
                    valorEsperadoPositivo))


    for filename in os.listdir(diretorioNegativo): #para arquivo em diretorio...
        #criando entrada a partir do arquivo da iteracao
        entradas.append(Entrada(filename, pega_rgb(diretorioNegativo,filename), valorEsperadoNegativo))


        for iteracao in range(numeroDeCamadasOcultas):
            #construtor da camada oculta
            #pesosW, pixels, ativacaoNegativa, ativacaoPositiva
            camadasOcultas.append(
                CamadaOculta(
                    pesosWIniciaisDaCamadaOculta[:],
                    entradas[-1].pixels,
                    ativacaoNegativa,
                    ativacaoPositiva))

        for iteracao in range(numeroDeCamadasExpostas):
            #pesosW, camadasOcultas, valorEsperado, valorEsperadoNegativo, valorEsperadoPositivo
            camadasExpostas.append(
                CamadaExposta(
                    pesosWIniciaisDaCamadaExposta[:],
                    camadasOcultas,
                    valorEsperadoNegativo,
                    valorEsperadoNegativo,
                    valorEsperadoPositivo))




    while checarSeTemErros(camadasExpostas):
        for entrada in entradas:
            recalculo = Recalculo()
            recalculo.gerarNovosPesos(entrada, camadasOcultas, camadasExpostas, taxaDeAprendizagem)

            for iteracao in range(len(camadasOcultas)):
                # class CamadaOculta:
                #     def __init__(self, pesosW, pixels, ativacaoNegativa, ativacaoPositiva):
                camadasOcultas[iteracao]=CamadaOculta(
                    recalculo.novosPesosCamadaOculta[iteracao],
                    entrada.pixels,
                    ativacaoNegativa,
                    ativacaoPositiva)   

            for iteracao in range(camadasExpostas):
                # class CamadaExposta:
                #     #todo
                #     #def __init__(self, pesosW, camadasOcultas, valorEsperado, valorEsperadoNegativo, valorEsperadoPositivo):
                camadasExpostas[iteracao]=CamadaExposta(
                    recalculo.novosPesosCamadaExposta[iteracao],
                    camadasOcultas,
                    valorEsperadoNegativo,
                    valorEsperadoPositivo)
        

        
main() #inicio
    


