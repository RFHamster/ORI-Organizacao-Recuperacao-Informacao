import nltk
from nltk.corpus import stopwords
import string
import fitz
import pandas as pd
from nltk.stem import RSLPStemmer
import spacy
from unidecode import unidecode
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

def abrir_e_ler_pdf(arquivo):
    documento = fitz.open(arquivo)
    texto = ''
    for numero_pagina in range(documento.page_count):
        pagina = documento.load_page(numero_pagina)
        texto += pagina.get_text()
    documento.close()
    return texto.lower()

def remover_pontuacao(texto):
    for pontuacao in string.punctuation:
        texto = texto.replace(pontuacao, '')
    return texto

def tokenizacao(texto):
    return nltk.word_tokenize(texto)

def remover_stopwords(tokenizados):
    stop_words = stopwords.words('portuguese')
    return [palavra for palavra in tokenizados if palavra not in stop_words]

def encontrar_stopwords(ocultas):
    stop_words = stopwords.words('portuguese')
    return [palavra for palavra in ocultas if palavra in stop_words]

def lematizacao_rslp(texto):
    # Definir erros e o que deve fazer com eles, subtituir ou excluir
    substituicoes = {
        "falasse": "falar",
        "brinca": "brincar",
        "bichinho": "bicho",
        "piãor": "pião",
        "borboleto": "borboleta",
        "ligeirinho": "ligeiro",
        "alegr": "alegre",
        "amarelinha": "amarela",
        "ruo": "rua",
        "escar": "escadas",
        "durar": "dura",
        "redondar": "redonda",
        "pode": "poder",
        "madeiro": "madeira",
        "abrar": "abrir",
        "devagarinho": "devagar",
        "abro": "abrir",
        "supetãor": "supetão",
        "fecho": "fechar",
        "tamanquinho": "tamanco",
    }
    removidos = ['—', '…','ohr','tão','então','pra','troc']

    # Carregando portuges para o spaCy e pondo em lematizando no texto
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(" ".join(texto))
    lematizadas = [token.lemma_ for token in doc]

    # Arrumando erros
    lematizadas = [substituicoes.get(lemma, lemma) for lemma in lematizadas]
    lematizadas = [lemma for lemma in lematizadas if lemma not in removidos]

    # Tirando acentos e colocando para minusculas
    lematizadas = [unidecode(lemma).lower() for lemma in lematizadas]

    return lematizadas

# Abrir
textos = [
    abrir_e_ler_pdf('/content/sample_data/Arquivos/Pontinho_de_Vista_Pedro_Bandeira.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/Convite_José_Paulo_Paes.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/As_borboletas_Vinicius_de_Moraes.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/Ao_pé_de_sua_criança_Pablo_Neruda.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/A_porta_Vinicius_de_Moraes.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/A_Centopeia_Marina_Colasanti.pdf'),
    abrir_e_ler_pdf('/content/sample_data/Arquivos/A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf')
]

# Remover pontuação
textos = [remover_pontuacao(texto) for texto in textos]

# Tokenizar
tokenizados_textos = [tokenizacao(texto) for texto in textos]

# Salvar stopwords
stopwords_textos = [encontrar_stopwords(tokenizado_texto) for tokenizado_texto in tokenizados_textos]
#print(stopwords_textos)

#Remover stopwords
textos_sem_stopwords = [remover_stopwords(tokenizado_texto) for tokenizado_texto in tokenizados_textos]
#print(textos_sem_stopwords)

# Lematizar com spaCy
textos_estimizados = [lematizacao_rslp(texto) for texto in textos_sem_stopwords]
print(textos_estimizados)

# Criar um DataFrame
colunas = ['Palavras'] + ['Texto{}'.format(i+1) for i in range(len(textos))]
df = pd.DataFrame(columns=colunas)

# Preencher a Matriz
todas_palavras = list(set([palavra for texto in textos_estimizados for palavra in texto]))
#print(todas_palavras)

todas_palavras.sort()  # Ordenar as palavras em ordem alfabética
df['Palavras'] = todas_palavras

# Contador de arquivos onde cada palavra aparece
contadores = {palavra: 0 for palavra in todas_palavras}

for i, texto_lematizado in enumerate(textos_estimizados):
    df['Texto{}'.format(i+1)] = [texto_lematizado.count(palavra) for palavra in todas_palavras]
    for palavra in todas_palavras:
        if palavra in texto_lematizado:
            contadores[palavra] += 1

# Preencher valores NaN com 0
df = df.fillna(0)

# Criar e escrever arquivo txt
with open('/content/sample_data/Arquivos/Resposta.txt', 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        palavra = row['Palavras']
        ocorrencias = []
        for col in df.columns[1:]:
            texto_numero = col.replace('Texto', '')
            quantidade = row[col]
            if quantidade > 0:
                ocorrencias.append('{}/{}'.format(texto_numero, quantidade))
        linha = '{}/{} -> {}'.format(palavra, contadores[palavra], ', '.join(ocorrencias))
        f.write(linha + '\n')

