from flask import Flask, render_template, request # type: ignore
import pandas as pd  # noqa: F401
import yfinance as yf # type: ignore
from autots import AutoTS # type: ignore
from datetime import date, timedelta
import json  # noqa: F401

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    crypto = "BTC-USD"
    days = 30
    forecast_data = None
    
    if request.method == "POST":
        crypto = request.form.get("crypto")
        days = int(request.form.get("days"))
        
        today = date.today()
        start_date = today - timedelta(days=730)
        
        data = yf.download(crypto, start=start_date, end=today)
        data.reset_index(inplace=True) 
        
        model = AutoTS(forecast_length=days, frequency='infer')
        model = model.fit(data, date_col='Date', value_col='Close')
        
        prediction = model.predict()
        forecast = prediction.forecast.reset_index()
        
        forecast_data = forecast.to_dict(orient="records")
    
    return render_template("index.html", forecast=forecast_data, crypto=crypto)

if __name__ == "__main__":
    app.run(debug=True)