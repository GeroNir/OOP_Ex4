class Pokemon():
    def __init__(self, pokemon):
        x, y = str(pokemon["pos"]).split(',')
        x = x[12:]
        y = y[3:-1]
        self.x = float(x)
        self.y = float(y)
        self.value = pokemon['value']
        self.type = pokemon['type']