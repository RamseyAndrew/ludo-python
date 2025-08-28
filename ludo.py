from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import random

console = Console()

# Setup players and tokens with player-specific starting positions
players = {
    "Player 1": {"color": "Red", "tokens": [0, 0, 0, 0], "start_pos": 1, "finish_entry": 50},
    "Player 2": {"color": "Blue", "tokens": [0, 0, 0, 0], "start_pos": 14, "finish_entry": 11},
    "Player 3": {"color": "Green", "tokens": [0, 0, 0, 0], "start_pos": 27, "finish_entry": 24},
    "Player 4": {"color": "Yellow", "tokens": [0, 0, 0, 0], "start_pos": 40, "finish_entry": 37}
}

# Map player names to letters for the board
player_letters = {
    "Player 1": "R",
    "Player 2": "B", 
    "Player 3": "G",
    "Player 4": "Y"
}

# Safe positions where tokens can't be captured (traditional Ludo safe spots)
safe_positions = [1, 9, 14, 22, 27, 35, 40, 48]

# Track consecutive 6s for each player
consecutive_sixes = {"Player 1": 0, "Player 2": 0, "Player 3": 0, "Player 4": 0}

def welcome_screen():
    console.print("[bold green]🎲 Welcome to Terminal Ludo! 🎲[/bold green]\n")
    table = Table(title="Players")
    table.add_column("Player", style="cyan", justify="center")
    table.add_column("Color", style="magenta", justify="center")
    table.add_column("Start Position", style="yellow", justify="center")
    
    for name, info in players.items():
        table.add_row(
            name, 
            f"[bold {info['color'].lower()}]{info['color']}[/bold {info['color'].lower()}]",
            str(info['start_pos'])
        )
    console.print(table)
    console.print("\n[bold yellow]Game Rules:[/bold yellow]")
    console.print("• Roll 6 to enter tokens onto the board")
    console.print("• Get all 4 tokens to position 57 to win!")
    console.print("• Rolling 6 gives you another turn")
    console.print("• Landing on opponent's token sends it back home")
    console.print("• Safe positions: 1, 9, 14, 22, 27, 35, 40, 48")
    console.print("• Three consecutive 6s sends your newest token back home")
    console.print("• Must roll exact number to finish (can't overshoot)")










def roll_dice(player):
    dice = random.randint(1, 6)
    console.print(f"[bold yellow]{player}[/bold yellow] rolled a 🎲 [bold cyan]{dice}[/bold cyan]")
    
    # Track consecutive 6s
    if dice == 6:
        consecutive_sixes[player] += 1
        if consecutive_sixes[player] >= 3:
            console.print(f"[bold red]Three consecutive 6s! {player}'s most recent token returns home![/bold red]")
            # Find the token that's furthest along and send it home
            tokens = players[player]["tokens"]
            max_pos = max(tokens) if any(t > 0 for t in tokens) else 0
            if max_pos > 0:
                for i, pos in enumerate(tokens):
                    if pos == max_pos:
                        tokens[i] = 0
                        break
            consecutive_sixes[player] = 0
            return 0  # No move allowed
    else:
        consecutive_sixes[player] = 0
    
    return dice

def get_movable_tokens(player, dice):
    """Get list of tokens that can be moved with the current dice roll"""
    tokens = players[player]["tokens"]
    start_pos = players[player]["start_pos"]
    movable = []
    
    for i, pos in enumerate(tokens):
        if pos == 0 and dice == 6:  # Can enter board
            movable.append(i)
        elif pos > 0:
            new_pos = calculate_new_position(player, pos, dice)
            if new_pos <= 57:  # Can move without overshooting finish
                movable.append(i)
    
    return movable

def calculate_new_position(player, current_pos, dice_roll):
    """Calculate new position considering player-specific paths and finish lanes"""
    start_pos = players[player]["start_pos"]
    finish_entry = players[player]["finish_entry"]
    
    if current_pos == 0:  # Entering board
        return start_pos
    
    # Check if token is in finish lane (positions 51-57)
    if current_pos >= 51:
        return min(current_pos + dice_roll, 57)
    
    # Calculate position on main circuit (1-50)
    circuit_pos = (current_pos - start_pos) % 52
    new_circuit_pos = circuit_pos + dice_roll
    
    # Check if entering finish lane
    if new_circuit_pos >= 50:  # Ready to enter finish lane
        return 51 + (new_circuit_pos - 50)
    else:
        # Still on main circuit
        return start_pos + new_circuit_pos if start_pos + new_circuit_pos <= 52 else (start_pos + new_circuit_pos) - 52

def capture_token(position, current_player):
    """Check if any opponent tokens are captured at this position"""
    captured = []
    
    # Skip if position is safe or in finish lane
    if position in safe_positions or position >= 51:
        return captured
    
    for player, info in players.items():
        if player == current_player:
            continue
            
        for i, token_pos in enumerate(info["tokens"]):
            if token_pos == position:
                info["tokens"][i] = 0  # Send back to start
                captured.append((player, i + 1))
    
    return captured

def move_token(player, dice):
    """Handle token movement with player choice"""
    if dice == 0:  # Three consecutive 6s penalty
        return False
        
    movable_tokens = get_movable_tokens(player, dice)
    
    if not movable_tokens:
        console.print(f"[bold red]No valid moves for {player}![/bold red]")
        return False
    
    # Show current token positions
    show_player_tokens(player)
    
    if len(movable_tokens) == 1:
        # Only one option, move automatically
        token_idx = movable_tokens[0]
        console.print(f"[bold cyan]Moving token {token_idx + 1} automatically...[/bold cyan]")
    else:
        # Multiple options, let player choose
        console.print(f"[bold cyan]Movable tokens: {[i+1 for i in movable_tokens]}[/bold cyan]")
        while True:
            try:
                choice = int(Prompt.ask("Choose token to move (number)")) - 1
                if choice in movable_tokens:
                    token_idx = choice
                    break
                else:
                    console.print("[bold red]Invalid choice! Choose from available tokens.[/bold red]")
            except ValueError:
                console.print("[bold red]Please enter a valid number![/bold red]")
    
    # Move the chosen token
    old_pos = players[player]["tokens"][token_idx]
    new_pos = calculate_new_position(player, old_pos, dice)
    
    players[player]["tokens"][token_idx] = new_pos
    
    if old_pos == 0:  # Entering board
        console.print(f"[bold {players[player]['color'].lower()}]{player}'s token {token_idx + 1} enters the board at position {new_pos}![/bold {players[player]['color'].lower()}]")
    else:  # Moving on board
        console.print(f"[bold {players[player]['color'].lower()}]{player}'s token {token_idx + 1} moves from {old_pos} to {new_pos}[/bold {players[player]['color'].lower()}]")
    
    # Check for captures (only if not in finish lane)
    if new_pos < 51:
        captured = capture_token(new_pos, player)
        for captured_player, captured_token in captured:
            console.print(f"[bold red]💥 {captured_player}'s token {captured_token} was captured and sent home![/bold red]")
    
    return True

def show_player_tokens(player):
    """Show current positions of player's tokens"""
    tokens = players[player]["tokens"]
    color = players[player]["color"].lower()
    
    table = Table(title=f"{player}'s Tokens")
    table.add_column("Token", style="cyan")
    table.add_column("Position", style="magenta")
    table.add_column("Status", style="green")
    
    for i, pos in enumerate(tokens):
        if pos == 0:
            status = "Home"
        elif pos == 57:
            status = "Finished!"
        elif pos >= 51:
            status = f"Finish Lane ({pos-50}/6)"
        else:
            status = "On Board"
        
        table.add_row(
            f"Token {i + 1}", 
            str(pos) if pos > 0 else "Home",
            f"[bold {color}]{status}[/bold {color}]"
        )
    
    console.print(table)

def check_winner(player):
    """Check if player has won (all tokens at position 57)"""
    return all(token == 57 for token in players[player]["tokens"])











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
    
    # Mark safe spots with stars
    safe_spots = [(6, 2), (2, 6), (6, 12), (8, 12), (12, 8), (8, 2)]
    for (r, c) in safe_spots:
        if 0 <= r < 15 and 0 <= c < 15:
            board[r][c] = "[bold white]★[/bold white] "
    
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
    start_colors = ["red", "blue", "yellow", "g"]
    
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
    
    # Finish lane positions (51-57)
    finish_coords = [
        (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)  # Toward center
    ]
    
    for i, coord in enumerate(finish_coords):
        token_positions[51 + i] = coord
    
    # Place player tokens on board
    for player, info in players.items():
        color = info["color"].lower()
        letter = player_letters[player]
        
        for token_pos in info["tokens"]:
            if token_pos > 0 and token_pos in token_positions:
                row, col = token_positions[token_pos]
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












def main():
    welcome_screen()
    input("\nPress [Enter] to start the game...")
    
    player_list = list(players.keys())
    current_turn = 0
    game_over = False
    
    while not game_over:
        player = player_list[current_turn]
        
        console.print(f"\n{'='*50}")
        console.print(f"[bold cyan]{player}'s turn![/bold cyan]")
        
        input("Press [Enter] to roll the dice... ")
        dice = roll_dice(player)
        
        # Try to move a token
        move_made = move_token(player, dice)
        
        # Print updated board and status
        print_board()
        print_game_status()
        
        # Check for winner
        if check_winner(player):
            console.print(f"\n🎉 [bold green]{player} WINS![/bold green] 🎉")
            console.print("All tokens have reached the finish line!")
            game_over = True
            break
        
        # Handle turn progression
        if dice == 6 and move_made and dice != 0:
            console.print("🎲 [bold yellow]You rolled a 6! Take another turn![/bold yellow]")
            # Don't change current_turn, same player goes again
        else:
            # Move to next player
            current_turn = (current_turn + 1) % len(player_list)
        
        # Ask if player wants to continue or quit
        if not game_over:
            choice = Prompt.ask("\nContinue playing? ([bold green]y[/bold green]/[bold red]n[/bold red])", default="y")
            if choice.lower() in ['n', 'no', 'quit', 'exit']:
                console.print("Thanks for playing! 👋")
                break

if __name__ == "__main__":
    main()      


