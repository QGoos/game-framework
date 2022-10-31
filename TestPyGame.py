import Framework.gameFramework as gameFramework

def main():

    tick_rate = 60
    display_width = 1200
    display_height = 900
    game_name = "Generic"

    GAME = gameFramework.Game(tick_rate,display_width,display_height,game_name)
    GAME.run_game()

if __name__ == "__main__":
    main()