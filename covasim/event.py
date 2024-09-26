class Event:
    def __init__(self, measurement="n",condition="exposed", threshold=20, min_age=0, max_age=None,layer=None, days=1):
        self.measurement = measurement
        self.condition = condition
        self.max_threshold = threshold #閾値(変動しない)
        self.threshold = threshold #閾値(複数回感染イベントが有るたびに下がるなどの変動をする)
        self.min_age = min_age
        self.max_age = max_age
        self.days = days
        self.days_list = [0] * days
        self.last_condition = None #対象が時刻t-1で対象となる病態になっていたかどうか
        self.last_loop_layer_counts = 0 #対象のlayerの最後のループのカウント
        self.last_t_layer_counts = 0 #対象のlayerの最後のt-1のカウント
        #レイヤーは省略化させる
        # 初期化時に layer に応じて self.layer の値を設定
        if layer == 'default_contact':
            self.layer = 'a'
        elif layer == 'household':
            self.layer = 'h'
        elif layer == 'school':
            print("layer正常に反応")
            self.layer = 's'
        elif layer == 'workplace':
            self.layer = 'w'
        elif layer == 'community':
            self.layer = 'c'
        else:
            # 該当しない場合は、Noneを設定
            self.layer = None
    
    def init_threshold(self,t):
        inds = t % self.days
        self.days_list[inds] = 0
        self.threshold = self.max_threshold-sum(self.days_list)
        #デバック
        #print(f"threshold={self.threshold}")
        
    
    def update(self,t,num_target):
        
        inds = t % self.days 
        self.days_list[inds] = num_target
        
        #デバック
        #print(num_target)
        #print(self.days_list)
        