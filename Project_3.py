"""
Projekt_3.py: druhý projekt do Engeto Online Python Akademie
author: Jan Kašpárek
email: jan.kasparek96@gmail.com
discord: jankasparek0720
"""

import requests
from bs4 import BeautifulSoup
import argparse
import csv
from pprint import pprint

# Create a arguments for input 
def arguments_parse():
    parse_arg = argparse.ArgumentParser(description="URL input")
    parse_arg.add_argument("web", metavar="web", type=str, help="Enter url")
    parse_arg.add_argument("file_name", metavar="file_name", type=str, help="Enter file name")
    args = parse_arg.parse_args()
    # 1st argument 
    web = args.web
    # 2nd argument 
    file_name = args.file_name
    return web , file_name

# row atributes for getting correct "td" data  
def row_atr(tr_tag):
    return {
        "Number": tr_tag[0].getText(),
        "Name": tr_tag[1].getText(),
    }
# row atributes for getting correct "td" data 
def row_atr_table_region(tr_tag):
    return {
    "Voters in the list": tr_tag[3].getText(),
    "Issued envelopes": tr_tag[4].getText(),
    "Valid votes": tr_tag[7].getText(),
}
# row atributes for getting correct "td" data 
def row_atr_table_parties(tr_tag):
    return {
    tr_tag[1].getText():tr_tag[2].getText(),    
}

def url_soup():
    web, _ = arguments_parse() # Getting argument for web page 
    url_response = requests.get(web) #gets url 
    soup = BeautifulSoup(url_response.text, 'html.parser') #def of soup
    container = soup.find("div", {"id": "container"}) #taking all web container
    tr_all = container.find_all("tr") # from it find all "tr" attributes
    return tr_all

def tr_area():
    list_links = [] #List for saving all links to a next page to scrape region and party data
    list_area = [] #List for scraped data of all city/villiges names and numbers

    # all scraped tr from url_soup
    for tr in url_soup():
        td_row = tr.find_all("td") #finds all "td" in every "tr" 
        td_number = tr.find_all("td",{"class": "cislo"}) #we need "td" data with class:cislo 
        if td_number: #if yes we have correct data for scraping, becouse some "td" were hidden or empty 
            data = row_atr(td_row) # from every td take define tags 
            list_area.append(data) # append data to list
            find_a = td_row[0].find("a") # in first "td", find attribute "a" 
            if find_a == None:
                continue
            else:
                href = td_row[0].find("a")["href"] # attribute "a", has "href" where is store link to the next page with specigic data for that city
            list_links.append("https://volby.cz/pls/ps2017nss/"+href) # merge the link with prefix to and save to a list
    return list_area, list_links

def links_url():
    _ , list_links = tr_area() # take list_links from tr_area()
    list_data = [] #list for scraped data
    
    # go through all links in the list 
    for url_r in list_links: 
        dict_data = {} #for data save 

        url_r_response = requests.get(url_r) #gets url from list 
        soup1 = BeautifulSoup(url_r_response.text, 'html.parser') #def of soup
        container = soup1.find("div", {"id": "container"}) #taking all web container
        all_tr = container.find_all("tr") # from it find all "tr" attributes
        
        # for scraping data as number of voters, issued envelopes atd 
        def tr_region():
            for data in all_tr[2:3]: # we dont need scrape everything just "tr" 2 and 3 on each pageg
                td_row_region = data.find_all("td") # find all "td" in every "tr" 
                data_region = row_atr_table_region(td_row_region) # from every td take define tags 
                for key in data_region: #some of these scrape data had special symbols, which been removed 
                    value = data_region.get(key) #from key we get item 
                    value = value.replace("\xa0","").strip() #strip the special symbols from item 
                    dict_data.update({key:value}) # save the data to dict 
        tr_region()
            
        def tr_party():
            for tr_parties in all_tr[3:]: # we dont need scrape everything just data "tr" from 3 to end on each pageg
                td_row_parties = tr_parties.find_all("td") # find all "td" in every "tr"
                td_number = tr_parties.find_all("td",{"class": "cislo"}) #we need "td" data with class:cislo 
                if td_number: #if yes we have correct data for scraping, becouse some "td" were hidden or empty 
                    data_parties = row_atr_table_parties(td_row_parties) # from every td take define tags
                    for key in data_parties: #some of these scrape data had special symbols, which been removed 
                        value = data_parties.get(key) #from key we get item 
                        value = value.replace("\xa0","").strip() #strip the special symbols from item 
                        dict_data.update({key:value}) #update dict 
            list_data.append(dict_data) #update dict to the list, becouse we have same keys on every page we cannot used dict for all, the data in dict will be rewritten so its need to be stored in list 
        tr_party()
    pprint(list_data)
    return list_data       

def append_data():
    # passing list  
    list_area, _  = tr_area() 
    list_data = links_url()
    full_list = []
    
    # merging together data from list to one 
    for i, j in zip(list_area, list_data): 
        combine_dict = {**i, **j} # combine dicts inside the lists into one dict 
        full_list.append(combine_dict) #and crating one big list with all data 
    return full_list   
        
def create_excell():
    # passing variables
    web, file_name = arguments_parse()
    full_list = append_data()
    # creating file as used argument 2 
    csv_filename = file_name
    # keys are all the same so we just using keys from first dict as header
    field_names = full_list[0].keys()

    # creating csv
    with open(csv_filename, "w", newline='', encoding="utf-8-sig") as new_csv_file:
        writer = csv.DictWriter(new_csv_file, fieldnames=field_names, delimiter=";")
        writer.writeheader()
        writer.writerows(full_list)
    print("-"*50)
    print("Data scraped from: ", web, "And saved to:" , csv_filename)
    print("Program closed!")
    print("-"*50)

if __name__ == "__main__":
    create_excell()
