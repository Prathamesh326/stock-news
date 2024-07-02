import requests
import smtplib

my_email = "" #enter your own email
password = "" #enter your own generated password

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "HIZ95GJM94XFTDDN" #try using your own upi key

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "7670564a48ea4a71a30fd5df2ad12418" #try using your own upi key

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
# HINT 1: Think about using the Python Slice Operator

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
# HINT 1: Consider using a List Comprehension.

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

stock_parameters = {

    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": NEWS_API_KEY,
}
response1 = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_data = response1.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_closing = float(stock_data_list[0]["4. close"])
before_yesterday_closing = float(stock_data_list[1]["4. close"])

stock_diff = abs(float(yesterday_closing - before_yesterday_closing))
diff_percent = (stock_diff / yesterday_closing) * 100

if diff_percent > 5:
    response2 = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = response2.json()
    news_data_list = [value for (key, value) in news_data.items()]
    first_three = news_data_list[2][slice(3)]
    articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in first_three]

    with smtplib.SMTP("smtp.gmail.com", port=587) as connections:
        connections.starttls()
        connections.login(my_email, password)
        for article in articles:
            connections.sendmail(from_addr=my_email,
                                 to_addrs=my_email,
                                 msg=article)
