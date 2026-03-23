from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    crypto = "BTC-USD"
    days = 30
    forecast_data = None

    if request.method == "POST":
        crypto = request.form.get("crypto")
        days = int(request.form.get("days"))

        try:
            # Load data
            today = date.today()
            start_date = today - timedelta(days=365)

            data = yf.download(crypto, start=start_date, end=today)
            data.reset_index(inplace=True)

            # Dummy forecast (replace with ML later)
            forecast = pd.DataFrame({
                "index": pd.date_range(start=today, periods=days),
                "Close": [50000 + i * 200 for i in range(days)]
            })

            # Debug print
            print(forecast.head())

            # Convert to JSON
            forecast_data = forecast.to_dict(orient="records")
            forecast["index"] = forecast["index"].astype(str)

        except Exception as e:
            print("ERROR:", e)

    return render_template("index.html", forecast=forecast_data, crypto=crypto)


if __name__ == "__main__":
    app.run(debug=True)