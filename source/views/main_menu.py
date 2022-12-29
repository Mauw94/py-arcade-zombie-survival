import arcade 
from views.game_view import GameView

class MainMenu(arcade.View):
    def __init__(self, screen_width, screen_height) -> None:
        self.screen_height = screen_height
        self.screen_width = screen_width
        super().__init__()
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            self.screen_width / 2,
            self.screen_height / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        print("mouse pressed")
        game_view = GameView()
        self.window.show_view(game_view)