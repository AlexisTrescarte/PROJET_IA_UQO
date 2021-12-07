from pyspark.sql import SparkSession

from pyspark import SparkConf, SparkContext


 

class SparkHistoricProcessor():
    
    def __init__(self):
        self.session = SparkSession.builder.appName('BinanceTradingBot').getOrCreate()
        self.df_trade_historic = self.session.read.csv('trade_historic.csv')

    def get_df_trade_historic(self):
        return self.df_trade_historic



session = SparkSession.builder.getOrCreate()

spark_historic = SparkHistoricProcessor()

df = spark_historic.get_df_trade_historic()

df.show()