import arcade
from typing import TYPE_CHECKING
from helpers.constants import Constants

if TYPE_CHECKING:  # Some weird way to avoid circular dependencies but still have typechecking
    from views.game_view import GameView


class Keys:

    def process_keychange(self, game: 'GameView'):
        # Process up/down
        if game.up_pressed and not game.down_pressed:
            if game.physics_engine.is_on_ladder():
                game.player_sprite.change_y = Constants.PLAYER_MOVEMENT_SPEED
            elif game.physics_engine.can_jump(y_distance=10) and not game.jump_needs_reset:
                game.player_sprite.change_y = Constants.PLAYER_JUMP_SPEED
                game.jump_needs_reset = True
        elif game.down_pressed and not game.up_pressed:
            if game.physics_engine.is_on_ladder():
                game.player_sprite.chaneg_y = -Constants.PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if game.physics_engine.is_on_ladder():
            if not game.up_pressed and not game.down_pressed:
                game.player_sprite.change_y = 0
            elif game.up_pressed and game.down_pressed:
                game.player_sprite.change_y = 0

        # Process left/right
        if game.right_pressed and not game.left_pressed:
            game.player_sprite.change_x = Constants.PLAYER_MOVEMENT_SPEED
        elif game.left_pressed and not game.right_pressed:
            game.player_sprite.change_x = -Constants.PLAYER_MOVEMENT_SPEED
        else:
            game.player_sprite.change_x = 0

    def on_key_press(self, game, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            game.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            game.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            game.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            game.right_pressed = True

        if key == arcade.key.Q:
            game.shoot_pressed = True

        if key == arcade.key.PLUS:
            game.camera.zoom(0.01)
        elif key == arcade.key.MINUS:
            game.camera.zoom(-0.01)

        self.process_keychange(game)

    def on_key_release(self, game, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            game.up_pressed = False
            game.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            game.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            game.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            game.right_pressed = False

        if key == arcade.key.Q:
            game.shoot_pressed = False

        self.process_keychange(game)

    def on_mouse_scroll(self, game, x, y, scroll_x, scroll_y):
        game.camera.zoom(-0.01 * scroll_y)
