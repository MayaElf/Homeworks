import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time


def parse_company_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    company_code = soup.find('span', class_='price-section__category').text.split()[-1]
    pe_ratio_div = soup.find('div', class_='snapshot__header', string='P/E Ratio')

    try:
        m = pe_ratio_div.find_parent('div', class_='snapshot__data-item').get_text(strip=True)
        match = re.search(r'[\d.]+', m)
        company_pe = float(match.group())
    except:
        company_pe = None

    return {
        "code": company_code,
        "P/E": company_pe,
    }


def main():
    start_time = time.time()

    url = "https://markets.businessinsider.com/index/components/s&p_500"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    company_urls = []
    company_links = soup.find_all('td', class_='table__td table__td--big')

    for link in company_links:
        url = link.a['href']
        company_urls.append(url)

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

    company_data = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        for data in executor.map(parse_company_data,
                                 [f"https://markets.businessinsider.com{url}" for url in company_urls]):
            company_data.append(data)

    companies = []

    for i in range(len(company_names)):
        company = {
            "code": company_data[i]["code"],
            "name": company_names[i].replace('\n', ''),
            "price": float(company_prices[i].replace('$', '')),
            "P/E": float(company_data[i]["P/E"]) if company_data[i]["P/E"] else None,
            "growth": float(company_growthes[i].replace('%', '')) if company_growthes[i] else None,
        }
        companies.append(company)

    # Sorting by parameters
    companies_sorted_by_price = sorted(companies, key=lambda x: x["price"], reverse=True)
    companies_sorted_by_pe = sorted(companies, key=lambda x: x["P/E"] if x["P/E"] else float("inf"))
    companies_sorted_by_growth = sorted(companies, key=lambda x: x["growth"] if x["growth"] else float("-inf"),
                                        reverse=True)

    # Top-10 from sorted list
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
    print(f"Multithread version takes {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()
