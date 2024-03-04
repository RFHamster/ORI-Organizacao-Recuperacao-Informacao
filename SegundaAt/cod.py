import math

## Variáveis Globais
QNT_DOCS = 7

## Função para ler o arquivo de resposta .txt
def ler_arquivo_txt(caminho_arquivo):
  try:
    with open(caminho_arquivo, "r") as arquivo:
      linhas = arquivo.readlines()
  except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
    return None

  # Removendo as quebras de linha das linhas e transformando em um vetor
  linhas = [linha.strip() for linha in linhas]
  return linhas

##----------------------------------------------------------------------------##

def calcularIDWTF(IDF,WTF):
  IDWTF = {}
  for valor, qnt in IDF.items():
    IDWTF[valor] = [0] * QNT_DOCS
    for i in range(QNT_DOCS):
      IDWTF[valor][i] = WTF[valor][i] * qnt

  return IDWTF

##----------------------------------------------------------------------------##

def calcularWTF(valor):
  if valor == 0:
    return 0

  return (1 + math.log(valor,10))

##----------------------------------------------------------------------------##

def fazer_termo_inv(termos):
  termoInv = {}
  IDF = {}
  WTF = {}
  # Colocando cada termo na matriz termo invertido
  for termo in termos:
    aux = termo.split(" ")
    # Retirar "->"
    aux.pop(1)
    # Pegando o token e em quais documentos ele aparece
    token, qntDocAparecido = aux[0].split("/")[:2]
    qntDocAparecido = int(qntDocAparecido)
    # Iniciando WTF e todas aparições nos docs como 0
    termoInv[token] = [0] * QNT_DOCS
    WTF[token] = [0] * QNT_DOCS
    # Calculando IDF
    IDF[token] = math.log(QNT_DOCS/qntDocAparecido,10)

    # Colocando o valor de aparições em cada documento
    for i in range(int(qntDocAparecido)):
      documento, qnt = aux[1+i].split("/")[:2]
      qnt = qnt.replace(",", "")
      documento = int(documento) - 1
      qnt = int(qnt)
      termoInv[token][documento] = qnt

      # Calculando WTF
      WTF[token][documento] = calcularWTF(qnt)

  return termoInv, IDF, WTF

##----------------------------------------------------------------------------##

def calcularVetorial(termos, IDF, IDWTF):
  resultado = ""
  vetores = {}
  modulos = [0] * (QNT_DOCS+1)

  ## Calculando o valor dos Vetores
  for termo in termos:
    if termo not in IDF:
      return "TERMO NÃO ENCONTRADO"
    ## vetores[termo][0] -> valor do termo no vetor consulta // vetores[termo][1 à 7] -> valor do termo no vetor documento
    vetores[termo] = [0.0] * (QNT_DOCS+1)
    vetores[termo][0] = IDF[termo]
    ## Incrementando os valores ao quadrado do vetor consulta
    modulos[0] += (IDF[termo] * IDF[termo])
    for i in range(QNT_DOCS):
      vetores[termo][i+1] = IDWTF[termo][i]
      modulos[i+1] += (IDWTF[termo][i] * IDWTF[termo][i])

  ## Finalizando o calculo do vetor consulta
  for i in range(len(modulos)):
    modulos[i] = math.sqrt(modulos[i])

  # print("Modulos")
  # print(modulos)

  # print("Vetor n Normalizado")
  # print(vetores)

  ## Normalizar Vetores
  for termo in termos:
    for i in range(QNT_DOCS+1):
      if modulos[i] == 0:
        vetores[termo][i] = 0
        continue
      vetores[termo][i] = vetores[termo][i]/modulos[i]

  # print("Vetor Normalizado")
  # print(vetores)

  ## Calcular Cossenos
  cossenos = {}

  for i in range(QNT_DOCS):
    cossenos[i] = 0

  for i in range(QNT_DOCS):
    for termo in termos:
      cossenos[i] += vetores[termo][0] * vetores[termo][i+1]

  # print("cossenos")
  # print(cossenos)

  cossenos_ordenados = sorted(cossenos.items(), key=lambda x: x[1], reverse=True)

  # print("cossenos_ordenados")
  # print(cossenos_ordenados)

  ## Ranquear

  # Criar uma lista de documentos ordenada pelos valores de cosseno
  documentos_ordenados = [doc for doc, _ in cossenos_ordenados]

  # Criar uma string de ranqueamento
  resultado = ">".join([f'vetor{doc+1}' for doc in documentos_ordenados])

  return resultado

caminho = "/content/sample_data/Termos.txt"

## Pegando cada linha do txt de termos
termos = ler_arquivo_txt(caminho)
#print(termos)

## Calculando Termo Invertido, IDF e WTF
termoInv, IDF, WTF = fazer_termo_inv(termos)
#print("termoInv")
#print(termoInv)
#print("IDF")
#print(IDF)
print("WTF")
print(WTF)

## Calculando IDWTF
IDWTF = calcularIDWTF(IDF,WTF)
##print(IDWTF)

while True:
    termos = input("Digite o(s) termo(s) (separe-os por ' ') (digite '0' para sair): ")
    if termos == '0':
        break
    termos = termos.split(" ")
    print(calcularVetorial(termos, IDF, IDWTF))