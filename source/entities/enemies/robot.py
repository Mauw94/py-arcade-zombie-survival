from entities.enemy import Enemy

class RobotEnemy(Enemy):
    def __init__(self):
        
        super().__init__("robot", "robot")
        
        self.health = 100