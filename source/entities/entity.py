import arcade
import helpers.texture_loader

from helpers.constants import Constants


class Entity(arcade.Sprite):

    texture_loader = helpers.texture_loader.TextureLoader()

    def __init__(self, name_folder, name_file):
        super().__init__()

        self.facing_direction = Constants.RIGHT_FACING

        self.cur_texture = 0
        self.scale = Constants.CHARACTER_SCALING

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

        self.idle_texture_pair = self.texture_loader.load_texture_pair(
            f"{main_path}_idle.png")
        self.jump_texture_pair = self.texture_loader.load_texture_pair(
            f"{main_path}_jump.png")
        self.fall_texture_pair = self.texture_loader.load_texture_pair(
            f"{main_path}_fall.png")

        self.walk_textures = []
        for i in range(8):
            texture = self.texture_loader.load_texture_pair(
                f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

        self.set_hit_box(self.texture.hit_box_points)
