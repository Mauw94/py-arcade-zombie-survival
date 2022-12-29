from entities.enemy import Enemy

class ZombieEnemy(Enemy):
    def __init__(self):
        
        super().__init__("zombie", "zombie")
        self.health = 50