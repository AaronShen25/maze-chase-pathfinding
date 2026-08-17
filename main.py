import pygame


TILE_SIZE = 32
HUD_HEIGHT = 40
FPS = 60

WALL_COLOR = (20, 40, 180)
WALL_OUTLINE_COLOR = (70, 110, 255)
PATH_COLOR = (0, 0, 0)
PELLET_COLOR = (240, 240, 240)
PLAYER_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)


# # = wall
# . = open path with pellet
# P = player starting position
MAZE_LAYOUT = [
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

ROWS = len(MAZE_LAYOUT)
COLUMNS = len(MAZE_LAYOUT[0])

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT


def create_maze() -> list[list[str]]:
    """Create a mutable copy of the maze."""
    return [list(row) for row in MAZE_LAYOUT]


def validate_maze() -> None:
    """Check that every maze row has the same length."""
    for row_index, row in enumerate(MAZE_LAYOUT):
        if len(row) != COLUMNS:
            raise ValueError(
                f"Row {row_index} has {len(row)} columns; "
                f"expected {COLUMNS}."
            )


def find_player_start(maze: list[list[str]]) -> tuple[int, int]:
    """Find the player starting position."""
    for row_index, row in enumerate(maze):
        for column_index, tile in enumerate(row):
            if tile == "P":
                # The P only marks the starting position.
                # After finding it, this becomes an empty path.
                maze[row_index][column_index] = " "
                return row_index, column_index

    raise ValueError("The maze does not contain a player start tile.")


def is_walkable(
    maze: list[list[str]],
    row: int,
    column: int,
) -> bool:
    """Return whether a tile can be entered."""
    if row < 0 or row >= ROWS:
        return False

    if column < 0 or column >= COLUMNS:
        return False

    return maze[row][column] != "#"


def move_player(
    maze: list[list[str]],
    player_row: int,
    player_column: int,
    row_change: int,
    column_change: int,
) -> tuple[int, int]:
    """Move the player if the destination is walkable."""
    new_row = player_row + row_change
    new_column = player_column + column_change

    if is_walkable(maze, new_row, new_column):
        return new_row, new_column

    return player_row, player_column


def collect_pellet(
    maze: list[list[str]],
    row: int,
    column: int,
) -> bool:
    """
    Remove a pellet from the player's current tile.

    Returns True if a pellet was collected.
    """
    if maze[row][column] == ".":
        maze[row][column] = " "
        return True

    return False


def draw_maze(
    screen: pygame.Surface,
    maze: list[list[str]],
) -> None:
    """Draw the maze and remaining pellets."""
    for row_index, row in enumerate(maze):
        for column_index, tile in enumerate(row):
            x = column_index * TILE_SIZE
            y = row_index * TILE_SIZE + HUD_HEIGHT

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
    center_y = (
        row * TILE_SIZE
        + TILE_SIZE // 2
        + HUD_HEIGHT
    )

    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        (center_x, center_y),
        TILE_SIZE // 3,
    )


def draw_score(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score: int,
) -> None:
    """Draw the current score."""
    text = font.render(
        f"Score: {score}",
        True,
        TEXT_COLOR,
    )

    screen.blit(text, (10, 8))


def main() -> None:
    validate_maze()

    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Maze Chase Pathfinding")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    maze = create_maze()

    player_row, player_column = find_player_start(maze)

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                old_row = player_row
                old_column = player_column

                if event.key in (pygame.K_UP, pygame.K_w):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        -1,
                        0,
                    )

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        1,
                        0,
                    )

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        0,
                        -1,
                    )

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        0,
                        1,
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False

                # Only check for a pellet if the player actually moved.
                if (
                    player_row != old_row
                    or player_column != old_column
                ):
                    if collect_pellet(
                        maze,
                        player_row,
                        player_column,
                    ):
                        score += 10

        screen.fill(PATH_COLOR)

        draw_maze(screen, maze)
        draw_player(
            screen,
            player_row,
            player_column,
        )
        draw_score(screen, font, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()