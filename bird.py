class Bird:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return f'{self.color}'

    def get_upflap(self):
        if self.color == "Blue":
            'assets/bluebird-upflap.png'
        elif self.color == "Yellow":
            'assets/yellowbird-upflap.png'
        else:
            'assets/redbird-upflap.png'

    def get_midflap(self):
        if self.color == "Blue":
            'assets/bluebird-midflap.png'
        elif self.color == "Yellow":
            'assets/yellowbird-midflap.png'
        else:
            'assets/redbird-midflap.png'

    def get_downflap(self):
        if self.color == "Blue":
            'assets/bluebird-downflap.png'
        elif self.color == "Yellow":
            'assets/yellowbird-downflap.png'
        else:
            'assets/redbird-downflap.png'
