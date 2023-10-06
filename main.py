from game import Game


def main():
    g = Game()
    while g.running:
        if g.isMainMenu:
            g.main_menu.show()
        elif not g.isMainMenu:
            g.settings_menu.show()
        g.game_loop()


if __name__ == "__main__":
    main()
