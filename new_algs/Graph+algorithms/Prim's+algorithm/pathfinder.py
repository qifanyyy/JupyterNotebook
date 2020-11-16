# imports
import ctypes
from boards.game_board import Game
from boards.game_setup_board import GameSetup
import platform

# avoiding display scalling by windows "maku UI larger or smaller"
if platform.system() == 'Windows':
    ctypes.windll.user32.SetProcessDPIAware()

# starting game:
if __name__ == "__main__":
    actual_game = GameSetup()
    p1_icon, p2_icon = actual_game.game_setup_loop()
    actual_game = Game(p1_icon, p2_icon)
    actual_game.game_loop(actual_game)


# TODO special blocks (path, increase bomb range)
# TODO kicking bombs !
# TODO new players pictures
# TODO boards (game engine) refactor (as queue)
# TODO code refactor
# TODO over network multiplayer
