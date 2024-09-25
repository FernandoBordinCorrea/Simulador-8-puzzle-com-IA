import random
from collections import deque
from tkinter import *

class NoArvore:
    def __init__(self, vetor, valor, movimento):
        self.esquerda = None
        self.direita = None
        self.anterior = None
        self.vetor = vetor
        self.valor = valor
        self.movimento = movimento

    def adicionar(self, no_pai, vetor, direcao, estadoFinal):
        index = no_pai.vetor.index(0)
        linhas, colunas = 3, 3
        linhasMatriz, colunasMatriz = divmod(index, colunas)

        if direcao == "cima" and linhasMatriz > 0:
            novo_index = index - colunas
        elif direcao == "baixo" and linhasMatriz < linhas - 1:
            novo_index = index + colunas
        elif direcao == "esquerda" and colunasMatriz > 0:
            novo_index = index - 1
        elif direcao == "direita" and colunasMatriz < colunas - 1:
            novo_index = index + 1
        else:
            return None

        novo_vetor = vetor.copy()
        novo_vetor[index], novo_vetor[novo_index] = novo_vetor[novo_index], novo_vetor[index]

        novo_no = NoArvore(novo_vetor, 0, direcao)
        novo_no.anterior = no_pai
        novo_no.calcular_valor(estadoFinal)

        self._inserir(no_pai, novo_no)

        return novo_no

    def _inserir(self, no_pai, novo_no):
        if novo_no.valor < no_pai.valor:
            if no_pai.esquerda is None:
                no_pai.esquerda = novo_no
            else:
                self._inserir(no_pai.esquerda, novo_no)
        else:
            if no_pai.direita is None:
                no_pai.direita = novo_no
            else:
                self._inserir(no_pai.direita, novo_no)

    def calcular_valor(self, estadoFinal):
        contador = 0
        for i in range(9):
            if self.vetor[i] == estadoFinal.vetor[i]:
                contador += 1
        self.valor = contador

def busca_largura(estadoInicial, estadoFinal):
    fila = deque([estadoInicial])
    visitados = set()
    visitados.add(tuple(estadoInicial.vetor))
    contador_estados = 0
    resultado =[]

    while fila:
        estadoAtual = fila.popleft()
        contador_estados += 1

        if verificaFinal(estadoAtual, estadoFinal):
            resultado = melhor_caminho(estadoAtual)
            return contador_estados, resultado

        for direcao in ["cima", "baixo", "esquerda", "direita"]:
            novo_estado = estadoAtual.adicionar(estadoAtual, estadoAtual.vetor, direcao, estadoFinal)
            if novo_estado and tuple(novo_estado.vetor) not in visitados:
                visitados.add(tuple(novo_estado.vetor))
                fila.append(novo_estado)

def busca_profundidade(estadoInicial, estadoFinal):
    pilha = [estadoInicial]
    visitados = set()
    visitados.add(tuple(estadoInicial.vetor))
    contador_estados = 0

    while pilha:
        estadoAtual = pilha.pop()
        contador_estados += 1

        if verificaFinal(estadoAtual, estadoFinal):
            resultado = melhor_caminho(estadoAtual)
            return contador_estados, resultado

        for direcao in ["cima", "baixo", "esquerda", "direita"]:
            novo_estado = estadoAtual.adicionar(estadoAtual, estadoAtual.vetor, direcao, estadoFinal)
            if novo_estado and tuple(novo_estado.vetor) not in visitados:
                visitados.add(tuple(novo_estado.vetor))
                pilha.append(novo_estado)

def busca_heuristica(estadoInicial, estadoFinal):
    visitados = set()
    caminho = [estadoInicial]
    contador_estados = 0

    while caminho:
        estadoAtual = caminho[-1]
        contador_estados += 1

        if verificaFinal(estadoAtual, estadoFinal):
            resultado = melhor_caminho(estadoAtual)
            return contador_estados, resultado

        visitados.add(tuple(estadoAtual.vetor))
        melhores_opcoes = []

        for direcao in ["cima", "baixo", "esquerda", "direita"]:
            novo_estado = estadoAtual.adicionar(estadoAtual, estadoAtual.vetor, direcao, estadoFinal)
            if novo_estado and tuple(novo_estado.vetor) not in visitados:
                melhores_opcoes.append(novo_estado)

        if melhores_opcoes:
            melhores_opcoes.sort(key=lambda no: no.valor, reverse=True)
            caminho.append(melhores_opcoes[0])
        else:
            caminho.pop()

    return None

def verificaFinal(estado_atual, estado_final):
    return estado_atual.vetor == estado_final.vetor

def randomizador(estadoAtual):
    while True:
        random.shuffle(estadoAtual.vetor)
        contador = 0

        for i in range(len(estadoAtual.vetor)):
            if estadoAtual.vetor[i] == 0:
                continue
            for j in range(i + 1, len(estadoAtual.vetor)):
                if estadoAtual.vetor[j] != 0 and estadoAtual.vetor[i] > estadoAtual.vetor[j]:
                    contador += 1

        if contador % 2 == 0:
            return estadoAtual.vetor

def melhor_caminho(estadoAtual):
    caminho = []
    while estadoAtual.anterior is not None:
        caminho.append(estadoAtual)
        estadoAtual = estadoAtual.anterior
        
    caminho.reverse()

    return caminho

def tela_inicial():
    for widget in janela.winfo_children():
        widget.destroy()

    global estadoFinal, estadoAtual

    estadoFinal = NoArvore([1, 2, 3, 4, 5, 6, 7, 8, 0], 0, None)

    estadoAtual = NoArvore(estadoFinal.vetor.copy(), 0, None)

    estadoAtual.vetor = randomizador(estadoAtual)

    nome_janela = Label(janela, text='8-Puzzle', bg='beige', font=('Times New Roman', 20, 'bold'), activebackground='#decdb9')
    nome_janela.pack(pady=20)

    botao1 = Button(janela, text="Jogar", bg='#decdb9', font=('Inter', 15), height=1, width=10, command=tela_jogo, activebackground='#decdb9')
    botao1.pack(pady=10)

    botao2 = Button(janela, text="IA", bg='#decdb9', font=('Inter', 15), height=1, width=10, command=tela_ia, activebackground='#decdb9')
    botao2.pack(pady=10)

def tela_jogo():
    for widget in janela.winfo_children():
        widget.destroy()

    Label(janela, text="Resolva o 8-Puzzle", bg='beige', font=('Inter', 18)).pack(pady=20)

    frame_tabuleiro = Frame(janela)
    frame_tabuleiro.pack()

    def atualizar_tabuleiro():
        for i in range(3):
            for j in range(3):
                posicao = i * 3 + j
                valor = estadoAtual.vetor[posicao]

                if valor == 0:
                    texto_botao = " "
                else:
                    texto_botao = str(valor)

                botao = Button(frame_tabuleiro, text=texto_botao, font=('Inter', 20), height=3, width=6, bg="#decdb9", activebackground='#decdb9')
                botao.grid(row=i, column=j, padx=5, pady=5)

                if valor != 0:
                    botao.config(command=lambda posicao=posicao: mover_peca(posicao))

    def mover_peca(posicao_selecionada):
        index_vazio = estadoAtual.vetor.index(0)

        if posicao_selecionada in [index_vazio - 1, index_vazio + 1, index_vazio - 3, index_vazio + 3]:
            estadoAtual.vetor[index_vazio], estadoAtual.vetor[posicao_selecionada] = estadoAtual.vetor[posicao_selecionada], estadoAtual.vetor[index_vazio]
            atualizar_tabuleiro()
            if verificaFinal(estadoAtual, estadoFinal):
                tela_final()

    atualizar_tabuleiro()

    voltar = Button(janela, text="Voltar", bg='#decdb9', font=('Inter', 8, 'bold'), height=1, width=10, command=tela_inicial, activebackground='#decdb9')
    voltar.place(x=10, y=10)

def tela_ia():
    for widget in janela.winfo_children():
        widget.destroy()

    Label(janela, text="Escolha o tipo de IA", bg='beige', font=('Times New Roman', 18)).pack(pady=20)

    Button(janela, text="Busca em Largura", bg='#decdb9', font=('Inter', 15), height=1, width=30, command=lambda: executar_ia("largura"), activebackground='#decdb9').pack(pady=15)
    Button(janela, text="Busca em Profundidade", bg='#decdb9', font=('Inter', 15), height=1, width=30, command=lambda: executar_ia("profundidade"), activebackground='#decdb9').pack(pady=15)
    Button(janela, text="Busca Heurística", bg='#decdb9', font=('Inter', 15), height=1, width=30, command=lambda: executar_ia("heuristica"), activebackground='#decdb9').pack(pady=15)

    Button(janela, text="Voltar", bg='#decdb9', font=('Inter', 8, 'bold'), height=1, width=10, command=tela_inicial, activebackground='#decdb9').place(x=10, y=10)

def executar_ia(tipo):
    if tipo == "largura":
        resultado_numEstados, resultado_caminho = busca_largura(estadoAtual, estadoFinal)
        tela_busca_final(tipo,resultado_numEstados, resultado_caminho)
    elif tipo == "profundidade":
        resultado_numEstados, resultado_caminho = busca_profundidade(estadoAtual, estadoFinal)
        tela_busca_final(tipo,resultado_numEstados, resultado_caminho)
    elif tipo == "heuristica":
        resultado_numEstados, resultado_caminho = busca_heuristica(estadoAtual, estadoFinal)
        tela_busca_final(tipo,resultado_numEstados, resultado_caminho)
        
def tela_busca_final(tipo, resultado_numEstados, resultado_caminho):
    for widget in janela.winfo_children():
        widget.destroy()
        
    estado_temoporario = NoArvore(estadoAtual.vetor.copy(), 0, None)
        
    Label(janela, text="Posição Inicial do 8-Puzzle", bg='beige', font=('Inter', 18)).pack(pady=20)

    frame_tabuleiro = Frame(janela)
    frame_tabuleiro.pack()

    def atualizar_tabuleiro():
        for i in range(3):
            for j in range(3):
                posicao = i * 3 + j
                valor = estado_temoporario.vetor[posicao]

                if valor == 0:
                    texto_botao = " "
                else:
                    texto_botao = str(valor)

                botao = Button(frame_tabuleiro, text=texto_botao, font=('Inter', 20), height=3, width=6, bg="#decdb9", activebackground='#decdb9')
                botao.grid(row=i, column=j, padx=5, pady=5)

                if valor != 0:
                    botao.config(command=lambda posicao=posicao: mover_peca(posicao))

    def mover_peca(posicao_selecionada):
        index_vazio = estado_temoporario.vetor.index(0)

        if posicao_selecionada in [index_vazio - 1, index_vazio + 1, index_vazio - 3, index_vazio + 3]:
            estado_temoporario.vetor[index_vazio], estado_temoporario.vetor[posicao_selecionada] = estado_temoporario.vetor[posicao_selecionada], estado_temoporario.vetor[index_vazio]
            atualizar_tabuleiro()

    atualizar_tabuleiro()

    texto_caminho = Text(janela, height=5, width=27, bg='#decdb9', font=('Inter', 15),  wrap=WORD)
    texto_caminho.pack(pady=20)

    texto_caminho.tag_configure("padronizado", font=('Inter', 15), background='#decdb9', foreground='black', justify='left')

    Label(janela, text=f"O número de estados visitados utilizando o método\n'Busca em {tipo}' foi: \n{resultado_numEstados}", bg='#decdb9', font=('Inter', 15), justify='center').pack(pady=20)

    for i, caminho in enumerate(resultado_caminho, start=1):
        if caminho.movimento:
            texto_caminho.insert(END, f"Movimento número {i}: {caminho.movimento}\n", "padronizado")

    Button(janela, text="Voltar", bg='#decdb9', font=('Inter', 15), height=1, width=30, command=tela_ia, activebackground='#decdb9').pack(pady=10)

def tela_final():
    for widget in janela.winfo_children():
        widget.destroy()

    Label(janela, text="Você venceu!", bg='beige', font=('Inter', 18)).pack(pady=20)

    voltar = Button(janela, text="Voltar", bg='#decdb9', font=('Inter', 8, 'bold'), height=1, width=10, command=tela_inicial, activebackground='#decdb9')
    voltar.place(x=10, y=10)

janela = Tk()
janela.title('8-Puzzle')
janela.geometry('800x800')
janela.configure(bg='beige')

tela_inicial()
janela.mainloop()