from helpers.constants import Constants
from entities.entity import Entity


class PlayerCharacter(Entity):
    def __init__(self):
        super().__init__("male_person", "malePerson")

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0 and self.facing_direction == Constants.RIGHT_FACING:
            self.facing_direction = Constants.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == Constants.LEFT_FACING:
            self.facing_direction = Constants.RIGHT_FACING

        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
