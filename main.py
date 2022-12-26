import pygame as pygame

from DropDown import DropDown
# from DropDown import DropDown, COLOR_INACTIVE
from utils import *

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Pyaint")
STATE = "COLOR"
Change = False
degrees = 0
sel = 0

TEXT = list();
TPOS = list();
TCOLOR = list();


def init_grid(rows, columns, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(columns):  # use _ when variable is not required
            grid[i].append(color)
    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH - PADDING, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5, HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "FillBucket":
                text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Brush":
                text_surface = pos_font.render("Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Text":
                text_surface = pos_font.render("Text", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break

            if button.name == "Change":
                text_surface = pos_font.render("Swap Toolbar", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            r, g, b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)

            win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))

        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    draw_brush_widths(win)
    draw_mouse_position_text(win)
    pygame.display.update()


def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),
        Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse"),
        Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, None, "ellipse")
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (BRUSH_SIZE == 2 and button.width == size_medium) or (
                BRUSH_SIZE == 3 and button.width == size_large)):
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height),
                            border_width)  # border


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= ROWS:
        raise IndexError
    return row, col


def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        grid[row][col] = drawing_color
    else:  # for values greater than 1
        r = row - BRUSH_SIZE + 1
        c = col - BRUSH_SIZE + 1

        for i in range(BRUSH_SIZE * 2 - 1):
            for j in range(BRUSH_SIZE * 2 - 1):
                if r + i < 0 or c + j < 0 or r + i >= ROWS or c + j >= COLS:
                    continue
                grid[r + i][c + j] = drawing_color


def paint_using_text(row, col, t_fontname, t_size):
    grid[row][col] = drawing_color
    FONT = pygame.font.SysFont(t_fontname, t_size)

    return


# Checks whether the coordinated are within the canvas
def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1


def fill_bucket(row, col, color):
    # Visiting array
    vis = [[0 for i in range(101)] for j in range(101)]

    # Creating queue for bfs
    obj = []

    # Pushing pair of {x, y}
    obj.append([row, col])

    # Marking {x, y} as visited
    vis[row][col] = 1

    # Until queue is empty
    while len(obj) > 0:

        # Extracting front pair
        coord = obj[0]
        x = coord[0]
        y = coord[1]
        preColor = grid[x][y]

        grid[x][y] = color

        # Popping front pair of queue
        obj.pop(0)

        # For Upside Pixel or Cell
        if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
            obj.append([x + 1, y])
            vis[x + 1][y] = 1

        # For Downside Pixel or Cell
        if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
            obj.append([x - 1, y])
            vis[x - 1][y] = 1

        # For Right side Pixel or Cell
        if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
            obj.append([x, y + 1])
            vis[x][y + 1] = 1

        # For Left side Pixel or Cell
        if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
            obj.append([x, y - 1])
            vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_width = 40
button_height = 40
button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT / 2 + 1
button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH / 2
brush_widths = [
    Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, "ellipse"),
    Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, "ellipse"),
    Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, "ellipse")
]

button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT / 2 + 1
button_space = 42

# Adding Buttons
buttons = []

for i in range(int(len(COLORS) / 2)):
    buttons.append(Button(100 + button_space * i, button_y_top_row, button_width, button_height, COLORS[i]))

for i in range(int(len(COLORS) / 2)):
    buttons.append(
        Button(100 + button_space * i, button_y_bot_row, button_width, button_height, COLORS[i + int(len(COLORS) / 2)]))

# Right toolbar buttonst
# need to add change toolbar button.
for i in range(10):
    if i == 0:
        buttons.append(Button(WIDTH + 20, (i * button_height) + 5, button_width, button_height, WHITE,
                              name="Change"))  # Change toolbar buttons
    else:
        buttons.append(Button(WIDTH + 20, (i * button_height) + 5, button_width, button_height, WHITE, "B" + str(i - 1),
                              BLACK))  # append tools

buttons.append(Button(WIDTH - PADDING - button_space, button_y_top_row, button_width, button_height, WHITE, "Erase",
                      BLACK))  # Erase Button
buttons.append(Button(WIDTH - PADDING - button_space, button_y_bot_row, button_width, button_height, WHITE, "Clear",
                      BLACK))  # Clear Button
buttons.append(Button(WIDTH - PADDING + 10, 16, button_width - 5, button_height - 5, name="FillBucket",
                      image_url="assets/paint-bucket.png"))  # FillBucket
buttons.append(Button(WIDTH - PADDING + 50, 16, button_width - 5, button_height - 5, name="Brush",
                      image_url="assets/paint-brush.png"))  # Brush
buttons.append(Button(WIDTH - PADDING + 10, + 69, button_width - 5, button_height - 5, name="Text",
                      image_url="assets/paint-text.png"))  # Text
buttons.append(Button(WIDTH - PADDING + 80, + 129, 24, 24, name="Cycle Font", image_url="assets/Cycle.png"))  # Text
buttons.append(Button(WIDTH - PADDING + 80, + 156, 24, 24, name="Font Size", image_url="assets/Plus.png"))  # Text

draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

FONTPOOL = ["Arial", "Times", "Calibri"];
FONT_SIZES = [8, 16, 24, 32, 40, 48, 56, 64, 72]
sel = 0
sel_f = 0
size_w = 0;
size_h = 0;
while run:
    clock.tick(FPS)  # limiting FPS to 60 or any other value

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # if user closed the program
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)

                if STATE == "COLOR":
                    paint_using_brush(row, col, BRUSH_SIZE)

                elif STATE == "TEXT":
                    # Define the font to use for the text
                    font = pygame.font.Font(FONTPOOL[sel] + ".ttf", FONT_SIZES[sel_f])

                    # Set the initial text to an empty string
                    text = ""
                    sx, sy = 200, 200
                    # Run the game loop
                    running = True

                    flipv = False;
                    fliph = False;

                    while running:
                        # Handle events
                        for event in pygame.event.get():

                            # if user types QUIT then the screen will close
                            if event.type == pygame.QUIT:
                                pygame.quit()

                            if pygame.mouse.get_pressed()[0]:
                                sx, sy = pygame.mouse.get_pos()
                                getPOS = False
                                WIN.fill((255, 255, 255))
                                draw(WIN, grid, buttons)

                            if event.type == pygame.KEYDOWN:

                                if event.key == pygame.K_TAB:
                                    degrees = degrees + 30
                                    WIN.fill((255, 255, 255))
                                    draw(WIN, grid, buttons)
                                    break

                                if event.key == pygame.K_F1:
                                    if fliph:
                                        fliph = False
                                    else:
                                        fliph = True

                                if event.key == pygame.K_F2:
                                    if flipv:
                                        flipv = False
                                    else:
                                        flipv = True

                                if event.key == pygame.K_UP:
                                    size_h = size_h + 5;

                                if event.key == pygame.K_DOWN:
                                    size_h = size_h - 5;

                                if event.key == pygame.K_LEFT:
                                    size_w = size_w - 5;

                                if event.key == pygame.K_RIGHT:
                                    size_w = size_w + 5;

                                # Exit using ESCAPE
                                if event.key == pygame.K_ESCAPE:
                                    running = False
                                    STATE = "COLOR"
                                    break

                                # Check for backspace
                                if event.key == pygame.K_BACKSPACE:
                                    WIN.fill((255, 255, 255))
                                    draw(WIN, grid, buttons)
                                    # get text input from 0 to -1 i.e. end.
                                    text = text[:-1]


                                # Unicode standard is used for string
                                # formation
                                else:
                                    WIN.fill((255, 255, 255))
                                    draw(WIN, grid, buttons)
                                    text += event.unicode

                        # Clear the screen
                        # screen.fill((0, 0, 0))

                        # Create the text surface
                        text_surface = font.render(text, True, drawing_color)
                        text_surface = pygame.transform.rotate(text_surface, degrees)
                        if flipv:
                            text_surface = pygame.transform.flip(text_surface, False, True);
                        if fliph:
                            text_surface = pygame.transform.flip(text_surface, True, False);
                        # Draw the text to the screen

                        if text != "" and text_surface.get_width() + size_w > 0 and text_surface.get_height() + size_h > 0:
                            text_surface = pygame.transform.smoothscale(text_surface, (
                            text_surface.get_width() + size_w, text_surface.get_height() + size_h))
                            WIN.blit(text_surface, (sx, sy))
                        else:
                            text_surface = font.render(text, True, drawing_color)
                        

                        # Update the display
                        pygame.display.flip()

                    TEXT.append(text_surface)
                    TPOS.append((sx, sy))
                    STATE = "COLOR"
                    break

                elif STATE == "FILL":
                    fill_bucket(row, col, drawing_color)

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        TPOS = list();
                        TEXT = list();
                        STATE = "COLOR"
                        break

                    if button.name == "Cycle Font":
                        sel = sel + 1;
                        if sel > 2:
                            sel = 0
                        break;

                    if button.name == "Font Size":
                        sel_f = sel_f + 1;
                        if sel_f > 8:
                            sel_f = 0
                        break;

                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    if button.name == "Text":
                        STATE = "TEXT"
                        break

                    if button.name == "Change":
                        Change = not Change
                        for i in range(10):
                            if i == 0:
                                buttons.append(
                                    Button(WIDTH + 20, (i * button_height) + 5, button_width, button_height, WHITE,
                                           name="Change"))
                            else:
                                if Change == False:
                                    buttons.append(
                                        Button(WIDTH + 20, (i * button_height) + 5, button_width, button_height, WHITE,
                                               "B" + str(i - 1), BLACK))
                                if Change == True:
                                    buttons.append(
                                        Button(WIDTH + 20, (i * button_height) + 5, button_width, button_height, WHITE,
                                               "C" + str(i - 1), BLACK))
                        break

                    if button.name == "Brush":
                        STATE = "COLOR"
                        break

                    drawing_color = button.color
                    draw_button.color = drawing_color

                    break

                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    # set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"

    draw(WIN, grid, buttons)

    font = pygame.font.Font(None, 24);

    CURR_FONT = font.render(FONTPOOL[sel], True, drawing_color)
    WIN.blit(CURR_FONT, (613, 136));
    CURR_FONT_SIZE = font.render(FONT_SIZES[sel_f].__str__(), True, drawing_color)
    WIN.blit(CURR_FONT_SIZE, (613, 162));

    for i in range(0, len(TEXT)):
        WIN.blit(TEXT[i], TPOS[i])

    pygame.display.flip()

pygame.quit()