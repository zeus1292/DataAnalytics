import requests
from bs4 import BeautifulSoup

def get_us_sector_performance():
    output_list = list()
    url = "https://eresearch.fidelity.com/eresearch/goto/markets_sectors/landing.jhtml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            None
        else:
            print("Failure")
    except:
        print("Something went wrong")
        return output_list
    results_page=BeautifulSoup(response.content,'lxml')
    all_a_tags = results_page.find_all('a',class_="heading1")
    for i in all_a_tags:
        row = list()
        row.append(i.get_text())
        base_url = "https://eresearch.fidelity.com"
        link = base_url+i.get('href')
        a = get_sector_change_and_market_cap(base_url+i.get('href'))
        if a == None:
            return None
        else:
            row.extend(list(a))
            row.append(link)
            output_list.append(tuple(row))
    output_list.sort(key=lambda x:x[3],reverse=True)
    return output_list

def get_sector_change_and_market_cap(sector_page_link):
    s_response=requests.get(sector_page_link)
    if s_response.status_code == 200:
            None
    else:
            print("There is a problem with the request")
            return None
    sector_response = BeautifulSoup(s_response.content,'lxml')
    all_table_tags = sector_response.find_all('table', class_="snapshot-data-tbl")
    for i in all_table_tags:
        all_span_class = i.find_all("span")
        try:
            sector_change=float(all_span_class[1].get_text()[:-1])
        except:
            sector_change=0.00
        try:
            sector_market_cap=all_span_class[3].get_text()
        except:
            sector_market_cap="0.00"
        try:    
            sector_market_weight=float(all_span_class[5].get_text()[:-1])
        except:
            sector_market_weight=0.00
    return sector_change,sector_market_cap,sector_market_weight

#Test get_sector_change_and_market_cap()
link = "https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=25"
get_sector_change_and_market_cap(link)

#Should return (-0.40, $3.58T, 6.80)