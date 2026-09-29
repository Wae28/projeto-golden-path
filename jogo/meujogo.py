import pygame
import sys
import os

# =========================================================
# INICIALIZAÇÃO
# =========================================================

pygame.init()

# =========================================================
# CONFIGURAÇÃO DE DIRETÓRIOS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJETO_DIR = os.path.dirname(BASE_DIR)
AVATARES_DIR = os.path.join(PROJETO_DIR, "avatares")

# =========================================================
# TELA
# =========================================================

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com Escolha de Avatar")

relogio = pygame.time.Clock()

TAMANHO = 100

# =========================================================
# INVENTÁRIO DE MAÇÃS
# =========================================================

MAX_MACAS = 3
quantidade_macas = 3

TAMANHO_MACA = 30
ESPACO_MACA = 8

X_INVENTARIO = 20
Y_INVENTARIO = 20

# =========================================================
# CARREGAR IMAGEM DA MAÇÃ
# =========================================================

caminho_maca = os.path.join(
    AVATARES_DIR,
    "maca.png"
)

try:
    maca_img = pygame.image.load(
        caminho_maca
    ).convert_alpha()

    maca_img = pygame.transform.scale(
        maca_img,
        (TAMANHO_MACA, TAMANHO_MACA)
    )

except:
    maca_img = None

# =========================================================
# FUNÇÃO PARA CARREGAR AVATAR
# =========================================================

def carregar_avatar(prefixo, inverter_original=False):

    frames_walk_base = []

    # =====================================================
    # CARREGAR FRAMES DE CAMINHADA
    # =====================================================

    try:
        arquivos = sorted(os.listdir(AVATARES_DIR))
    except:
        arquivos = []

    for nome in arquivos:

        if (
            nome.lower().startswith(
                prefixo.lower() + "frame"
            )
            and nome.lower().endswith(".png")
        ):

            try:
                caminho = os.path.join(
                    AVATARES_DIR,
                    nome
                )

                img = pygame.image.load(
                    caminho
                ).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (TAMANHO, TAMANHO)
                )

                frames_walk_base.append(img)

            except:
                continue

    # =====================================================
    # CASO NÃO ENCONTRE OS FRAMES
    # =====================================================

    if not frames_walk_base:

        try:
            caminho = os.path.join(
                AVATARES_DIR,
                prefixo + "frame0.png"
            )

            img = pygame.image.load(
                caminho
            ).convert_alpha()

            img = pygame.transform.scale(
                img,
                (TAMANHO, TAMANHO)
            )

            frames_walk_base = [img]

        except:

            fallback = pygame.Surface(
                (TAMANHO, TAMANHO),
                pygame.SRCALPHA
            )

            fallback.fill(
                (255, 0, 0, 255)
            )

            frames_walk_base = [fallback]

    # =====================================================
    # CARREGAR UMA IMAGEM INDIVIDUAL
    # =====================================================

    def carregar_unico(nome_arquivo):

        try:
            caminho = os.path.join(
                AVATARES_DIR,
                nome_arquivo + ".png"
            )

            img = pygame.image.load(
                caminho
            ).convert_alpha()

            return pygame.transform.scale(
                img,
                (TAMANHO, TAMANHO)
            )

        except:
            return frames_walk_base[0]

    # =====================================================
    # IMAGENS BASE
    # =====================================================

    idle_base = carregar_unico(
        prefixo + "frame0"
    )

    pulo_base = carregar_unico(
        prefixo + "pulo"
    )

    caindo_base = carregar_unico(
        prefixo + "caindo"
    )

    caida_base = carregar_unico(
        prefixo + "caida"
    )

    preparar_base = carregar_unico(
        prefixo + "preparandopulo"
    )

    # =====================================================
    # AGACHADO
    #
    # Avatar 2:
    # avatar2agachado.png
    #
    # Outros:
    # avatar1abaixado.png
    # avatar3abaixado.png
    # avatar4abaixado.png
    # =====================================================

    if prefixo.lower() == "avatar2":

        abaixado_base = carregar_unico(
            prefixo + "agachado"
        )

    else:

        abaixado_base = carregar_unico(
            prefixo + "abaixado"
        )


    
    # =====================================================
    # AUMENTAR PULO E AGACHAMENTO DO AVATAR 2
    # =====================================================

    if prefixo.lower() == "avatar2":
        TAMANHO_ESPECIAL = 130

        # Aumenta somente o frame de pulo
        pulo_base = pygame.transform.scale(
            pulo_base,
            (TAMANHO_ESPECIAL, TAMANHO_ESPECIAL)
        )

        # Aumenta somente o frame de agachamento
        abaixado_base = pygame.transform.scale(
            abaixado_base,
            (TAMANHO_ESPECIAL, TAMANHO_ESPECIAL)
        )

    # =====================================================
    # DIREÇÃO DO AVATAR
    # =====================================================

    if inverter_original:

        frames_walk_dir = frames_walk_base

        frames_walk_esq = [
            pygame.transform.flip(
                frame,
                True,
                False
            )
            for frame in frames_walk_base
        ]

    else:

        frames_walk_esq = frames_walk_base

        frames_walk_dir = [
            pygame.transform.flip(
                frame,
                True,
                False
            )
            for frame in frames_walk_base
        ]

    # =====================================================
    # RETORNAR TODAS AS IMAGENS
    # =====================================================

    return {

        # -------------------------------------------------
        # WALK
        # -------------------------------------------------

        "walk_esq": frames_walk_esq,
        "walk_dir": frames_walk_dir,

        # -------------------------------------------------
        # IDLE
        # -------------------------------------------------

        "idle_esq": (
            pygame.transform.flip(
                idle_base,
                True,
                False
            )
            if inverter_original
            else idle_base
        ),

        "idle_dir": (
            idle_base
            if inverter_original
            else pygame.transform.flip(
                idle_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # PULO
        # -------------------------------------------------

        "pulo_esq": (
            pygame.transform.flip(
                pulo_base,
                True,
                False
            )
            if inverter_original
            else pulo_base
        ),

        "pulo_dir": (
            pulo_base
            if inverter_original
            else pygame.transform.flip(
                pulo_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # CAINDO
        # -------------------------------------------------

        "caindo_esq": (
            pygame.transform.flip(
                caindo_base,
                True,
                False
            )
            if inverter_original
            else caindo_base
        ),

        "caindo_dir": (
            caindo_base
            if inverter_original
            else pygame.transform.flip(
                caindo_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # CAÍDA
        # -------------------------------------------------

        "caida_esq": (
            pygame.transform.flip(
                caida_base,
                True,
                False
            )
            if inverter_original
            else caida_base
        ),

        "caida_dir": (
            caida_base
            if inverter_original
            else pygame.transform.flip(
                caida_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # PREPARANDO PULO
        # -------------------------------------------------

        "preparar_esq": (
            pygame.transform.flip(
                preparar_base,
                True,
                False
            )
            if inverter_original
            else preparar_base
        ),

        "preparar_dir": (
            preparar_base
            if inverter_original
            else pygame.transform.flip(
                preparar_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # AGACHADO
        # -------------------------------------------------

        "abaixado_esq": (
            pygame.transform.flip(
                abaixado_base,
                True,
                False
            )
            if inverter_original
            else abaixado_base
        ),

        "abaixado_dir": (
            abaixado_base
            if inverter_original
            else pygame.transform.flip(
                abaixado_base,
                True,
                False
            )
        )
    }


# =========================================================
# CARREGAMENTO DOS AVATARES
# =========================================================

avatar1 = carregar_avatar(
    "avatar1",
    inverter_original=True
)

avatar2 = carregar_avatar(
    "avatar2",
    inverter_original=False
)

avatar3 = carregar_avatar(
    "avatar3",
    inverter_original=False
)

avatar4 = carregar_avatar(
    "avatar4",
    inverter_original=False
)

lista_avatares = [
    avatar1,
    avatar2,
    avatar3,
    avatar4
]

# =========================================================
# CARREGAR CENÁRIO
# =========================================================

def carregar_fundo(nome):

    # Primeiro tenta dentro da pasta do jogo

    caminho = os.path.join(
        BASE_DIR,
        nome
    )

    # Se não encontrar, tenta na pasta principal

    if not os.path.exists(caminho):

        caminho = os.path.join(
            PROJETO_DIR,
            nome
        )

    try:

        fundo = pygame.image.load(
            caminho
        ).convert()

        fundo = pygame.transform.scale(
            fundo,
            (
                LARGURA,
                ALTURA
            )
        )

        return fundo

    except:

        fundo = pygame.Surface(
            (
                LARGURA,
                ALTURA
            )
        )

        fundo.fill(
            (255, 192, 203)
        )

        return fundo


fundo = carregar_fundo(
    "cenario1.png"
)

# =========================================================
# MENU DE ESCOLHA DE AVATAR
# =========================================================

fonte = pygame.font.SysFont(
    "arial",
    30
)

botoes = [
    pygame.Rect(
        100 + i * 160,
        220,
        120,
        120
    )
    for i in range(4)
]

avatar_escolhido = avatar1
escolhendo_avatar = True

# =========================================================
# LOOP DO MENU
# =========================================================

while escolhendo_avatar:

    tela.fill(
        (230, 230, 250)
    )

    # =====================================================
    # TÍTULO
    # =====================================================

    titulo = fonte.render(
        "Escolha seu Avatar",
        True,
        (0, 0, 0)
    )

    titulo_rect = titulo.get_rect(
        center=(
            LARGURA // 2,
            100
        )
    )

    tela.blit(
        titulo,
        titulo_rect
    )

    # =====================================================
    # DESENHAR OS QUATRO AVATARES
    # =====================================================

    for i, botao in enumerate(botoes):

        pygame.draw.rect(
            tela,
            (255, 255, 255),
            botao,
            border_radius=20
        )

        img_menu = lista_avatares[i]["idle_dir"]

        img_rect = img_menu.get_rect(
            center=botao.center
        )

        tela.blit(
            img_menu,
            img_rect
        )

    # =====================================================
    # EVENTOS
    # =====================================================

    for evento in pygame.event.get():

        # -------------------------------------------------
        # FECHAR JOGO
        # -------------------------------------------------

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # -------------------------------------------------
        # CLIQUE DO MOUSE
        # -------------------------------------------------

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                for i, botao in enumerate(botoes):

                    if botao.collidepoint(
                        evento.pos
                    ):

                        avatar_escolhido = lista_avatares[i]

                        escolhendo_avatar = False

                        print(
                            "Avatar escolhido:",
                            i + 1
                        )

    pygame.display.update()
    relogio.tick(60)

# =========================================================
# VARIÁVEIS DO JOGO
# =========================================================

x = 400
y = 400

vel_x = 5
vel_y = 0

gravidade = 0.5
forca_pulo = -12

chao = 400

no_chao = True

olhando_direita = True

tempo_animacao = 0
vel_animacao = 0.2

tempo_pouso = 0

# =========================================================
# LOOP PRINCIPAL
# =========================================================

while True:

    # =====================================================
    # DESENHAR FUNDO
    # =====================================================

    tela.blit(
        fundo,
        (0, 0)
    )

    # =====================================================
    # EVENTOS
    # =====================================================

    for evento in pygame.event.get():

        # -------------------------------------------------
        # SAIR
        # -------------------------------------------------

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # -------------------------------------------------
        # PULO
        # -------------------------------------------------

        if evento.type == pygame.KEYDOWN:

            if evento.key in [
                pygame.K_SPACE,
                pygame.K_UP
            ]:

                if no_chao:

                    vel_y = forca_pulo
                    no_chao = False

    # =====================================================
    # TECLAS
    # =====================================================

    teclas = pygame.key.get_pressed()

    movendo = False

    abaixado = teclas[
        pygame.K_DOWN
    ]

    # =====================================================
    # MOVIMENTO
    # =====================================================

    if not abaixado:

        # -------------------------------------------------
        # ESQUERDA
        # -------------------------------------------------

        if teclas[pygame.K_LEFT]:

            if x > 0:

                x -= vel_x

                movendo = True

                olhando_direita = False

        # -------------------------------------------------
        # DIREITA
        # -------------------------------------------------

        if teclas[pygame.K_RIGHT]:

            if x < LARGURA - TAMANHO:

                x += vel_x

                movendo = True

                olhando_direita = True

    # =====================================================
    # FÍSICA
    # =====================================================

    vel_y += gravidade
    y += vel_y

    # =====================================================
    # CHÃO
    # =====================================================

    if y >= chao:

        if not no_chao:

            tempo_pouso = 10

        y = chao

        vel_y = 0

        no_chao = True

    # =====================================================
    # DETERMINAR ESTADO
    # =====================================================

    if abaixado and no_chao:

        estado = "abaixado"

    elif not no_chao:

        # -------------------------------------------------
        # SUBINDO
        # -------------------------------------------------

        if vel_y < -2:

            estado = "pulo"

        # -------------------------------------------------
        # DESCENDO
        # -------------------------------------------------

        elif vel_y > 2:

            estado = "caindo"

        # -------------------------------------------------
        # PONTO MAIS ALTO
        # -------------------------------------------------

        else:

            estado = "preparar"

    else:

        # -------------------------------------------------
        # ACABOU DE POUSAR
        # -------------------------------------------------

        if tempo_pouso > 0:

            estado = "caida"

            tempo_pouso -= 1

        # -------------------------------------------------
        # CAMINHANDO
        # -------------------------------------------------

        elif movendo:

            estado = "walk"

        # -------------------------------------------------
        # PARADO
        # -------------------------------------------------

        else:

            estado = "idle"

    # =====================================================
    # ESCOLHER DIREÇÃO
    # =====================================================

    if olhando_direita:

        sufixo = "_dir"

    else:

        sufixo = "_esq"

    # =====================================================
    # ESCOLHER IMAGEM
    # =====================================================

    if estado == "walk":

        tempo_animacao += vel_animacao

        quantidade_frames = len(
            avatar_escolhido[
                "walk" + sufixo
            ]
        )

        if quantidade_frames <= 0:

            quantidade_frames = 1

        if tempo_animacao >= quantidade_frames:

            tempo_animacao = 0

        imagem = avatar_escolhido[
            "walk" + sufixo
        ][
            int(tempo_animacao)
        ]

    else:

        imagem = avatar_escolhido[
            estado + sufixo
        ]

    # =====================================================
    # POSICIONAR PERSONAGEM
    # =====================================================

    # Mantém os pés no mesmo lugar mesmo com o avatar2 maior.
    tamanho_imagem = imagem.get_height()

    rect = imagem.get_rect(
        midbottom=(
            x + TAMANHO // 2,
            y + tamanho_imagem
        )
    )

    # =====================================================
    # DESENHAR PERSONAGEM
    # =====================================================

    tela.blit(
        imagem,
        rect
    )

    # =====================================================
    # DESENHAR MAÇÃS
    # =====================================================

    for i in range(quantidade_macas):

        if maca_img is not None:

            maca_rect = maca_img.get_rect(
                topleft=(
                    X_INVENTARIO
                    + i * (
                        TAMANHO_MACA
                        + ESPACO_MACA
                    ),
                    Y_INVENTARIO
                )
            )

            tela.blit(
                maca_img,
                maca_rect
            )

    # =====================================================
    # ATUALIZAR TELA
    # =====================================================

    pygame.display.update()

    relogio.tick(60)