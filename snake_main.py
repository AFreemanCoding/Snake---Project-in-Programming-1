from snake_view import draw_board
import random
import os
from PIL import Image, ImageTk

def app_started(app):
    app.direction = 'east'
    app.info_mode = True
    app.state = 'start'

    app.difficulty = 2
    app.timer_delay = 160

    app.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    app.snake_size = 3
    app.head_pos = (3, 4)

    app.start_image = None
    app.original_start_image = None
    load_start_image(app)


def timer_fired(app):
    if app.state == 'active' and not app.info_mode:
        move_snake(app)


def key_pressed(app, event):
    if app.state == 'start':
        if event.key == '1':
            app.difficulty = 1
            app.timer_delay = 240
        elif event.key == '2':
            app.difficulty = 2
            app.timer_delay = 160
        elif event.key == '3':
            app.difficulty = 3
            app.timer_delay = 95
        elif event.key == 'Space':
            app.state = 'active'
            app.info_mode = False
        return

    if event.key == 'i':
        app.info_mode = not app.info_mode
        return

    if app.state == 'gameover':
        if event.key == 'r':
            app_started(app)
        return

    if app.state != 'active':
        return

    if event.key == 'Up' and app.direction != 'south':
        app.direction = 'north'
    elif event.key == 'Down' and app.direction != 'north':
        app.direction = 'south'
    elif event.key == 'Left' and app.direction != 'east':
        app.direction = 'west'
    elif event.key == 'Right' and app.direction != 'west':
        app.direction = 'east'


def redraw_all(app, canvas):
    if app.state == 'start':
        draw_start_screen(app, canvas)
        return

    if app.state == 'gameover':
        draw_game_over_screen(app, canvas)
        return

    canvas.create_rectangle(0, 0, app.width, app.height, fill='#04101a', outline='')

    draw_board(
        canvas,
        25,
        35,
        app.width - 25,
        app.height - 25,
        app.board,
        app.info_mode
    )

    draw_top_bar(app, canvas)

    if app.info_mode:
        canvas.create_text(
            15,
            app.height - 15,
            anchor='w',
            text=(
                f"direction: {app.direction}   "
                f"snake_size: {app.snake_size}   "
                f"head_pos: {app.head_pos}   "
                f"state: {app.state}"
            ),
            fill='white',
            font='Arial 10 bold'
        )


def load_start_image(app):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_folder, 'start_screen.png')

    try:
        app.original_start_image = Image.open(image_path)
        update_start_image(app)
    except:
        app.original_start_image = None
        app.start_image = None


def update_start_image(app):
    if app.original_start_image is None:
        return

    resized_image = app.original_start_image.copy()
    resized_image = resized_image.resize((app.width, app.height), Image.LANCZOS)
    app.start_image = ImageTk.PhotoImage(resized_image)


def size_changed(app):
    update_start_image(app)


def draw_start_screen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black', outline='')

    if app.start_image is not None:
        canvas.create_image(app.width / 2, app.height / 2, image=app.start_image)
    else:
        canvas.create_text(
            app.width / 2,
            app.height / 2,
            text='Missing start_screen.png',
            fill='white',
            font='Arial 20 bold'
        )



def move_snake(app):
    next_head_position = get_next_head_position(app)

    if not is_legal_move(next_head_position, app.board):
        app.state = 'gameover'
        return

    next_row, next_col = next_head_position

    # I denne versjonen bruker vi fisk i stedet for epler,

    if app.board[next_row][next_col] == -1:
        app.snake_size += 1
        add_apple_at_random_location(app.board)
    else:
        subtract_one_from_all_positives(app.board)

    app.head_pos = next_head_position
    app.board[next_row][next_col] = app.snake_size


def get_next_head_position(app):
    head_row, head_col = app.head_pos

    if app.direction == 'north':
        head_row -= 1
    elif app.direction == 'south':
        head_row += 1
    elif app.direction == 'west':
        head_col -= 1
    elif app.direction == 'east':
        head_col += 1

    return (head_row, head_col)


def subtract_one_from_all_positives(board):
    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            if board[row_index][col_index] > 0:
                board[row_index][col_index] -= 1


def add_apple_at_random_location(board):

    # I spillet er -1 en fisk ikke et eple, men for testens skyld beholder vi funkjsonkallet

    empty_cells = []

    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            if board[row_index][col_index] == 0:
                empty_cells.append((row_index, col_index))

    if empty_cells:
        random_row, random_col = random.choice(empty_cells)
        board[random_row][random_col] = -1


def is_legal_move(position, board):
    row, col = position

    if row < 0 or row >= len(board):
        return False
    if col < 0 or col >= len(board[0]):
        return False
    if board[row][col] > 0:
        return False

    return True


# Ekstra funksjoner for å gjøre spillet mer komplett, og slik at det passer sjø slange tema

def draw_top_bar(app, canvas):
    canvas.create_rectangle(0, 0, app.width, 26, fill='#081a28', outline='')

    fish_eaten = app.snake_size - 3
    difficulty_text = {1: 'Easy', 2: 'Medium', 3: 'Hard'}.get(app.difficulty, 'Medium')

    canvas.create_text(
        15,
        13,
        text=f"Difficulty: {difficulty_text}",
        anchor='w',
        fill='#d8f1ff',
        font='Arial 11 bold'
    )

    canvas.create_text(
        app.width - 55,
        11,
        text='🐟',
        fill='white',
        font='Arial 14'
    )

    canvas.create_text(
        app.width - 38,
        14,
        text=str(fish_eaten),
        fill='#ffd84d',
        font='Arial 12 bold'
    )


def draw_game_over_screen(app, canvas):
    center_x = app.width / 2
    center_y = app.height / 2

    canvas.create_rectangle(0, 0, app.width, app.height, fill="#081629", outline='')

    snake_x = app.width * 0.25
    snake_y = app.height * 0.6

    canvas.create_oval(
        snake_x - 55, snake_y - 30, snake_x + 55, snake_y + 30,
        fill='',
        outline='#0d1117',
        width=10
    )
    canvas.create_arc(
        snake_x - 55, snake_y - 30, snake_x + 55, snake_y + 30,
        start=20,
        extent=200,
        style='arc',
        outline='#f0c419',
        width=4
    )

    canvas.create_oval(
        snake_x - 30, snake_y - 18, snake_x + 30, snake_y + 18,
        fill='',
        outline='#0d1117',
        width=8
    )
    canvas.create_arc(
        snake_x - 30, snake_y - 18, snake_x + 30, snake_y + 18,
        start=40,
        extent=200,
        style='arc',
        outline='#f0c419',
        width=3
    )

    head_x = snake_x + 58
    head_y = snake_y - 10

    canvas.create_oval(
        head_x - 22, head_y - 16, head_x + 22, head_y + 16,
        fill='#0d1117',
        outline='#000000',
        width=2
    )
    canvas.create_arc(
        head_x - 20, head_y, head_x + 20, head_y + 18,
        start=200,
        extent=180,
        style='pieslice',
        fill='#f0c419',
        outline=''
    )
    canvas.create_arc(
        head_x - 16, head_y - 14, head_x + 18, head_y + 4,
        start=20,
        extent=180,
        style='pieslice',
        fill='#0a0e16',
        outline=''
    )

    for eye_x in [head_x - 8, head_x + 8]:
        canvas.create_line(eye_x - 4, head_y - 8, eye_x + 4, head_y, fill='#cc0000', width=2)
        canvas.create_line(eye_x + 4, head_y - 8, eye_x - 4, head_y, fill='#cc0000', width=2)

    canvas.create_line(head_x + 20, head_y + 4, head_x + 32, head_y + 12, fill='#cc103a', width=2)
    canvas.create_line(head_x + 32, head_y + 12, head_x + 28, head_y + 20, fill='#cc103a', width=2)
    canvas.create_line(head_x + 32, head_y + 12, head_x + 36, head_y + 20, fill='#cc103a', width=2)

    canvas.create_text(
        center_x + 3,
        center_y - 17,
        text='GAME OVER',
        fill='#3a0000',
        font='Georgia 48 bold'
    )
    canvas.create_text(
        center_x,
        center_y - 20,
        text='GAME OVER',
        fill='#cc0000',
        font='Georgia 48 bold'
    )
    canvas.create_text(
        center_x,
        center_y + 22,
        text=f'Fish eaten: {app.snake_size - 3}',
        fill='#d8f1ff',
        font='Georgia 16'
    )
    canvas.create_text(
        center_x,
        center_y + 52,
        text='Press R to restart',
        fill='#992222',
        font='Georgia 13'
    )


if __name__ == '__main__':
    from uib_inf100_graphics.event_app import run_app
    run_app(width=750, height=600, title='Snake')