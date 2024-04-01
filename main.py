import aiohttp
import asyncio
import datetime
import sys

async def fetch_exchange_rate(session, date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}&exchange=&coursid=5"

    async with session.get(url) as response:
        return await response.json()

async def get_exchange_rates():
    async with aiohttp.ClientSession() as session:
        tasks = []
        today = datetime.date.today()
        for i in range(10):
            date = today - datetime.timedelta(days=i)
            tasks.append(fetch_exchange_rate(session, date))
        return await asyncio.gather(*tasks)

def print_exchange_rates(data):
    for rates in data:
        date = rates['date']
        eur_rate = next((x['saleRate'] for x in rates['exchangeRate'] if x['currency'] == 'EUR'), None)
        usd_rate = next((x['saleRate'] for x in rates['exchangeRate'] if x['currency'] == 'USD'), None)
        if eur_rate is not None and usd_rate is not None:
            print(f"On {date}: EUR rate - {eur_rate:.2f}, USD rate - {usd_rate:.2f}")
        else:
            print(f"On {date}: Data not available for EUR and USD")

async def main():
    try:
        data = await get_exchange_rates()
        print_exchange_rates(data)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, print stack trace:
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: python main.py")
    else:
        asyncio.run(main())
