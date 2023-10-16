import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_company_urls(session, soup):
    company_links = soup.find_all('td', class_='table__td table__td--big')
    company_urls = []

    for link in company_links:
        url = link.a['href']
        company_urls.append(url)
    return company_urls

async def get_company_data(session, company_url):
    base_url = "https://markets.businessinsider.com" + company_url
    html = await fetch_url(session, base_url)
    soup = BeautifulSoup(html, 'lxml')

    company_code = soup.find('span', class_='price-section__category').text.split()[-1]
    pe_ratio_div = soup.find('div', class_='snapshot__header', string='P/E Ratio')

    try:
        m = pe_ratio_div.find_parent('div', class_='snapshot__data-item').get_text(strip=True)
        match = re.search(r'[\d.]+', m)
        company_pe = float(match.group())
    except:
        company_pe = None

    return company_code, company_pe

async def main():
    start_time = time.time()
    url = "https://markets.businessinsider.com/index/components/s&p_500"

    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, url)
        soup = BeautifulSoup(html, 'lxml')

        company_urls = await get_company_urls(session, soup)
        company_data = await asyncio.gather(*(get_company_data(session, url) for url in company_urls))

        table = soup.find('table')
        table_data = []
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all(['th', 'td'])
                row_data = [column.text for column in columns]
                table_data.append(row_data)

        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        df = df.rename(columns=lambda x: x.strip())
        df['Latest Price\nPrevious Close'] = df['Latest Price\nPrevious Close'].str.replace('\t', '')

        company_names = df['Name']
        company_prices = df['Latest Price\nPrevious Close'].str.split('\n', expand=True)[1]
        company_growthes = df['1 Year\n+/-\n%'].str.split('\n', expand=True)[2]

        companies = []
        for i in range(len(company_names)):
            company = {
                "code": company_data[i][0],
                "name": company_names[i].replace('\n', ''),
                "price": float(company_prices[i].replace('$', '')),
                "P/E": float(company_data[i][1]) if company_data[i][1] else None,
                "growth": float(company_growthes[i].replace('%', '')) if company_growthes[i] else None,
            }
            companies.append(company)

        # Sorting
        companies_sorted_by_price = sorted(companies, key=lambda x: x["price"], reverse=True)
        companies_sorted_by_pe = sorted(companies, key=lambda x: x["P/E"] if x["P/E"] else float("inf"))
        companies_sorted_by_growth = sorted(companies, key=lambda x: x["growth"] if x["growth"] else float("-inf"),
                                            reverse=True)

        # Sorting top 10
        top_10_expensive = companies_sorted_by_price[:10]
        top_10_low_pe = companies_sorted_by_pe[:10]
        top_10_growth = companies_sorted_by_growth[:10]

        # JSON-files for top-10
        def save_to_json(filename, data):
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

        save_to_json("top_10_expensive.json", top_10_expensive)
        save_to_json("top_10_low_pe.json", top_10_low_pe)
        save_to_json("top_10_growth.json", top_10_growth)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Asyncio version takes {execution_time:.2f} seconds")


if __name__ == '__main__':
    asyncio.run(main())
