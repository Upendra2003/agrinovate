import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import mplcyberpunk
import matplotlib
matplotlib.use('Agg')

plt.style.use("cyberpunk")

def fetch_data(day_offset):
    state_code = 'UP'
    state = 'Uttar+Pradesh'
    district = 'Pratapgarh'
    district_code = '61'
    market_code = '686'
    market = 'Pratapgarh'
    crop = 'Wheat'
    crop_code = '1'
    today = datetime.today()
    date = today - timedelta(days=day_offset)
    formatted_date = date.strftime("%d-%b-%Y")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
    }
    url = f'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity={crop_code}&Tx_State={state_code}&Tx_District={district_code}&Tx_Market={market_code}&DateFrom={formatted_date}&DateTo={formatted_date}&Fr_Date={formatted_date}&To_Date={formatted_date}&Tx_Trend=0&Tx_CommodityHead={crop}&Tx_StateHead={state}&Tx_DistrictHead={district}&Tx_MarketHead={district}'
    webpage = requests.get(url, headers=headers).text
    soup = BeautifulSoup(webpage, 'html.parser')
    min_price = max_price = None
    if soup.find_all('td')[0].text.strip() != 'No Data Found':
        min_price = soup.find_all('td')[6].text.strip()
        max_price = soup.find_all('td')[7].text.strip()
    return formatted_date, min_price, max_price

def create_plot():
        
    

    # Create a list of dates for the past 7 days
    dates = [datetime.today() - timedelta(days=i) for i in range(7)]

    # Fetch data in parallel
    date = []
    min_price = []
    max_price = []

    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = [executor.submit(fetch_data, i) for i in range(7)]
        results = [future.result() for future in as_completed(futures)]

    # Ensure results are in the order of dates
    results.sort(key=lambda x: datetime.strptime(x[0], "%d-%b-%Y"))

    # Unpack sorted results
    date, min_price, max_price = zip(*results)

    # Fill missing data with previous day's values
    min_price_filled = [min_price[0]]
    max_price_filled = [max_price[0]]

    for i in range(1, len(min_price)):
        min_price_filled.append(min_price[i] if min_price[i] is not None else min_price_filled[-1])
        max_price_filled.append(max_price[i] if max_price[i] is not None else max_price_filled[-1])

    dates_num = range(len(date))  # Use index positions for simplicity

    plt.figure(figsize=(10, 5))

    # Plot data
    plt.plot(dates_num, min_price_filled, label='Min Price', color='blue', marker='o')
    plt.plot(dates_num, max_price_filled, label='Max Price', color='red', marker='o')

    # Mark price at each point
    plt.scatter(dates_num, min_price_filled, color='blue')
    plt.scatter(dates_num, max_price_filled, color='red')
    
    # Add labels to each point
    for i in range(len(dates)):
        plt.text(dates_num[i], min_price_filled[i], str(min_price_filled[i]), color='blue', ha='right', va='bottom')
        plt.text(dates_num[i], max_price_filled[i], str(max_price_filled[i]), color='red', ha='right', va='bottom')

    # Add legend
    plt.legend()

    # Remove axes and title
    plt.axis('off')  # Remove axes

    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    
    # Encode the image in base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    plt.close()  # Close the plot to free memory
   
    return {'plot': img_base64 , 'min_price' : min_price_filled[len(date)-1] , 'max_price' : max_price_filled[len(date)-1]}


