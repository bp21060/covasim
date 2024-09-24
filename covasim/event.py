class Event:
    def __init__(self, measurement="n",condition="exposed", threshold=20, min_age=0, max_age=None, days=1):
        self.measurement = measurement
        self.condition = condition
        self.max_threshold = threshold #閾値(変動しない)
        self.threshold = threshold #閾値(複数回感染イベントが有るたびに下がるなどの変動をする)
        self.min_age = min_age
        self.max_age = max_age
        self.days = days
        self.days_list = [0] * days
        self.last_condition = None #対象が時刻t-1で対象となる病態になっていたかどうか
    
    def init_threshold(self,t):
        inds = t % self.days
        self.days_list[inds] = 0
        self.threshold = self.max_threshold-sum(self.days_list)
        #デバック
        print(f"threshold={self.threshold}")
        
    
    def update(self,t,num_target):
        
        inds = (t-1) % self.days #もう既に+1されているのでここで調整
        self.days_list[inds] = num_target
        
        #デバック
        print(num_target)
        print(self.days_list)