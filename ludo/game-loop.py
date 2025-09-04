def main():
    welcome_screen()
    input("\nPress [Enter] to start the game...")
    
    # Setup persistence (optional)
    SessionFactory = get_session_factory() if get_session_factory else None
    session = SessionFactory() if SessionFactory else None
    game_id = None
    

    if session and GameModel and PlayerModel:
        # Ensure players exist
        existing_players = {p.name: p for p in session.query(PlayerModel).all()}
        for name, info in players.items():
            if name not in existing_players:
                p = PlayerModel(name=name, color=info["color"])
                session.add(p)
        session.commit()

        # Create game record
        game = GameModel(started_at=datetime.utcnow())
        session.add(game)
        session.commit()
        game_id = game.id

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
        moved, token_idx, old_pos, new_pos = move_token(player, dice)
        
        # Persist move if applicable
        if session and game_id and MoveModel and PlayerModel and moved and token_idx is not None:
            db_player = session.query(PlayerModel).filter_by(name=player).first()
            mv = MoveModel(
                game_id=game_id,
                player_id=db_player.id if db_player else None,
                turn_index=turn_counter,
                dice=dice,
                token_index=token_idx + 1,
                old_pos=old_pos,
                new_pos=new_pos,
            )
            session.add(mv)
            session.commit()

        turn_counter += 1

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
        if dice == 6 and moved and dice != 0:
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

    # Close game
    if session and game_id and GameModel:
        game = session.query(GameModel).get(game_id)
        if game:
            game.ended_at = datetime.utcnow()
            session.commit()
        session.close()

if __name__ == "__main__":
    main()      


