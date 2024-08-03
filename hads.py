import pygame
import random
import sys
import time



# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treinamento de Digitação")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Carregar imagem da tela inicial
hand_image = pygame.image.load('hand_position.png')
hand_image_rect = hand_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Fonte
font = pygame.font.Font(None, 54)
small_font = pygame.font.Font(None, 36)

# Estado do jogo
game_state = 'start'

# Configurações do jogo
falling_keys = []
key_speed = 1
score = 0
lives = 5

# Ranking dos melhores jogadores
ranking = []

# Tempo inicial
start_time = None

# Nome do jogador
player_name = ''
max_name_length = 10

# Função para desenhar a tela inicial
def draw_start_screen():
    screen.fill(WHITE)
    screen.blit(hand_image, hand_image_rect)
    start_text = font.render('Pressione qualquer tecla para começar', True, BLACK)
    start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(start_text, start_text_rect)

# Função para desenhar a tela do jogo
def draw_game_screen():
    screen.fill(WHITE)
    for key in falling_keys:
        key_text = font.render(key['char'], True, BLACK)
        screen.blit(key_text, (key['x'], key['y']))

    score_text = small_font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    lives_text = small_font.render(f'Lives: {lives}', True, RED)
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

# Função para desenhar a tela de Game Over
def draw_game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render('Game Over', True, BLACK)
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_text_rect)
    
    ranking_text = small_font.render('Ranking:', True, BLACK)
    screen.blit(ranking_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

    medals = ['Ouro', 'Prata', 'Bronze']
    for i, (score, name) in enumerate(ranking[:3]):
        ranking_entry_text = small_font.render(f'{medals[i]}: {name} - {score}', True, BLACK)
        screen.blit(ranking_entry_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30 * (i + 1)))

    restart_text = small_font.render('Pressione qualquer tecla para reiniciar', True, BLACK)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(restart_text, restart_text_rect)

# Função para desenhar a tela de entrada de nome do jogador
def draw_name_input_screen():
    screen.fill(WHITE)
    enter_name_text = font.render('Digite seu nome:', True, BLACK)
    enter_name_text_rect = enter_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(enter_name_text, enter_name_text_rect)

    name_text = font.render(player_name, True, BLACK)
    name_text_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(name_text, name_text_rect)

# Função para atualizar a lógica do jogo
def update_game():
    global lives, score, key_speed, start_time, game_state

    current_time = time.time()
    if current_time - start_time >= 60:
        key_speed += 0.10
        start_time = current_time

    for key in falling_keys:
        key['y'] += key_speed
        if key['y'] > SCREEN_HEIGHT:
            falling_keys.remove(key)
            lives -= 1
            if lives == 0:
                game_state = 'name_input'

    pressed_keys = pygame.key.get_pressed()
    for key in falling_keys:
        if pressed_keys[ord(key['char'])]:
            falling_keys.remove(key)
            score += 1

# Função para resetar o jogo
def reset_game():
    global falling_keys, key_speed, score, lives, start_time, player_name
    falling_keys = []
    key_speed = 1
    score = 0
    lives = 5
    start_time = None
    player_name = ''

# Função principal
def main():
    global game_state, score, lives, start_time, player_name

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_state == 'start':
                    reset_game()
                    game_state = 'playing'
                    start_time = time.time()
                elif game_state == 'playing':
                    char = chr(event.key)
                    for key in falling_keys:
                        if key['char'] == char:
                            falling_keys.remove(key)
                            score += 1
                            break
                elif game_state == 'game_over':
                    game_state = 'start'
                elif game_state == 'name_input':
                    if event.key == pygame.K_RETURN:
                        ranking.append((score, player_name))
                        ranking.sort(reverse=True, key=lambda x: x[0])
                        game_state = 'game_over'
                        player_name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < max_name_length:
                            player_name += event.unicode

        if game_state == 'start':
            draw_start_screen()
        elif game_state == 'playing':
            if random.randint(1, 20) == 1:  # Controla a frequência de novas teclas
                falling_keys.append({
                    'char': chr(random.randint(97, 122)),  # Letras minúsculas
                    'x': random.randint(0, SCREEN_WIDTH - 50),
                    'y': 0
                })
            update_game()
            draw_game_screen()
        elif game_state == 'name_input':
            draw_name_input_screen()
        elif game_state == 'game_over':
            draw_game_over_screen()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
