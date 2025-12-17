import pygame
import sys

# igra je identična kot v C verziji samo GUI je dodan

# velikost okna
SIRINA, VISINA = 1920, 1080
CELICA_SIZE = 180
POLJE_SIZE_PX = CELICA_SIZE * 3
POLJE_LEVO = (SIRINA - POLJE_SIZE_PX) // 2  # sredina
POLJE_VRH = 200
LINE_SIRINA = 15

# barve
BG_BARVA = (28, 28, 28)
POLJE_BARVA = (200, 200, 200)
X_BARVA = (255, 100, 100)
O_BARVA = (100, 200, 255)
TEXT_BARVA = (255, 255, 255)
GUMB_BARVA = (70, 130, 180)
GUMB_HOVER = (100, 160, 210)

pygame.init()
zaslon = pygame.display.set_mode((SIRINA, VISINA))
pygame.display.set_caption("3 v vrsto")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Times new roman", 60, bold=True)
font_med = pygame.font.SysFont("Calibri", 40)
font_small = pygame.font.SysFont("segoeui", 32)

board = [[' ' for _ in range(3)] for _ in range(3)]
PLAYER = 'X'
COMPUTER = 'O'

def reset_board():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

def draw_board():
    zaslon.fill(BG_BARVA)
    
    # mreža
    board_y = POLJE_VRH
    board_x = POLJE_LEVO
    for i in range(1, 3):
        pygame.draw.line(zaslon, POLJE_BARVA, (board_x + i * CELICA_SIZE, board_y), (board_x + i * CELICA_SIZE, board_y + POLJE_SIZE_PX), LINE_SIRINA)
        
        pygame.draw.line(zaslon, POLJE_BARVA, (board_x, board_y + i * CELICA_SIZE), (board_x + POLJE_SIZE_PX, board_y + i * CELICA_SIZE), LINE_SIRINA)

    # xoxo
    for i in range(3):
        for j in range(3):
            cx = board_x + j * CELICA_SIZE + CELICA_SIZE // 2
            cy = board_y + i * CELICA_SIZE + CELICA_SIZE // 2
            if board[i][j] == 'X':
                pygame.draw.line(zaslon, X_BARVA, (cx - 76, cy - 82), (cx + 74, cy + 82), LINE_SIRINA - 2)
                pygame.draw.line(zaslon, X_BARVA, (cx - 76, cy + 82), (cx + 74, cy - 82), LINE_SIRINA - 2)
            elif board[i][j] == 'O':
                pygame.draw.circle(zaslon, O_BARVA, (cx, cy), 80, LINE_SIRINA - 3)




def check_winner():
    for i in range(3):
        if board[i][0] != ' ' and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
    for j in range(3):
        if board[0][j] != ' ' and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return ' '

def are_free_spaces():
    return any(' ' in row for row in board)

def minimax(depth, is_maximizing):
    result = check_winner()
    if result == COMPUTER:
        return 10 - depth
    elif result == PLAYER:
        return depth - 10
    elif not are_free_spaces():
        return 0




# algoritem za računalniško potezo
# identičen kot v C verziji
    if is_maximizing:
        best = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = COMPUTER
                    best = max(best, minimax(depth + 1, False))
                    board[i][j] = ' '
        return best
    # !isMaximizing tukaj
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = PLAYER
                    best = min(best, minimax(depth + 1, True))
                    board[i][j] = ' '
        return best

def computer_move():
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = COMPUTER
                score = minimax(0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = COMPUTER





def draw_text_center(text, font, BARVA, y):
    surf = font.render(text, True, BARVA)
    rect = surf.get_rect(center=(SIRINA // 2, y))
    zaslon.blit(surf, rect)

# večina funkcij tle notri ima lambda uporabo kot zgleda se naredi objekt (nekako kot strukt za ustvarit)
def draw_button(text, center_x, y):
    # dobi 2-terico x,y miške ob trenutku
    mouse = pygame.mouse.get_pos()

    btn_rect = pygame.Rect(center_x - 80, y, 160, 60)
    # barva glede na to če je miška na gumbu ali ni
    BARVA = (GUMB_HOVER) if btn_rect.collidepoint(mouse) else GUMB_BARVA
    # rect kot rectangle radius da zaolbjeno obliko
    pygame.draw.rect(zaslon, BARVA, btn_rect, border_radius=100)
    txt = font_med.render(text, True, (255, 255, 255))
    zaslon.blit(txt, txt.get_rect(center=btn_rect.center))
    return btn_rect



# od tu dol se igra
want_to_play = True

while want_to_play:
    reset_board()
    winner = ' '

    # dokler ni zmagovalca in so še možne poteze
    while winner == ' ' and are_free_spaces():
        draw_board()                    
        pygame.display.flip()
        # omeji FPS na 60 da ne uniči računalnika xd
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if POLJE_VRH <= my < POLJE_VRH + POLJE_SIZE_PX:
                    col = (mx - POLJE_LEVO) // CELICA_SIZE
                    row = (my - POLJE_VRH) // CELICA_SIZE
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
                        board[row][col] = PLAYER
                        winner = check_winner()
                        if winner == ' ' and are_free_spaces():
                            computer_move()
                            winner = check_winner()

    # Konec igre
    draw_board()

    y = 80

    if winner == COMPUTER:
        draw_text_center("IZGUBIL SI!", font_big, (255, 100, 100), y)
        y += 70
        draw_text_center("TOČKE: 0", font_med, TEXT_BARVA, y)
    else:
        draw_text_center("IZENAČENO!", font_big, (200, 200, 200), y)
        y += 70
        draw_text_center("TOČKE : 0", font_med, TEXT_BARVA, y)



    y += POLJE_VRH + POLJE_SIZE_PX - 80
    draw_text_center("Ali želite še igrati?", font_med, TEXT_BARVA, y)

    y += 40
    da_rect = draw_button("Da", SIRINA // 2 - 120, y)
    ne_rect = draw_button("Ne", SIRINA // 2 + 120, y)

    da_center_x = SIRINA // 2 - 120
    ne_center_x = SIRINA // 2 + 120

    pygame.display.flip()

    # Čakanje na izbiro
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if da_rect.collidepoint(event.pos):
                    want_to_play = True
                    waiting = False
                elif ne_rect.collidepoint(event.pos):
                    want_to_play = False
                    waiting = False
        da_rect = draw_button("Da", da_center_x, y)
        ne_rect = draw_button("Ne", ne_center_x, y)
        pygame.display.flip()
        clock.tick(30)

# Poslovilni ekran
zaslon.fill(BG_BARVA)

draw_text_center("HVALA, DA SI SE POIGRAL/A!", font_big, (255, 255, 200), VISINA // 2 - 100)

# ta flip funkcija izrisuje stvari drugače se samo shranijo pa ne izpišejo. Baje da je lažja alternativa / manj zahtevna na procesor če samo izrišeš slike gor na ekran in ne updateaš vedno ko je treba izrisat
pygame.display.flip()
pygame.time.wait(2000)

pygame.quit()