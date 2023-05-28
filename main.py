import pygame, os, random

# Definindo as constantes de nosso game:
TELA_LARGURA = 300
TELA_ALTURA = 600

IMAGEM_CANO = (pygame.image.load(os.path.join('assets','pipe.png')))
IMAGEM_CHAO = (pygame.image.load(os.path.join('assets','base.png')))


IMAGEM_BACKGROUND = (pygame.image.load(os.path.join('assets','bg.png')))
IMAGEM_BACKGROUND = pygame.transform.scale(IMAGEM_BACKGROUND, (
    IMAGEM_BACKGROUND.get_width() * 1.5,
    IMAGEM_BACKGROUND.get_height() * 1.5,
))

IMAGENS_PASSARO = [
     (pygame.image.load(os.path.join('assets','bird1.png'))),
      (pygame.image.load(os.path.join('assets','bird2.png'))),
       (pygame.image.load(os.path.join('assets','bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('jura',25)

# Definindo as Classes

class Passaro():
    IMAGENS = IMAGENS_PASSARO
    #animaçoes da rotacao:
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    
    def __init__(self,x ,y) -> None:
        self.x = x
        self.y = y

        self.angulo = 0
        self.velocidade = 0 
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagens = self.IMAGENS[0]

    def pular(self):
        self.velocidade = -8
        self.tempo = 0
        self.altura = self.y
    
    def mover(self):
        # Calcular o deslocamento:
        self.tempo += 1 
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo # formula do deslocamento

        # Restringir o deslocamento:
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Dar atenção ao Angulo do Passaro: 
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
        
    def desenhar(self, tela):
        # Definir qual imagem usar:
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagens = self.IMAGENS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagens = self.IMAGENS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagens = self.IMAGENS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagens = self.IMAGENS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4 +1:
            self.imagens = self.IMAGENS[0]
            self.contagem_imagem = 0

        # Se o passaro estiver caindo, nao bater asa
        if self.angulo <= -80:
            self.imagens = self.IMAGENS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # Desenhar a imagem:
        imagem_rotacionada = pygame.transform.rotate(self.imagens, self.angulo)
        posicao_centro_imagem = self.imagens.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagens)

class Cano():
    DISTANCIA = 150
    VELOCIDADE = 5

    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0 
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(30,270)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao():
    VELOCIDADE = 5
    LARGURA = IMAGEM_CANO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y) -> None:
        self.y = y
        self.chao_1 = 0
        self.chao_2 = self.LARGURA

    def mover(self):
        self.chao_1 -= self.VELOCIDADE
        self.chao_2 -= self.VELOCIDADE

        if self.chao_1 + self.LARGURA < 0:
            self.chao_1 = self.chao_2 + self.LARGURA
        
        if self.chao_2 + self.LARGURA < 0:
            self.chao_2 = self.chao_1 + self.LARGURA
        
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.chao_1, self.y))
        tela.blit(self.IMAGEM, (self.chao_2, self.y))
        

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0,0))
    
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"PONTOS: {pontos}", 0, (255,255,255))
    tela.blit(texto, (TELA_LARGURA -10 - texto.get_width(), 10))
    chao.desenhar(tela)

    pygame.display.update()

def main():
    passaros = [Passaro((TELA_LARGURA/2)-60, TELA_ALTURA/2)]
    chao = Chao(TELA_ALTURA-50)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30) # Definindo os FPS do game!
        
        # Interagindo com o game:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        
        # Movendo os elementos da cena!
        for passaro in passaros:
            passaro.mover()

        chao.mover()
        
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagens.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)



        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == "__main__":
    main()  

