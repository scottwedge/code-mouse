class Config:
    '''Singleton'''

    DURATION = 'days'               # everything will be computed in terms of this unit
    MIN_WEIGHT = 0
    MAX_WEIGHT = 100
    START_WEIGHT = 1
    MAX_WEIGHT_AFTER_FULL = 250
    RATE_OF_DECAY = 1               # how quickly mouse loses weight without food
    RATE_OF_GROWTH = 1 / 20.        # for ex, gains 1 unit per 20 staged changes
    SATIATION_INTERVAL = 1          # how long before RATE_OF_DECAY kicks in

    __instance = None

    # TODO set config params from file and make sure they are legal
    def __new__(cls, config=None):
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)
            Config.__instance.config = config
        return Config.__instance

    # def __init__(self, config=None):
    #     self.config = config
    #     self.set_duration()
    
    # def set_duration(self):
    #     duration = self.config.get('duration')
    #     if duration and duration in ['days', 'hours', 'minutes']:
    #         self.duration = duration
    #     else:
    #         self.duration = Config.DURATION
        
    def __str__(self):
        return '''
        duration = {0}
        min_weight = {1}
        max_weight = {2}
        start_weight = {3}
        max_weight_after_full = {4}
        rate_of_decay = {5}
        rate_of_growth = {6}
        satiation_interval = {7} {8}
        '''.format(
            self.DURATION,
            self.MIN_WEIGHT,
            self.MAX_WEIGHT,
            self.START_WEIGHT,
            self.MAX_WEIGHT_AFTER_FULL,
            self.RATE_OF_DECAY,
            self.RATE_OF_GROWTH,
            self.SATIATION_INTERVAL,
            self.DURATION,
        )
