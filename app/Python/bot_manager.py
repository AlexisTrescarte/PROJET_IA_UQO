from Python.first_algo_RSI import RSI_Algo
from Python.second_algo_MACD import MACD_Algo
from Python.third_algo_EWO import EWO_Algo
from datetime import datetime
import csv, os


class BotManager():
    def __init__(self):
        self.candelsticks = []
        self.algo_RSI = RSI_Algo()
        self.algo_MACD = MACD_Algo()
        self.algo_EWO = EWO_Algo()
        self.in_position = [False, None]
        self.profit = 0
        self.trade_history = []

        if os.path.exists('trade_historic.csv'):
            os.remove('trade_historic.csv')


    def update_with_history(self, history):
        turn = 0
        for candelstick in history:
            self.candelsticks.append(candelstick)
            RSI_want_to_buy, RSI_want_to_sell = self.algo_RSI.update(candelstick['close'])
            MACD_want_to_buy, MACD_want_to_sell = self.algo_MACD.update(candelstick['close'])
            EWO_want_to_buy, EWO_want_to_sell = self.algo_EWO.update(candelstick['close'])

            if (RSI_want_to_buy or MACD_want_to_buy or EWO_want_to_buy) and not self.in_position[0] and turn>100:
                self.launch_jugment_aggregation_buy(RSI_want_to_buy, MACD_want_to_buy )

            if (RSI_want_to_sell or MACD_want_to_sell or EWO_want_to_sell) and self.in_position[0] and turn>100:
                self.launch_jugment_aggregation_sell(RSI_want_to_sell, MACD_want_to_sell)
            turn+=1

    def update(self,new_candelstick):
        self.candelsticks.append(new_candelstick)
        RSI_want_to_buy, RSI_want_to_sell = self.algo_RSI.update(new_candelstick['c'])
        MACD_want_to_buy, MACD_want_to_sell = self.algo_MACD.update(new_candelstick['c'])
        EWO_want_to_buy, EWO_want_to_sell = self.algo_EWO.update(new_candelstick['c'])

        if (RSI_want_to_buy or MACD_want_to_buy or EWO_want_to_buy) and not self.in_position[0]:
            self.launch_jugment_aggregation_buy()

        if (RSI_want_to_sell or MACD_want_to_sell or EWO_want_to_sell) and self.in_position[0]:
            self.launch_jugment_aggregation_sell()

    

    def launch_jugment_aggregation_buy(self, RSI_want_to_buy, MACD_want_to_buy):

        # Est-tu performant ?
        rsi_performance = self.algo_RSI.get_performance()
        macd_performance = self.algo_MACD.get_performance()
        ewo_performance = self.algo_EWO.get_performance()

        if RSI_want_to_buy:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = 1
            macd_increase_rate = self.algo_MACD.get_increase_rate()
            ewo_increase_rate = self.algo_EWO.get_increase_rate()

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate
            if score > 100:
                self.in_position=[True, float(self.candelsticks[-1]['close'])]

                

        elif MACD_want_to_buy:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = self.algo_RSI.get_increase_rate()
            macd_increase_rate = 1
            ewo_increase_rate = self.algo_EWO.get_increase_rate()

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate
            if score > 100:
                self.in_position=[True, float(self.candelsticks[-1]['close'])]


        else:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = self.algo_RSI.get_increase_rate()
            macd_increase_rate = self.algo_MACD.get_increase_rate()
            ewo_increase_rate = 1

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate
            if score > 100:
                self.in_position=[True, float(self.candelsticks[-1]['close'])]
        

    def launch_jugment_aggregation_sell(self, RSI_want_to_sell, MACD_want_to_sell):

        score = 0

        # Est-tu performant ?
        rsi_performance = self.algo_RSI.get_performance()
        macd_performance = self.algo_MACD.get_performance()
        ewo_performance = self.algo_EWO.get_performance()

        if RSI_want_to_sell:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = 1
            macd_increase_rate = self.algo_MACD.get_decrease_rate()
            ewo_increase_rate = self.algo_EWO.get_decrease_rate()

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate


        elif MACD_want_to_sell:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = self.algo_RSI.get_decrease_rate()
            macd_increase_rate = 1
            ewo_increase_rate = self.algo_EWO.get_decrease_rate()

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate
            

        else:
            # Pense-tu que le prix va monter ?
            rsi_increase_rate = self.algo_RSI.get_decrease_rate()
            macd_increase_rate = self.algo_MACD.get_decrease_rate()
            ewo_increase_rate = 1

            # Veux-tu acheter ? 
            score = rsi_performance*rsi_increase_rate+macd_performance*macd_increase_rate+ewo_performance*ewo_increase_rate

        if score > 100:

                date = datetime.fromtimestamp(self.candelsticks[-1]['time']).strftime('%H:%M-%d-%m-%y')
                open_price = str(self.in_position[1])
                close_price = self.candelsticks[-1]['close']

                trade_info = [date, open_price, close_price]

                if len(self.trade_history) == 0 :
                     self.trade_history.append( { 
                         "time" : self.candelsticks[-1]['time'] ,
                         "prix_achat" : self.in_position[1],
                         "prix_vente" : float(self.candelsticks[-1]['close']),
                         "value" : 10000 + ( 10000*(float(self.candelsticks[-1]['close'])-self.in_position[1]) / float(self.candelsticks[-1]['close'])),
                         "performance_RSI": rsi_performance,
                         "performance_MACD": macd_performance,
                         "performance_EWO": ewo_performance,
                         "increase_rate_RSI": rsi_increase_rate,
                         "increase_rate_MACD": macd_increase_rate,
                         "increase_rate_EWO": ewo_increase_rate
                     } )

                else :
                     self.trade_history.append( { 
                         "time" : self.candelsticks[-1]['time'] ,
                         "prix_achat" : self.in_position[1],
                         "prix_vente" : float(self.candelsticks[-1]['close']),
                         "value" : self.trade_history[-1]['value'] + ( 10000*(float(self.candelsticks[-1]['close'])-self.in_position[1]) / float(self.candelsticks[-1]['close'])),
                         "performance_RSI": rsi_performance,
                         "performance_MACD": macd_performance,
                         "performance_EWO": ewo_performance,
                         "increase_rate_RSI": rsi_increase_rate,
                         "increase_rate_MACD": macd_increase_rate,
                         "increase_rate_EWO": ewo_increase_rate
                     } )


                with open('trade_historic.csv', 'a', newline='') as csvfile:
                    writer_csv = csv.writer(csvfile, delimiter=' ')
                    writer_csv.writerow(trade_info)
                    csvfile.close()

                profit = float(self.candelsticks[-1]['close']) - self.in_position[1]
                self.in_position=[False, None]
                self.profit+=profit