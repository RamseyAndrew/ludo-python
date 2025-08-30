from rich.console import Console
from rich.table import Table

console = Console()

players = {
    "Player 1": {"color": "Red", "tokens": [0, 0, 0, 0], "start_pos": 1, "finish_entry": 50},
    "Player 2": {"color": "Blue", "tokens": [0, 0, 0, 0], "start_pos": 14, "finish_entry": 11},
    "Player 3": {"color": "Green", "tokens": [0, 0, 0, 0], "start_pos": 27, "finish_entry": 24},
    "Player 4": {"color": "Yellow", "tokens": [0, 0, 0, 0], "start_pos": 40, "finish_entry": 37}
}

player_letters = {
    "Player 1": "R",
    "Player 2": "B", 
    "Player 3": "G",
    "Player 4": "Y"
}

safe_positions = [1, 9, 14, 22, 27, 35, 40, 48]
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