"""
Platformer Game
"""
import arcade
from views.main_menu import MainMenu
from helpers.constants import Constants

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, Constants.SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here


def main():
    """Main function"""
    window = arcade.Window(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, Constants.SCREEN_TITLE)
    menu_view = MainMenu(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
    window.show_view(menu_view)
    # window = MyGame()
    # window.setup()
    arcade.run()


if __name__ == "__main__":
    main()