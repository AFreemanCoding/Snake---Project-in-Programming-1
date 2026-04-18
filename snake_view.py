def draw_board(canvas, x1, y1, x2, y2, board, info_mode):
    row_count = len(board)
    col_count = len(board[0])

    cell_width = (x2 - x1) / col_count
    cell_height = (y2 - y1) / row_count

    head_value, tail_value = find_head_and_tail_values(board)

    for row_index in range(row_count):
        for col_index in range(col_count):
            cell_left = x1 + col_index * cell_width
            cell_top = y1 + row_index * cell_height
            cell_right = cell_left + cell_width
            cell_bottom = cell_top + cell_height
            cell_value = board[row_index][col_index]

            draw_cell_background(
                canvas, cell_left, cell_top, cell_right, cell_bottom,
                cell_width, cell_height, row_index, col_index
            )

            if cell_value > 0:
                is_head = cell_value == head_value
                is_tail = cell_value == tail_value
                draw_snake_part(
                    canvas, cell_left, cell_top, cell_width, cell_height,
                    is_head, is_tail
                )
                
            elif cell_value < 0:
                draw_fish(
                    canvas, cell_left, cell_top, cell_right, cell_bottom, cell_width
                )

            if info_mode:
                center_x = (cell_left + cell_right) / 2
                center_y = (cell_top + cell_bottom) / 2
                canvas.create_text(
                    center_x, center_y,
                    text=f"{row_index},{col_index}\n{cell_value}",
                    font='Arial 7',
                    fill='#d8f1ff'
                )


def find_head_and_tail_values(board):
    head_value = 0
    tail_value = None

    for row in board:
        for cell_value in row:
            if cell_value > head_value:
                head_value = cell_value
            if cell_value > 0 and (tail_value is None or cell_value < tail_value):
                tail_value = cell_value

    return head_value, tail_value


# Ekstra funksjoner for grafikk og farger til bakgrunnen, slangen og fisken for å gjøre det om til sjø slange tema

def draw_cell_background(canvas, cell_left, cell_top, cell_right, cell_bottom,
                         cell_width, cell_height, row_index, col_index):
    water_pattern = (row_index * 5 + col_index * 7) % 4

    if water_pattern == 0:
        water_color = '#071a2a'
    elif water_pattern == 1:
        water_color = '#0a2236'
    elif water_pattern == 2:
        water_color = '#0c2740'
    else:
        water_color = '#082033'

    canvas.create_rectangle(
        cell_left, cell_top, cell_right, cell_bottom,
        fill=water_color, outline='#03111d', width=1
    )

    if (row_index + col_index) % 2 == 0:
        canvas.create_arc(
            cell_left + cell_width * 0.10, cell_top + cell_height * 0.18,
            cell_right - cell_width * 0.10, cell_top + cell_height * 0.55,
            start=0, extent=180, style='arc', outline='#163d5c', width=1
        )

    if (row_index * 2 + col_index) % 3 == 0:
        canvas.create_arc(
            cell_left + cell_width * 0.22, cell_top + cell_height * 0.45,
            cell_right - cell_width * 0.22, cell_bottom - cell_height * 0.10,
            start=0, extent=180, style='arc', outline='#114566', width=1
        )

    if (row_index * 3 + col_index) % 5 == 0:
        canvas.create_oval(
            cell_left + cell_width * 0.72, cell_top + cell_height * 0.18,
            cell_left + cell_width * 0.78, cell_top + cell_height * 0.24,
            fill='#9ed8ff', outline=''
        )
        canvas.create_oval(
            cell_left + cell_width * 0.80, cell_top + cell_height * 0.28,
            cell_left + cell_width * 0.84, cell_top + cell_height * 0.32,
            fill='#7fcaff', outline=''
        )


def draw_snake_part(canvas, cell_left, cell_top, cell_width, cell_height, is_head, is_tail):
    if is_head:
        draw_snake_head(canvas, cell_left, cell_top, cell_width, cell_height)
    elif is_tail:
        draw_snake_tail(canvas, cell_left, cell_top, cell_width, cell_height)
    else:
        draw_snake_body(canvas, cell_left, cell_top, cell_width, cell_height)


def draw_snake_head(canvas, cell_left, cell_top, cell_width, cell_height):
    canvas.create_oval(
        cell_left + cell_width * 0.05, cell_top + cell_height * 0.05,
        cell_left + cell_width * 0.95, cell_top + cell_height * 0.95,
        fill='#121722', outline='#000000', width=2
    )

    canvas.create_arc(
        cell_left + cell_width * 0.08, cell_top + cell_height * 0.12,
        cell_left + cell_width * 0.92, cell_top + cell_height * 0.92,
        start=210, extent=180, style='pieslice', fill='#f0c419', outline=''
    )

    canvas.create_arc(
        cell_left + cell_width * 0.12, cell_top + cell_height * 0.08,
        cell_left + cell_width * 0.94, cell_top + cell_height * 0.84,
        start=20, extent=180, style='pieslice', fill='#0b0f18', outline=''
    )

    canvas.create_oval(
        cell_left + cell_width * 0.18, cell_top + cell_height * 0.12,
        cell_left + cell_width * 0.72, cell_top + cell_height * 0.35,
        fill='#1d2636', outline=''
    )

    for eye_x in (0.37, 0.60):
        canvas.create_oval(
            cell_left + cell_width * (eye_x - 0.07), cell_top + cell_height * 0.26,
            cell_left + cell_width * (eye_x + 0.07), cell_top + cell_height * 0.40,
            fill='#ffd84d', outline='#332200'
        )
        canvas.create_line(
            cell_left + cell_width * eye_x, cell_top + cell_height * 0.27,
            cell_left + cell_width * eye_x, cell_top + cell_height * 0.39,
            fill='#1a0a00', width=max(1, int(cell_width * 0.025))
        )

    canvas.create_arc(
        cell_left + cell_width * 0.34, cell_top + cell_height * 0.50,
        cell_left + cell_width * 0.66, cell_top + cell_height * 0.72,
        start=200, extent=140, style='arc', outline='#4a0000', width=2
    )

    canvas.create_line(
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.68,
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.82,
        fill='#e0103a', width=2
    )
    canvas.create_line(
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.82,
        cell_left + cell_width * 0.43, cell_top + cell_height * 0.92,
        fill='#e0103a', width=2
    )
    canvas.create_line(
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.82,
        cell_left + cell_width * 0.57, cell_top + cell_height * 0.92,
        fill='#e0103a', width=2
    )


def draw_snake_tail(canvas, cell_left, cell_top, cell_width, cell_height):
    canvas.create_oval(
        cell_left + cell_width * 0.24, cell_top + cell_height * 0.24,
        cell_left + cell_width * 0.76, cell_top + cell_height * 0.76,
        fill='#f0c419', outline='#000000', width=1
    )

    canvas.create_polygon(
        cell_left + cell_width * 0.26, cell_top + cell_height * 0.30,
        cell_left + cell_width * 0.38, cell_top + cell_height * 0.50,
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.30,
        fill='#0d1117', outline=''
    )
    canvas.create_polygon(
        cell_left + cell_width * 0.38, cell_top + cell_height * 0.70,
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.50,
        cell_left + cell_width * 0.62, cell_top + cell_height * 0.70,
        fill='#0d1117', outline=''
    )
    canvas.create_polygon(
        cell_left + cell_width * 0.50, cell_top + cell_height * 0.30,
        cell_left + cell_width * 0.62, cell_top + cell_height * 0.50,
        cell_left + cell_width * 0.74, cell_top + cell_height * 0.30,
        fill='#0d1117', outline=''
    )


def draw_snake_body(canvas, cell_left, cell_top, cell_width, cell_height):
    canvas.create_oval(
        cell_left + cell_width * 0.14, cell_top + cell_height * 0.14,
        cell_left + cell_width * 0.86, cell_top + cell_height * 0.86,
        fill='#11161f', outline='#000000', width=1
    )

    canvas.create_arc(
        cell_left + cell_width * 0.14, cell_top + cell_height * 0.14,
        cell_left + cell_width * 0.86, cell_top + cell_height * 0.86,
        start=210, extent=180, style='pieslice', fill='#f0c419', outline=''
    )

    canvas.create_arc(
        cell_left + cell_width * 0.22, cell_top + cell_height * 0.30,
        cell_left + cell_width * 0.78, cell_top + cell_height * 0.78,
        start=190, extent=150, style='arc', outline='#d4ac17', width=2
    )


def draw_fish(canvas, cell_left, cell_top, cell_right, cell_bottom, cell_width):
    center_x = (cell_left + cell_right) / 2
    center_y = (cell_top + cell_bottom) / 2
    pixel_size = cell_width * 0.06

    def pixel(relative_left, relative_top, relative_right, relative_bottom, color):
        canvas.create_rectangle(
            center_x + relative_left * pixel_size,
            center_y + relative_top * pixel_size,
            center_x + relative_right * pixel_size,
            center_y + relative_bottom * pixel_size,
            fill=color, outline=''
        )

    pixel(-4, -3, -2, -1, '#3a8abf')
    pixel(-4, 1, -2, 3, '#3a8abf')
    pixel(-3, -3, 4, 3, '#4aa8d8')
    pixel(1, -2, 3, 0, '#6ec4f0')

    pixel(-2, -4, 3, -3, '#1a4a70')
    pixel(-2, 3, 3, 4, '#1a4a70')
    pixel(4, -2, 5, 2, '#1a4a70')
    pixel(-3, -2, -2, 2, '#1a4a70')
    pixel(2, -3, 3, -2, '#1a4a70')
    pixel(-2, -3, -1, -2, '#1a4a70')
    pixel(2, 2, 3, 3, '#1a4a70')
    pixel(-2, 2, -1, 3, '#1a4a70')

    pixel(-2, -5, -1, -4, '#3a8abf')
    pixel(-1, -6, 1, -4, '#3a8abf')
    pixel(1, -5, 2, -4, '#3a8abf')

    pixel(1, -2, 3, 0, '#d0eeff')
    pixel(1.2, -1.8, 2.5, -0.2, '#1a2a3a')
    pixel(1.2, -1.8, 1.9, -1.2, '#ffffff')
    pixel(3.5, 0.5, 4.5, 1.5, '#1a4a70')


if __name__ == '__main__':
    from uib_inf100_graphics.simple import canvas, display

    test_board = [
        [1, 2, 3, 0, 5, 4, -1, -1, 1, 2, 3],
        [0, 4, 0, 7, 0, 3, -1, 0, 0, 4, 0],
        [0, 5, 0, 8, 1, 2, -1, -1, 0, 5, 0],
        [0, 6, 0, 9, 0, 0, 0, -1, 0, 6, 0],
        [0, 7, 0, 10, 11, 12, -1, -1, 0, 7, 0],
    ]

    draw_board(canvas, 25, 80, 375, 320, test_board, True)
    display(canvas)