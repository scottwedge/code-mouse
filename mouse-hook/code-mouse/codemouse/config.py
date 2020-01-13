class Config:
    DURATION = 'days'               # everything will be computed in terms of this unit
    MIN_WEIGHT = 0
    MAX_WEIGHT = 100
    START_WEIGHT = 30
    MAX_WEIGHT_AFTER_FULL = 250
    RATE_OF_DECAY = 1               # how quickly mouse loses weight without food
    RATE_OF_GROWTH = 1 / 20.        # for ex, gains 1 unit per 20 staged changes
    SATIATION_INTERVAL = 1          # how long before RATE_OF_DECAY kicks in

    # TODO set config params and make sure they are legal
    def __init__(self, config):
        self.config = config
        self.set_duration()
        self.min_weight = Config.MIN_WEIGHT
        self.max_weight = Config.MAX_WEIGHT
        self.start_weight = Config.START_WEIGHT
        self.max_weight_after_full = Config.MAX_WEIGHT_AFTER_FULL
        self.rate_of_decay = Config.RATE_OF_DECAY
        self.rate_of_growth = Config.RATE_OF_GROWTH
        self.satiation_interval = Config.SATIATION_INTERVAL
    
    def set_duration(self):
        duration = self.config.get('duration')
        if duration and duration in ['days', 'hours', 'minutes']:
            self.duration = duration
        else:
            self.duration = Config.DURATION

    def display(self):
        print('Duration: {0}'.format(self.duration))
        print('Min weight: {0}'.format(self.min_weight))
        print('Max weight: {0}'.format(self.max_weight))
        print('Start weight: {0}'.format(self.start_weight))
        print('Max weight after full: {0}'.format(self.max_weight_after_full))
        print('Rate of decay: {0}'.format(self.rate_of_decay))
        print('Rate of growth: {0}'.format(self.rate_of_growth))
        print('Satiation interval: {0} {1}'.format(self.rate_of_decay, self.duration))