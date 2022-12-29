from entities.entity import Entity
from helpers.constants import Constants

class Enemy(Entity):
    def __init__(self, name_folder, name_file):
        super().__init__(name_folder, name_file)
        
        self.should_update_walk = 0
        self.health = 0
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.facing_direction == Constants.RIGHT_FACING:
            self.facing_right = Constants.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == Constants.LEFT_FACING:
            self.facing_right = Constants.RIGHT_FACING
            
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1