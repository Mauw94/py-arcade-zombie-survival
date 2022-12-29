import arcade
from entities.entity import Entity

class PlayerCharacter(Entity):
    def __init__(self):
        super().__init__("male_person", "malePerson")
        
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        
    