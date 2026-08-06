import pygame


TILE_SIZE = 32
FPS = 60

WALL_COLOR = (20, 40, 180)
WALL_OUTLINE_COLOR = (70, 110, 255)
PATH_COLOR = (0, 0, 0)
PELLET_COLOR = (240, 240, 240)
PLAYER_COLOR = (255, 255, 0)


# # = wall
# . = open path with pellet
# P = player starting position
MAZE = [
    "#####################",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#.#...............#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.#.#.#.#.#.#####",
    "#.....#.#...#.#.....#",
    "#.#####.##.##.#####.#",
    "#.........P.........#",
    "#.#####.##.##.#####.#",
    "#.....#.#...#.#.....#",
    "#####.#.#.#.#.#.#####",
    "#.....#...#...#.....#",
    "#.#.###.#####.###.#.#",
    "#.#...............#.#",
    "#.###.###.#.###.###.#",
    "#.........#.........#",
    "#####################",
]

ROWS = len(MAZE)
COLUMNS = len(MAZE[0])

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE


def validate_maze() -> None:
    """Check that every maze row has the same length."""
    for row_index, row in enumerate(MAZE):
        if len(row) != COLUMNS:
            raise ValueError(
                f"Row {row_index} has {len(row)} columns; "
                f"expected {COLUMNS}."
            )


def find_player_start() -> tuple[int, int]:
    """Find and return the player's starting row and column."""
    for row_index, row in enumerate(MAZE):
        for column_index, tile in enumerate(row):
            if tile == "P":
                return row_index, column_index

    raise ValueError("The maze does not contain a player start tile.")


def is_walkable(row: int, column: int) -> bool:
    """Return whether the player can enter the given tile."""
    if row < 0 or row >= ROWS:
        return False

    if column < 0 or column >= COLUMNS:
        return False

    return MAZE[row][column] != "#"


def move_player(
    player_row: int,
    player_column: int,
    row_change: int,
    column_change: int,
) -> tuple[int, int]:
    """Move the player if the destination is not a wall."""
    new_row = player_row + row_change
    new_column = player_column + column_change

    if is_walkable(new_row, new_column):
        return new_row, new_column

    return player_row, player_column


def draw_maze(screen: pygame.Surface) -> None:
    """Draw each tile in the maze."""
    for row_index, row in enumerate(MAZE):
        for column_index, tile in enumerate(row):
            x = column_index * TILE_SIZE
            y = row_index * TILE_SIZE

            tile_rect = pygame.Rect(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE,
            )

            if tile == "#":
                pygame.draw.rect(
                    screen,
                    WALL_COLOR,
                    tile_rect,
                )

                pygame.draw.rect(
                    screen,
                    WALL_OUTLINE_COLOR,
                    tile_rect,
                    width=2,
                )
            else:
                pygame.draw.rect(
                    screen,
                    PATH_COLOR,
                    tile_rect,
                )

                if tile == ".":
                    pygame.draw.circle(
                        screen,
                        PELLET_COLOR,
                        tile_rect.center,
                        3,
                    )


def draw_player(
    screen: pygame.Surface,
    row: int,
    column: int,
) -> None:
    """Draw the player in the centre of its tile."""
    center_x = column * TILE_SIZE + TILE_SIZE // 2
    center_y = row * TILE_SIZE + TILE_SIZE // 2

    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        (center_x, center_y),
        TILE_SIZE // 3,
    )


def main() -> None:
    validate_maze()
    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Maze Chase Pathfinding")

    clock = pygame.time.Clock()
    player_row, player_column = find_player_start()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    player_row, player_column = move_player(
                        player_row,
                        player_column,
                        -1,
                        0,
                    )

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player_row, player_column = move_player(
                        player_row,
                        player_column,
                        1,
                        0,
                    )

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player_row, player_column = move_player(
                        player_row,
                        player_column,
                        0,
                        -1,
                    )

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player_row, player_column = move_player(
                        player_row,
                        player_column,
                        0,
                        1,
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(PATH_COLOR)

        draw_maze(screen)
        draw_player(screen, player_row, player_column)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()