from flask import Flask, render_template, jsonify, request
from binance.client import Client
from binance.enums import *
from Python.bot_manager import BotManager
import config
from datetime import datetime, timedelta

client = Client(config.API_KEY, config.SECRET_KEY)
bot_manager = BotManager()

app = Flask(__name__)

@app.route("/")
def index():
    # Get client account
    account = client.get_account()
    # Get blanace for all crypto
    balances = account['balances']
    user_balances = []
    for balance in balances:
        if(float(balance['free'])>0):
            user_balances.append(balance)

    # Get all the symbols
    exchange_infos = client.get_exchange_info()
    symbols = exchange_infos['symbols']

    return render_template('index.html', user_balances=user_balances, symbols=symbols)


@app.route('/pass_val',methods=['POST'])
def pass_val():
    candelstick = (request.get_json())['k']
    bot_manager.update(candelstick)

    return jsonify({'reply':'success'})

@app.route('/history')
def history():

    now = datetime.now()
    first_date = now - timedelta(days = 730)
    candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, first_date.strftime("%d %b, %Y"), now.strftime("%d %b, %Y"))
    
    processed_candlesticks = []
    for data in candlesticks:
        candlesticks = {
            "time": data[0]/1000 ,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4],
        }
        processed_candlesticks.append(candlesticks)
    bot_manager.update_with_history(processed_candlesticks)
    return jsonify(processed_candlesticks)

@app.route('/trades')
def trades():
    return jsonify(bot_manager.trade_history)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')