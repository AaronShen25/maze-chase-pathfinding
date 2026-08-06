import pygame


WIDTH = 800
HEIGHT = 600
FPS = 60


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Chase Pathfinding")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (WIDTH // 2, HEIGHT // 2),
            20,
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()