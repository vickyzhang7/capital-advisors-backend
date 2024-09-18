from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os  
from dotenv import load_dotenv  


load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'Time Series (Daily)' in data:
        daily_data = data['Time Series (Daily)']
        dates = list(daily_data.keys())
        closing_prices = [float(daily_data[date]['4. close']) for date in dates]

        # Reverse the order of the dates and prices to show the oldest first
        return {
            'dates': dates[:10][::-1],  # Reverse the list of dates
            'prices': closing_prices[:10][::-1]  # Reverse the list of prices
        }
    else:
        return {'error': 'Unable to fetch data for the symbol'}
    
@app.route('/')
def home():
    return "Welcome to the Stock Price API"

@app.route('/stock/<symbol>', methods=['GET'])
def stock(symbol):
    data = get_stock_data(symbol)
    return jsonify(data)

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    port = int(os.environ.get('PORT', 5001))  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)


