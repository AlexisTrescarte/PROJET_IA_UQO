import talib, numpy

RSI_PERIOD = 14
EMA_FAST_PERIOD = 50
EMA_SLOW_PERIOD = 100

class RSI_Algo:
    def __init__(self):
        self.closes_data_list = []
        self.rsi_list = []
        self.ema_50_list = []
        self.ema_100_list = []
        self.in_position = [False, None]
        self.list_of_trade = []
        self.want_buy = False
        self.want_sell = False
        

    def update(self, new_close_data):
        self.want_buy = False
        self.want_sell = False
        self.closes_data_list.append(float(new_close_data))
        
        if(len(self.closes_data_list) > EMA_SLOW_PERIOD):
            self.process_rsi()
        return self.want_buy, self.want_sell

    def process_rsi(self):
        self.closes_data_array = numpy.array(self.closes_data_list)

        self.rsi_list = talib.RSI(self.closes_data_array, RSI_PERIOD)
        self.ema_50_list = talib.EMA(self.closes_data_array, timeperiod=EMA_FAST_PERIOD)
        self.ema_100_list = talib.EMA(self.closes_data_array, timeperiod=EMA_SLOW_PERIOD)

        if (self.ema_50_list[-2]-self.ema_100_list[-2]<0) and (self.ema_50_list[-1]-self.ema_100_list[-1]>0) and not self.in_position[0]:
            self.want_buy = True
            self.buy()

        if self.get_last_rsi() > 70 and self.in_position[0]:
            self.want_sell = True
            self.sell()
        
    def get_rsi_list(self):
        return self.rsi_list

    def get_last_rsi(self):
        return self.rsi_list[-1]

    def get_performance(self):
        positive_trade=0
        for trade in self.list_of_trade:
            if trade>0:
                positive_trade+=1
        if len(self.list_of_trade) == 0:
            return 50
        return (positive_trade*100)/len(self.list_of_trade)

    def get_increase_rate(self):
        if(self.ema_50_list[-1]-self.ema_100_list[-1] < 0 ):
            return 0.4
        return 0.7

    def get_decrease_rate(self):
        if(self.ema_50_list[-1]-self.ema_100_list[-1] > 0 ):
            return 0.4
        return 0.7

    def buy(self):
        self.in_position[0] = True
        self.in_position[1] = float(self.closes_data_list[-1])
        # print("L'Algo RSI achete à : {}".format(self.in_position[1]))

    def sell(self):
        self.list_of_trade.append(float(self.closes_data_list[-1]) - self.in_position[1])
        self.in_position[0] = False
        self.in_position[1] = None
        # print("L'Algo RSI vend à : {}".format(float(self.closes_data_list[-1])))
        # print("L'algo RSI a une performance de {}".format(self.performance))