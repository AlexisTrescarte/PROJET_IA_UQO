var chart = LightweightCharts.createChart(document.getElementById("chart_btc"), {
	width: screen.width-32,
  	height: screen.height/2,
	layout: {
		backgroundColor: '#ffffff',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000',
	borderDownColor: 'rgba(255, 144, 0, 1)',
	borderUpColor: 'rgba(255, 144, 0, 1)',
	wickDownColor: 'rgba(255, 144, 0, 1)',
	wickUpColor: 'rgba(255, 144, 0, 1)',
  });

// CHART 2

var chart2 = LightweightCharts.createChart(document.getElementById("chart_capital"), {
	width: screen.width-32,
  	height:  screen.height/2,
	layout: {
		backgroundColor: '#ffffff',
		textColor: 'rgba(33, 56, 77, 1)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.7)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.7)',
		},
	},
	timeScale: {
		timeVisible: true,
    secondsVisible: false,
	},
});

var lineSeries2 = chart2.addLineSeries();
var history = {}

//
// Trade table

function update_table(trade_history){
	listOfTrades = ``
	trade_history.forEach(trade =>
		listOfTrades += 
		`
		  <tr>
			<td scope="row"> ${trade['time']}</td>
			<td scope="row"> ${trade['prix_achat']}</td>
			<td scope="row"> ${trade['prix_vente']}</td>
			<td scope="row"> ${trade['value']}</td>
			<td scope="row"> ${trade['performance_RSI']}</td>
			<td scope="row"> ${trade['performance_MACD']}</td>
			<td scope="row"> ${trade['performance_EWO']}</td>
			<td scope="row"> ${trade['increase_rate_RSI']}</td>
			<td scope="row"> ${trade['increase_rate_MACD']}</td>
			<td scope="row"> ${trade['increase_rate_EWO']}</td>
		  </tr>
		  `
	  )

	console.log(listOfTrades);
	
	document.getElementById('trades_tab').innerHTML = listOfTrades;
}

//


// Récupération avec endpoint
fetch('http://127.0.0.1:5000//history')
	.then((r) => r.json())
	.then((response)=> {

		candleSeries.setData(response);

		print(response);
		fetch('http://127.0.0.1:5000//trades')
				.then((r) => r.json())
				.then((response)=> {
				lineSeries2.setData(response);
				update_table(response);
		})
})




var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/ethusdt@kline_1h");
binanceSocket.onmessage = function (event) {
	var candlestick = (JSON.parse(event.data)).k;
	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	});
	
	

	if(candlestick.x){

		fetch('http://127.0.0.1:5000//trades')
				.then((r) => r.json())
				.then((response)=> {
				lineSeries2.setData(response);
				update_table(response)
		})

		$.ajax(
				{
					type:'POST',
					contentType:'application/json',
					dataType:'json',
					url:'/pass_val',
					data: event.data,
					success:function (data) {
						var reply=data.reply;
						if (reply=="success")
						{
							return;
						}
						else
						{
						alert("some error ocured in session agent")
						}
		
				}
			}
		);
	}
	 
}