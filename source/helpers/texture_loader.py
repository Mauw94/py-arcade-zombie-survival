import arcade

class TextureLoader:
    def load_texture_pair(self, filename):
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]