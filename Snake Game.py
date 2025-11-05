import pygame
import random
import time

#FUNDO PADRÃO PRETO, CASO A IMAGEM NÃO SEJA CARREGADA
fundo_imagem = None

# FUNÇÃO PARA CRIAR E SALVAR PONTUAÇÃO EM ARQUIVO .TXT
def salvar_pontuacao(pontos):
    with open("pontuacao.txt", "a") as arquivo:
        arquivo.write(f"{pontos}\n")


#FUNÇÃO PARA LER PONTUAÇÕES, TRANSFORMA EM UMA VARIAVEL
def ler_pontuacoes():
    try:
        with open("pontuacao.txt", "r") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        return []

#FUNÇÃO QUE DESENHA A COBRINHA NA TELA
def desenhar():
    if fundo_imagem:
        tela.blit(fundo_imagem, (0, 0))
    else:
        tela.fill((0, 0, 0))
    for parte in cobra:
        pygame.draw.rect(tela, (0, 255, 0), (parte[0], parte[1], 10, 10))
    pygame.draw.rect(tela, (255, 0, 0), (comida[0], comida[1], 10, 10))

    fonte_pontuacao = pygame.font.Font('fonte_pontuacao.ttf', 20)
    texto = fonte_pontuacao.render(F"PONTUAÇÃO: {pontos}", True, (255,255,255))
    textoRect = texto.get_rect()
    textoRect.center = (300, 57)
    tela.blit(texto, textoRect)

    pygame.display.update()


#FUNÇÃO QUE COLOCA A TELA DE GAMEOVER QUANDO O JOGADOR PERDE
def game_over():
    pygame.mixer.music.stop()
    time.sleep(1)

    #TELA FICA PRETA PARA A APARIÇÃO DO GAMEOVER
    tela.fill((0, 0, 0))

    #INFORMAÇÕES DA FONTE DA TALA DE GAMEOVER
    fonte_gameover = pygame.font.Font('fonte_gameover.ttf', 50)
    texto_gameover = fonte_gameover.render(F"GAME OVER", True, (255,0,0))
    textoRect = texto_gameover.get_rect()
    textoRect.center = (300, 190)
    tela.blit(texto_gameover, textoRect)

    #INFORMAÇÕES DA FONTA DO PLACAR FINAL NA TELA DE GAMEOVER
    fonte_pontuacao = pygame.font.Font('fonte_gameover.ttf', 22)
    texto = fonte_pontuacao.render(F"PONTUACAO FINAL: {pontos}", True, (255,255,255))
    textoRect = texto.get_rect()
    textoRect.center = (300, 230)
    tela.blit(texto, textoRect)

    som_gameover.play()

    pygame.display.update()

    time.sleep(7)

def menu_jogo():
    #FICA REPETINDO A SOUNDTRACK DO MENU ATÉ A TECLA ESPAÇO SER PRESSIONADA
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    esperando = True
    while esperando:
        #POSSIBILTA QUE A TELA DE MENU FUNCIONE DIREITO E QUE DÊ PARA FECHAR NO X
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            #VERIFICA SE TEM TECLA SENDO PRESSIONADA, SE FOR A TECLA ESPAÇO ESPERANDO = FALSE E ENTRA NO WHILE DO JOGO
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False

        #DESENHA A TELA DO MENU
        tela.blit(fundo_menu, (0, 0))
        pygame.display.update()
        
    # 1.5 SEGUNDOS DE FADE OUT NA MÚSICA
    pygame.mixer.music.fadeout(1500)
        
#INICIALIZA O PYGAME, FONTES E MIXER
pygame.mixer.init()
pygame.init()
pygame.font.init()


#IMAGEM DO FUNDO
imagem_fundo = 'background.png'

#IMAGEM DO MENU INICIAL
imagem_menu = 'tela_menu.png'

#SOUNDTRACK DO JOGO
musica_fundo = 'Trilha-sonora.ogg'
musica_menu = 'musica_menu.ogg'
musica_game_over = 'game-over.ogg'
comendo = 'comendo.ogg'


#SOM GAMEOVER QUANDO O JOGADOR PERDER
som_gameover = pygame.mixer.Sound(musica_game_over)
som_gameover.set_volume(0.6)


#SOM QUANDO A COBRA COME A MAÇÃ
som_comendo = pygame.mixer.Sound(comendo)
som_comendo.set_volume(0.6)

#TAMANHO DA TELA E NOME DA JANELA
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Jogo da cobrinha - APC")

#CARREGA A IMAGEM DO MENU E REDIMENCIONA ELA PARA 600x400
fundo_menu_original = pygame.image.load(imagem_menu).convert()
fundo_menu = pygame.transform.scale(fundo_menu_original, (600, 400))


#CARREGA A IMAGEM DE FUNDO E REDIMENCIONA ELA PARA 600x400
fundo_imagem_original = pygame.image.load(imagem_fundo).convert()
fundo_imagem = pygame.transform.scale(fundo_imagem_original, (600, 400))


#INFORMAÇÕES DOS ELEMENTOS
cobra = [(120, 250)]
direcao = (10, 0)
comida = (300, 200)
pontos = 0


rodando = True
velocidade = pygame.time.Clock()

menu_jogo()

#FICA REPETINDO A SOUNDTRACK DE FUNDO ATÉ TER O GAMEOVER
pygame.mixer.music.load(musica_fundo)
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

while rodando:
    #POSSIBILTA QUE O JOGO FUNCIONE DIREITO E QUE DÊ PARA FECHAR NO X
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        #SISTEMA DE CONTROLES DO JOGO (WASD/KEYS: LEFT, RIGHT, UP, DOWN) + MUDANÇA DE DIREÇÃO DA COBRINHA
        if evento.type == pygame.KEYDOWN:
            if (evento.key == pygame.K_w)  or (evento.key == pygame.K_UP):
                direcao = (0, -10)
            elif (evento.key == pygame.K_s)  or (evento.key == pygame.K_DOWN):
                direcao = (0, 10)
            elif (evento.key == pygame.K_a)  or (evento.key == pygame.K_LEFT):
                direcao = (-10, 0)
            elif (evento.key == pygame.K_d)  or (evento.key == pygame.K_RIGHT):
                direcao = (10, 0)

    nova_cabeca = (cobra[0][0] + direcao[0], cobra[0][1] + direcao[1])
    cobra.insert(0, nova_cabeca)
    
    #ATUALIZAÇÃO DA COBRINHA DE ACORDO QUE COME AS MAÇÃS
    if nova_cabeca == comida:
        som_comendo.play()
        pontos += 1

        #SISTEMA DE SPAWN DAS MAÇÃS
        comida = (random.randrange(30, 570, 10),
                  random.randrange(80, 340, 10))
    else:
        cobra.pop()
        
    #SISTEMA DE COLISÃO DA COBRINHA SE A CABEÇA FOR DE ENCONTRO COM O CORPO
    if nova_cabeca in cobra[1:]:
        rodando = False
    elif nova_cabeca[0] < 30 or nova_cabeca[0] >= 570:
        rodando = False
    elif nova_cabeca[1] < 75 or nova_cabeca[1] >= 360:
        rodando = False

    #DETECTA SE RODANDO FOR == FALSE E REPRODUZ O SOM E A TELA DE GAMEOVER
    if not rodando:
        game_over()

    desenhar()
    
    #DEFINE O FPS/VELOCIDADE DO JOGO
    if pontos < 20:
        velocidade_atual = 13   #LENTA
    elif pontos < 40:
        velocidade_atual = 16   #MÉDIA
    else:
        velocidade_atual = 20   #RÁPIDA

    velocidade.tick(velocidade_atual)

salvar_pontuacao(pontos)
pygame.quit()

print(f"\nPontuação Final: {pontos}")

print("\nHistórico de pontuações:")
for pontuação in ler_pontuacoes():
    print(pontuação.strip())