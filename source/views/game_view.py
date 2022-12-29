import arcade
import os

from entities.player_character import PlayerCharacter
from helpers.constants import Constants

class GameView(arcade.View):
 
    def __init__(self):
        super().__init__()
        
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
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
        
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
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
        
        self.tile_map = arcade.load_tilemap(map_name, Constants.TILE_SCALING, layer_options)
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
        
        # TODO add enemies
        
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
        
