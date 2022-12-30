import arcade
import os
import math

from entities.player_character import PlayerCharacter
from helpers.constants import Constants
from input.keys import Keys
from entities.enemies.robot import RobotEnemy
from entities.enemies.zombie import ZombieEnemy


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.handle_input = Keys()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None

        self.end_of_map = 0
        self.score = 0
        self.can_shoot = False
        self.shoot_timer = 0

        self.collect_coin_sound = arcade.load_sound(
            ":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        map_name = ":resources:tiled_maps/map_with_ladders.json"

        layer_options = {
            Constants.LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True
            },
            Constants.LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": True
            },
            Constants.LAYER_NAME_LADDERS: {
                "use_spatial_hash": True
            },
            Constants.LAYER_NAME_COINS: {
                "use_spatial_hash": True
            },
        }

        self.tile_map = arcade.load_tilemap(
            map_name, Constants.TILE_SCALING, layer_options)
        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.score = 0
        self.can_shoot = True
        self.shoot_timer = 0

        # Create player
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = (
            self.tile_map.tile_width * Constants.TILE_SCALING * Constants.PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * Constants.TILE_SCALING * Constants.PLAYER_START_Y
        )
        self.scene.add_sprite(Constants.LAYER_NAME_PLAYER, self.player_sprite)

        self.end_of_map = self.tile_map.width * Constants.GRID_PIXEL_SIZE

        enemies_layer = self.tile_map.object_lists[Constants.LAYER_NAME_ENEMIES]

        for obj in enemies_layer:
            cartesian = self.tile_map.get_cartesian(obj.shape[0], obj.shape[1])
            enemy_type = obj.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy()
            elif enemy_type == "zombie":
                enemy = ZombieEnemy()
            enemy.center_x = math.floor(
                (cartesian[0] * Constants.TILE_SCALING *
                 self.tile_map.tile_width)
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) *
                (Constants.TILE_SCALING * self.tile_map.tile_height)
            )

            if "boundary_left" in obj.properties:
                enemy.boundary_left = obj.properties["boundary_left"]
            if "boundary_right" in obj.properties:
                enemy.boundary_right = obj.properties["boundary_right"]
            if "change_x" in obj.properties:
                enemy.change_x = obj.properties["change_x"]

            self.scene.add_sprite(Constants.LAYER_NAME_ENEMIES, enemy)

        self.scene.add_sprite_list(Constants.LAYER_NAME_BULLETS)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[Constants.LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=Constants.GRAVITY,
            ladders=self.scene[Constants.LAYER_NAME_LADDERS],
            walls=self.scene[Constants.LAYER_NAME_PLATFORMS]
        )

    def on_show_view(self):
        self.setup()

    def on_draw(self):

        self.clear()

        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()

        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18
        )

    def on_update(self, delta_time):

        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.player_sprite.jumping = False
        else:
            self.player_sprite.jumping = True
        
        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_spite.is_on_ladder = True
            self.handle_input.process_keychange(self)
        else:
            self.player_sprite.is_on_ladder = False
            self.handle_input.process_keychange(self)
        
        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", Constants.SPRITE_SCALING_LASER)
                if self.player_sprite.facing_direction == Constants.RIGHT_FACING:
                    bullet.change_x += Constants.BULLET_SPEED
                else:
                    bullet.change_x -= Constants.BULLET_SPEED
                
                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y
                
                self.scene.add_sprite(Constants.LAYER_NAME_BULLETS, bullet)
                
                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == Constants.SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0
            
        # Update animations
        self.scene.update_animation(
            delta_time,
            [
                Constants.LAYER_NAME_COINS,
                Constants.LAYER_NAME_BACKGROUND,
                Constants.LAYER_NAME_PLAYER,
                Constants.LAYER_NAME_ENEMIES,
            ],
        )

        # Update moving platforms, enemies and bullets
        self.scene.update(
            [Constants.LAYER_NAME_ENEMIES, Constants.LAYER_NAME_MOVING_PLATFORMS,
                Constants.LAYER_NAME_BULLETS]
        )

        # See if enemy hit a boundary and needs to reverse direction
        for enemy in self.scene[Constants.LAYER_NAME_ENEMIES]:
            if enemy.boundary_right and enemy.right > enemy.boundary_right and enemy.change_x > 0:
                enemy.change_x *= -1

            if enemy.boundary_left and enemy.left < enemy.boundary_left and enemy.change_x < 0:
                enemy.change_x *= -1

        # Check for bullet collisions with enemies or platforms
        for bullet in self.scene[Constants.LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet, 
                [
                    self.scene[Constants.LAYER_NAME_ENEMIES], 
                    self.scene[Constants.LAYER_NAME_PLATFORMS],
                    self.scene[Constants.LAYER_NAME_MOVING_PLATFORMS]
                ]
            )
            
            if hit_list:
                bullet.remove_from_sprite_lists()    
                for collision in hit_list:
                    if self.scene[Constants.LAYER_NAME_ENEMIES] in collision.sprite_lists:
                        collision.health -= Constants.BULLET_DAMAGE
                        if collision.health <= 0:
                            collision.remove_from_sprite_lists()
                            self.score += 10
                        arcade.play_sound(self.hit_sound)
                return
            
            # Remove bullet if off screen
            if bullet.right < 0 or bullet.left > (self.tile_map.width * self.tile_map.tile_width) * Constants.TILE_SCALING:
                bullet.remove_from_sprite_lists()
            
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[Constants.LAYER_NAME_COINS],
                self.scene[Constants.LAYER_NAME_ENEMIES]
            ]
        )

        for collision in player_collision_list:
            if self.scene[Constants.LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                game_view = GameOverView()
                self.window.show_view(game_view)
                return
            else:
                if "Points" not in collision.properties:
                    print("Warning, collected a coin without a Points property")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points
                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        self.center_camera_to_player()

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.camera.scale * (
            self.player_sprite.center_x - (self.camera.viewport_width / 2)
        )
        screen_center_y = self.camera.scale * (
            self.player_sprite.center_y - (self.camera.viewport_height / 2)
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered, speed)

    def process_keychange(self):
        self.handle_input.process_keychange(self)

    def on_key_press(self, key, modifiers):
        self.handle_input.on_key_press(self, key, modifiers)

    def on_key_release(self, key, modifiers):
        self.handle_input.on_key_release(self, key, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.handle_input.on_mouse_scroll(self, x, y, scroll_x, scroll_y)


class GameOverView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Game Over - Click to restart",
            Constants.SCREEN_WIDTH / 2,
            Constants.SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)
