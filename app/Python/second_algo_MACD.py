import talib, numpy

SIGNAL_PERIOD=9
FAST_PERIOD=12
SLOW_PERIOD=26
MACD_PERIOD=34

class MACD_Algo:
    def __init__(self):
        self.closes_data_list = []
        self.macd_list = []
        self.in_position = [False, None]
        self.list_of_trade = []
        self.want_buy = False
        self.want_sell = False

    def update(self, new_close_data):
        self.want_buy = False
        self.want_sell = False
        self.closes_data_list.append(float(new_close_data))

        if(len(self.closes_data_list) > MACD_PERIOD):
            self.process_macd()

        return self.want_buy, self.want_sell

    def process_macd(self):
        self.closes_data_array = numpy.array(self.closes_data_list)
        macd, macdsignal, macdhist = talib.MACD(self.closes_data_array, fastperiod=FAST_PERIOD, slowperiod=SLOW_PERIOD, signalperiod=SIGNAL_PERIOD)
        self.macd_list = [macd, macdsignal]

        if(macd[-1]-macdsignal[-1]>0 and macd[-2]-macdsignal[-2]<0 and self.in_position[0]):
            self.want_sell = True
            self.sell()

        if(macd[-1]-macdsignal[-1]<0 and macd[-2]-macdsignal[-2]>0 and not self.in_position[0]):
            self.want_buy = True
            self.buy()

        
    def get_macd_list(self):
        return self.macd_list

    def get_last_macd(self):
        return self.macd_list[-1]

    def get_performance(self):
        positive_trade=0
        for trade in self.list_of_trade:
            if trade>0:
                positive_trade+=1
        if len(self.list_of_trade) == 0:
            return 50
        return (positive_trade*100)/len(self.list_of_trade)

    def get_increase_rate(self):
        if( self.macd_list[0][-1]-self.macd_list[1][-1] < 0 ):
            return 0.4
        return 0.7

    def get_decrease_rate(self):
        if( self.macd_list[0][-1]-self.macd_list[1][-1] > 0 ):
            return 0.4
        return 0.75

    def buy(self):
        self.in_position[0] = True
        self.in_position[1] = float(self.closes_data_list[-1])
        # print("L'Algo MACD achete à : {}".format(self.in_position[1]))

    def sell(self):
        self.list_of_trade.append(float(self.closes_data_list[-1]) - self.in_position[1])
        self.in_position[0] = False
        self.in_position[1] = None
        # print("L'Algo MACD vend à : {}".format(float(self.closes_data_list[-1])))
        # print("L'algo MACD a une performance de {}".format(self.performance))