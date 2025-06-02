import tkinter as tk
import random

# Hangman stages
hangman_stages = [
    """
     ------
     |    |
     |    
     |   
     |
    ---
    """,
    """
     ------
     |    O
     |    
     |   
     |
    ---
    """,
    """
     ------
     |    O
     |    |
     |    
     |
    ---
    """,
    """
     ------
     |    O
     |   /|
     |    
     |
    ---
    """,
    """
     ------
     |    O
     |   /|\\
     |    
     |
    ---
    """,
    """
     ------
     |    O
     |   /|\\
     |   /
     |
    ---
    """,
    """
     ------
     |    O
     |   /|\\
     |   / \\
     |
    ---
    """
]

# Function to check if a number is valid in the current board
def valid(board, row, col, num):
#loops through all the rows and columns and checks if the number is present or not
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
#check the 3x3 subgrid for the number
    gridrow, gridcol = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[gridrow + i][gridcol + j] == num:
                return False
    return True

# Function to solve the board (used for validation and hints)
def solve(board):
#if a cell is 0 this will fill it with 1-9
#base case: if no cells are empty board is complete
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
    #checks if it doesnot conflict with the rules
                    if valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):#function calls itself
                            return True
                        board[i][j] = 0 #if function returns false and number doesnt lead to a solution number is removed.
                return False
    return True

# Function to generate a Sudoku puzzle
def generate_puzzle():
    board = [[0] * 9 for _ in range(9)] # 
    for _ in range(20):  # Randomly fill 20 cells
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        while not valid(board, row, col, num) or board[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num

    # Solve the board to generate a solution
    solution = [row[:] for row in board]
    solve(solution)

    return board, solution

# GUI display
def display_game():
    root = tk.Tk()
    root.title("Sudoku with Hangman and Hints")

    # Initialize the game
    puzzle, solution = generate_puzzle()
    board = [row[:] for row in puzzle] #Shallow copy of solved board
    hints_left = tk.IntVar(value=3)
    mistakes = tk.IntVar(value=0)

    # Hangman display
    hangman_label = tk.Label(root, text=hangman_stages[0], font=("Courier", 12), justify="left")
    hangman_label.grid(row=0, column=9, rowspan=9, padx=10)

    # Sudoku board
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            # Determine border thickness
            top = 2 if i % 3 == 0 else 1
            left = 2 if j % 3 == 0 else 1
            right = 2 if j == 8 else 1
            bottom = 2 if i == 8 else 1

            frame = tk.Frame(
                root,
                width=40,
                height=40,
                highlightbackground="black",
                highlightthickness=0,
                bd=0
            )
            frame.grid(row=i, column=j, padx=(left, right), pady=(top, bottom))

            if puzzle[i][j] != 0:
                label = tk.Label(frame, text=puzzle[i][j], font=("Arial", 18), bg="lightgray", width=2, height=1)
                label.pack(expand=True, fill=tk.BOTH)
                row_entries.append(None)
            else:
                entry = tk.Entry(frame, font=("Arial", 18), justify="center", width=2)
                entry.pack(expand=True, fill=tk.BOTH)

                def on_input(event, row=i, col=j, entry=entry):
                    value = entry.get()
                    if value:
                        try:
                            value = int(value)
                            if value != solution[row][col]:
                                mistakes.set(mistakes.get() + 1)
                                entry.delete(0, tk.END)
                                hangman_label.config(text=hangman_stages[min(mistakes.get(), len(hangman_stages) - 1)])
                                if mistakes.get() == len(hangman_stages) - 1:
                                    end_game("Game Over! The Hangman is complete.")
                            else:
                                board[row][col] = value
                                entry.config(state="disabled", disabledbackground="lightgreen")
                        except ValueError:
                            entry.delete(0, tk.END)

                entry.bind("<Return>", on_input)
                row_entries.append(entry)
        entries.append(row_entries)

    # Provide a hint
    def provide_hint():
        if hints_left.get() > 0:
            empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
            if empty_cells:
                row, col = random.choice(empty_cells)
                board[row][col] = solution[row][col]
                entries[row][col].insert(0, solution[row][col])
                entries[row][col].config(state="disabled", disabledbackground="lightblue")
                hints_left.set(hints_left.get() - 1)
                hint_button.config(text=f"Hints: {hints_left.get()}")
            if hints_left.get() == 0:
                hint_button.config(state="disabled")

    # End the game
    def end_game(message):
        for i in range(9):
            for j in range(9):
                if entries[i][j]:
                    entries[i][j].config(state="disabled")
        tk.Label(root, text=message, font=("Arial", 16), fg="red").grid(row=10, column=0, columnspan=9, pady=10)

    # Hint button
    hint_button = tk.Button(root, text=f"Hints: {hints_left.get()}", command=provide_hint)
    hint_button.grid(row=10, column=5, pady=10)

    root.mainloop()

# Start the game
display_game()
