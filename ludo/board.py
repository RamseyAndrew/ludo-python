from rich.console import console
from rich.table import Table
from players import players, player_letters, consecutive_sixes, safe_positions

def print_board():
    """Print the Ludo board with colorful layout"""
    # Create 15x15 board
    board = [["  " for _ in range(15)] for _ in range(15)]
    
    # Fill home areas (6x6 in corners) with colors
    # Top-left = Red home  
    for r in range(0, 6):
        for c in range(0, 6):
            board[r][c] = "[red]R[/red] "
    
    # Top-right = Blue home
    for r in range(0, 6):
        for c in range(9, 15):
            board[r][c] = "[blue]B[/blue] "
    
    # Bottom-left = Green home
    for r in range(9, 15):
        for c in range(0, 6):
            board[r][c] = "[green]G[/green] "
    
    # Bottom-right = Yellow home
    for r in range(9, 15):
        for c in range(9, 15):
            board[r][c] = "[yellow]Y[/yellow] "
    
    # Create the cross-shaped path
    # Vertical paths
    for r in range(0, 15):
        if r != 7:  # Skip center row
            board[r][6] = "[white]○[/white] "
            board[r][8] = "[white]○[/white] "
    
    # Horizontal paths
    for c in range(0, 15):
        if c != 7:  # Skip center column
            board[6][c] = "[white]○[/white] "
            board[8][c] = "[white]○[/white] "
    
    # Mark safe spots with stars based on ring indices in safe_positions
    # Map ring indices to board coordinates and decorate them
    # (we'll fill token_positions later; temporarily collect here and decorate after mapping)
    
    # Create finish lanes leading to center
    # Red finish lane (going right toward center)
    for c in range(1, 6):
        board[7][c] = "[bold red]△[/bold red] "
    
    # Blue finish lane (going down toward center)  
    for r in range(1, 6):
        board[r][7] = "[bold blue]△[/bold blue] "
    
    # Green finish lane (going left toward center)
    for c in range(9, 14):
        board[7][c] = "[bold green]△[/bold green] "
    
    # Yellow finish lane (going up toward center)
    for r in range(9, 14):
        board[r][7] = "[bold yellow]△[/bold yellow] "
    
    # Center square (finish position)
    board[7][7] = "[bold magenta]★[/bold magenta] "
    
    # Mark starting positions for each player
    start_markers = [(6, 1), (1, 8), (8, 13), (13, 6)]  # Red, Blue, Green, Yellow
    start_colors = ["red", "blue", "green", "yellow"]
    
    for i, (r, c) in enumerate(start_markers):
        board[r][c] = f"[bold {start_colors[i]}]◉[/bold {start_colors[i]}] "
    
    # Comprehensive token position mapping for proper Ludo circuit
    token_positions = {}
    
    # Main circuit positions (1-52) mapped to board coordinates
    # Starting from Red's entry and going clockwise
    circuit_coords = [
        # Red's path (bottom row, going right)
        (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
        (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), 
        (8, 11), (8, 12), (8, 13),
        
        # Right side going up
        (7, 13), (6, 13), (5, 13), (4, 13), (3, 13),
        (2, 13), (1, 13), (0, 13),
        
        # Top side going left  
        (0, 12), (0, 11), (0, 10), (0, 9), (0, 8),
        (0, 7), (0, 6), (0, 5), (0, 4), (0, 3),
        (0, 2), (0, 1), (0, 0),
        
        # Left side going down
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
        (6, 0), (7, 0), (8, 0), (9, 0), (10, 0),
        (11, 0), (12, 0), (13, 0), (14, 0),
        
        # Bottom going right back to start
        (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6)
    ]
    
    # Map circuit positions 1-52
    for i, coord in enumerate(circuit_coords[:52]):
        token_positions[i + 1] = coord
    
    # Finish lane positions (51-57) are player-specific; build per-player maps
    finish_lane_coords = {
        "Player 1": [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)],            # Red → right to center
        "Player 2": [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)],            # Blue → down to center
        "Player 3": [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7)],        # Green → left to center
        "Player 4": [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7), (7, 7)],        # Yellow → up to center
    }
    
    # Decorate safe ring squares
    for idx in safe_positions:
        if idx in token_positions:
            r, c = token_positions[idx]
            if 0 <= r < 15 and 0 <= c < 15:
                board[r][c] = "[bold white]★[/bold white] "

    # Place player tokens on board
    for player, info in players.items():
        color = info["color"].lower()
        letter = player_letters[player]
        
        for token_pos in info["tokens"]:
            if token_pos > 0 and 1 <= token_pos <= 52:
                if token_pos in token_positions:
                    row, col = token_positions[token_pos]
                    if 0 <= row < 15 and 0 <= col < 15:
                        board[row][col] = f"[bold {color}]{letter}[/bold {color}] "
            elif 51 <= token_pos <= 57:
                # Player-specific finish lane
                lane_idx = token_pos - 51
                coords = finish_lane_coords[player]
                row, col = coords[lane_idx]
                if 0 <= row < 15 and 0 <= col < 15:
                    board[row][col] = f"[bold {color}]{letter}[/bold {color}] "
    
    # Print the board
    console.print("\n[bold cyan]🎯 LUDO BOARD 🎯[/bold cyan]\n")
    
    for row in board:
        console.print("".join(row))
    
    console.print("\n[bold green]Legend:[/bold green]")
    console.print("[red]R[/red]/[blue]B[/blue]/[green]G[/green]/[yellow]Y[/yellow] = Home areas")
    console.print("[white]○[/white] = Regular path")
    console.print("[bold white]★[/bold white] = Safe spots")
    console.print("[bold red]△[/bold red]/[bold blue]△[/bold blue]/[bold green]△[/bold green]/[bold yellow]△[/bold yellow] = Finish lanes") 
    console.print("[bold magenta]★[/bold magenta] = Center (finish)")
    console.print("[bold red]◉[/bold red]/[bold blue]◉[/bold blue]/[bold green]◉[/bold green]/[bold yellow]◉[/bold yellow] = Starting positions")
    console.print("[bold red]R[/bold red]/[bold blue]B[/bold blue]/[bold green]G[/bold green]/[bold yellow]Y[/bold yellow] = Player tokens")

def print_game_status():
    """Print current game status for all players"""
    table = Table(title="Game Status")
    table.add_column("Player", style="cyan")
    table.add_column("Tokens Home", style="red")
    table.add_column("Tokens On Board", style="yellow") 
    table.add_column("Tokens in Finish", style="blue")
    table.add_column("Tokens Finished", style="green")
    table.add_column("Consecutive 6s", style="magenta")
    
    for player, info in players.items():
        tokens = info["tokens"]
        home = sum(1 for t in tokens if t == 0)
        on_board = sum(1 for t in tokens if 0 < t < 51)
        in_finish = sum(1 for t in tokens if 51 <= t < 57)
        finished = sum(1 for t in tokens if t == 57)
        sixes = consecutive_sixes[player]
        
        table.add_row(player, str(home), str(on_board), str(in_finish), str(finished), str(sixes))
    
    console.print(table)
