import pygame
import random

# Pygame
pygame.init()

# Constants
GRID_SIZE = 5
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
SCOREBOARD_HEIGHT = 100
WIN_LENGTH = 5


# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# Create the game window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + SCOREBOARD_HEIGHT))
pygame.display.set_caption("Longest Line Game")

# Game variables
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_over = False
winning_line = []
winner = None

# Fonts
font = pygame.font.Font(None, 25)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE
            if grid[y][x] == 1:
                color = RED
            elif grid[y][x] == 2:
                color = BLUE
            elif (x, y) in winning_line:
                color = GREEN
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_scoreboard(player_score, ai_score):
    scoreboard_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, BLACK, scoreboard_rect)

    player_score_text = font.render(f"Player: {player_score-1}", True, RED)
    ai_score_text = font.render(f"AI: {ai_score-1}", True, BLUE)
    reset_text = font.render("Reset", True, WHITE)

    screen.blit(player_score_text, (10, WINDOW_SIZE + 10))
    screen.blit(ai_score_text, (WINDOW_SIZE - 10 - ai_score_text.get_width(), WINDOW_SIZE + 10))
    screen.blit(reset_text, (WINDOW_SIZE // 2 - reset_text.get_width() // 2, WINDOW_SIZE + 10))

def draw_win_screen():
    win_text = font.render(f"{winner} wins!", True, WHITE)
    win_rect = pygame.Rect(WINDOW_SIZE // 2 - win_text.get_width() // 2, WINDOW_SIZE // 2 - win_text.get_height() // 2, win_text.get_width(), win_text.get_height())
    pygame.draw.rect(screen, BLACK, win_rect)
    screen.blit(win_text, (WINDOW_SIZE // 2 - win_text.get_width() // 2, WINDOW_SIZE // 2 - win_text.get_height() // 2))

def reset_game():
    global grid, game_over, winning_line, winner
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    winning_line = []
    winner = None


def count_longest_line(player, x, y):
    longest_line = 0
    winning_line_candidate = []
    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        line_length = 1
        line = [(x, y)]
        nx, ny = x + dx, y + dy
        while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == player:
            line_length += 1
            line.append((nx, ny))
            nx += dx
            ny += dy
        if line_length > longest_line:
            longest_line = line_length
            winning_line_candidate = line
    return longest_line, winning_line_candidate


def ai_move():
    best_move = None
    best_score = -1

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                grid[y][x] = 2
                ai_score, _ = count_longest_line(2, x, y)
                grid[y][x] = 1
                player_score, _ = count_longest_line(1, x, y)
                grid[y][x] = 0

                score = ai_score * 2 - player_score
                if score > best_score:
                    best_score = score
                    best_move = (x, y)

    if best_move:
        x, y = best_move
        grid[y][x] = 2

def check_win(player):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == player:
                
                line_length, line = count_longest_line(player, x, y)
                if line_length >= WIN_LENGTH:
                
            
                    return True, line
    return False, []

def main():
    global game_over, winning_line, winner
    running = True
    while running:
        player_score, _ = max((count_longest_line(1, x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE)), key=lambda x: x[0])
        ai_score, _ = max((count_longest_line(2, x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE)), key=lambda x: x[0])

        screen.fill(WHITE)
        draw_grid()
        draw_scoreboard(player_score, ai_score)

        if game_over:
            draw_win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

                if y < WINDOW_SIZE and grid[grid_y][grid_x] == 0:
                    grid[grid_y][grid_x] = 1
                    game_over, winning_line = check_win(1)
                    if game_over:
                        winner = "Player"
                    else:
                        ai_move()
                        game_over, winning_line = check_win(2)
                        if game_over:
                            winner = "AI"

                if y >= WINDOW_SIZE and y <= WINDOW_SIZE + SCOREBOARD_HEIGHT:
                    reset_game()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
