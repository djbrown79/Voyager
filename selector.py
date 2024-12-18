import os
import shutil

def select_option(options, prompt="Select an option:"):
    """Display options in a grid layout using arrow keys for selection."""
    if not options:
        return None

    # Get terminal width
    term_width = shutil.get_terminal_size().columns
    
    # Calculate layout
    max_option_length = max(len(str(opt)) for opt in options) + 4  # Add padding
    num_cols = max(1, term_width // max_option_length)
    num_rows = (len(options) + num_cols - 1) // num_cols

    # Create 2D grid of options
    grid = []
    for row in range(num_rows):
        grid_row = []
        for col in range(num_cols):
            idx = col * num_rows + row
            if idx < len(options):
                grid_row.append(options[idx])
            else:
                grid_row.append("")
        grid.append(grid_row)

    # ANSI codes
    HIGHLIGHT = '\033[7m'
    NORMAL = '\033[0m'
    CLEAR_LINE = '\033[2K'
    UP = '\033[1A'
    
    # Print menu
    print(prompt)
    for row in grid:
        line = ""
        for opt in row:
            if opt:
                line += f"  {opt:<{max_option_length}}"
        print(line.rstrip())
    
    # Move cursor up
    print(UP * len(grid), end='\r')
    
    current_row = 0
    current_col = 0
    while True:
        # Display grid with current selection highlighted
        for row_idx, row in enumerate(grid):
            line = ""
            for col_idx, opt in enumerate(row):
                if opt:
                    if row_idx == current_row and col_idx == current_col:
                        # Ensure the option text is padded correctly without subtracting ANSI codes
                        highlighted_opt = f"{HIGHLIGHT}{opt:<{max_option_length}}{NORMAL}"
                        line += f"  {highlighted_opt}"
                    else:
                        line += f"  {opt:<{max_option_length}}"
            print(f"\r{CLEAR_LINE}{line.rstrip()}")
        
        # Move cursor back up
        print(UP * len(grid), end='\r')
        
        # Handle input
        import msvcrt
        while True:
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                if key == 224:  # Special key prefix
                    key = ord(msvcrt.getch())
                    if key == 72 and current_row > 0:  # Up
                        current_row -= 1
                        break
                    elif key == 80 and current_row < num_rows - 1:  # Down
                        if current_col * num_rows + current_row + 1 < len(options):
                            current_row += 1
                            break
                    elif key == 75 and current_col > 0:  # Left
                        current_col -= 1
                        break
                    elif key == 77 and current_col < num_cols - 1:  # Right
                        if (current_col + 1) * num_rows + current_row < len(options):
                            current_col += 1
                            break
                elif key == 13:  # Enter
                    idx = current_col * num_rows + current_row
                    if idx < len(options):
                        # Clean up display
                        for _ in range(len(grid) + 1):
                            print(f"\r{CLEAR_LINE}")
                            print(UP, end='')
                        print(f"\r{CLEAR_LINE}")
                        print(f"\r{options[idx]}")
                        return options[idx]
                elif key == 27:  # Escape
                    # Clean up display
                    for _ in range(len(grid)):
                        print(f"\r{CLEAR_LINE}")
                        print(UP, end='')
                    print(f"\r{CLEAR_LINE}")
                    print(f"\r{prompt} cancelled")
                    return None