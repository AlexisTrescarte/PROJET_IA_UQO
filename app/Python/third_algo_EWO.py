import talib, numpy

FAST_PERIOD=5
SLOW_PERIOD=35

class EWO_Algo:
    def __init__(self):
        self.closes_data_list = []
        self.ewo_list = []
        self.in_position = [False, None]
        self.list_of_trade = []
        self.want_buy = False
        self.want_sell = False

    def update(self, new_close_data):
        self.want_buy = False
        self.want_sell = False
        self.closes_data_list.append(float(new_close_data))
        if(len(self.closes_data_list) > SLOW_PERIOD):
            self.process_ewo()

        return self.want_buy, self.want_sell

    def process_ewo(self):
        self.closes_data_array = numpy.array(self.closes_data_list)
        self.ewo_list = talib.SMA(self.closes_data_array, timeperiod=FAST_PERIOD) - talib.SMA(self.closes_data_array, timeperiod=SLOW_PERIOD)

        if(self.ewo_list[-1]<0 and self.ewo_list[-2]>0 and self.in_position[0]):
            self.want_sell = True
            self.sell()

        if(self.ewo_list[-1]>0 and self.ewo_list[-2]<0 and not self.in_position[0]):
            self.want_buy = True
            self.buy()


        
    def get_awo_list(self):
        return self.ewo_list

    def get_last_awo(self):
        return self.ewo_list[-1]

    def get_performance(self):
        positive_trade=0
        for trade in self.list_of_trade:
            if trade>0:
                positive_trade+=1
        if len(self.list_of_trade) == 0:
            return 50
        return (positive_trade*100)/len(self.list_of_trade)

    def get_increase_rate(self):
        if(self.ewo_list[-1]>0):
            return 0.4
        return 0.7

    def get_decrease_rate(self):
        if(self.ewo_list[-1]<0):
            return 0.4
        return 0.7


    def buy(self):
        self.in_position[0] = True
        self.in_position[1] = float(self.closes_data_list[-1])
        # print("L'Algo EWO achete à : {}".format(self.in_position[1]))

    def sell(self):
        self.list_of_trade.append(float(self.closes_data_list[-1]) - self.in_position[1])
        self.in_position[0] = False
        self.in_position[1] = None
        # print("L'Algo EWO vend à : {}".format(float(self.closes_data_list[-1])))
        # print("L'algo EWO a une performance de {}".format(self.performance))