
class Selection():
    UNIT_KEY = "unit"
    TARGET_KEY = "target"
    def __init__(self, unit_position=None, target_position=None):
        self.unit_position = unit_position
        self.target_position = target_position
    
    @classmethod
    def from_dict(cls, dict):
        return cls(
            unit_position = dict.get(cls.UNIT_KEY, None),
            target_position = dict.get(cls.TARGET_KEY, None)
        )
    
    def to_dict(self):
        return {
            self.UNIT_KEY : self.unit_position,
            self.target_position : self.target_position
        }