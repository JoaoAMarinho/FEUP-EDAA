class Color():
    """
    Color class
    """

    def __init__(self, red=0, green=0, blue=0, alpha=None):
        """
        Initialize color
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def increment(self, color):
        """
        Increment color
        """
        self.red += color.red
        self.green += color.green
        self.blue += color.blue

    def __str__(self):
        return "{self.red}-{self.green}-{self.blue}"
