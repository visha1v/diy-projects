import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_FALL_SPEED = 5
PADDLE_SPEED = 7

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Ball")

font = pygame.font.SysFont(None, 35)

def draw_paddle(paddle_rect):
    pygame.draw.rect(screen, BLUE, paddle_rect)

def draw_ball(ball_rect):
    pygame.draw.ellipse(screen, RED, ball_rect)

def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def main():
    # Game variables
    paddle_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BALL_SIZE), 0, BALL_SIZE, BALL_SIZE)
    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle_rect.x += PADDLE_SPEED

        if paddle_rect.left < 0:
            paddle_rect.left = 0
        if paddle_rect.right > SCREEN_WIDTH:
            paddle_rect.right = SCREEN_WIDTH

        ball_rect.y += BALL_FALL_SPEED

        if ball_rect.top > SCREEN_HEIGHT:
            ball_rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
            ball_rect.y = 0

        if ball_rect.colliderect(paddle_rect):
            score += 1
            ball_rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
            ball_rect.y = 0

        screen.fill((0, 0, 0))

        draw_paddle(paddle_rect)
        draw_ball(ball_rect)

        display_score(score)

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
