class Mouse():
    __instance = None

    # Called when instantiating, cls is Mouse
    def __new__(cls):
        if Mouse.__instance is None:
            Mouse.__instance = object.__new__(cls)
            Mouse.__instance.name = None
        return Mouse.__instance

    # Called each time something is returned by new
    def __init__(self):
        pass

    
m = Mouse()
m.weight = 10

