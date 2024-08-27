import requests
import smtplib
from email.mime.text import MIMEText

def get_stock_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    latest_time = list(data['Time Series (1min)'].keys())[0]
    price = float(data['Time Series (1min)'][latest_time]['1. open'])
    return price

def send_email_notification(subject, body, to_email):
    from_email = "my_email@example.com"
    password = "my_email_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Example usage
api_key = "my_alphavantage_api_key"
symbol = "AAPL"
threshold_price = 150.00
to_email = "my_email@example.com"

price = get_stock_price(symbol, api_key)
if price < threshold_price:
    send_email_notification(
        subject=f"Stock Alert: {symbol} below ${threshold_price}",
        body=f"The current price of {symbol} is ${price}.",
        to_email=to_email
    )
