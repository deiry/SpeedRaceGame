from movement import Movement
from speed_racer_game import SpeedRacer
import threading
import asyncio

class Main:

    def game_init(self):
        # camera_thread = threading.Thread(target=movement.main)
        # camera_thread.start()
        speed_game = SpeedRacer()
        game_thread = threading.Thread(target=speed_game.main)
        game_thread.start()
        
        movement = Movement()
        movement.main()
        print("funciona asincrono")
        return


if __name__ == '__main__':
    game = Main()
    game.game_init()