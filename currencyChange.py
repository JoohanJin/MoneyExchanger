import os
import requests
from bs4 import BeautifulSoup


def getting_data(url = ""):
    all_list = []
    countries = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"class": "table table-bordered downloads tablesorter"})
    table_body = table.find("tbody")
    table_tr = table_body.find_all("tr")
    for i in table_tr:
        all_list.append(i.text.strip())
    return all_list

def getting_country(url = ""):
    all_list= getting_data(url)
    countries = []
    for i in all_list:
        if i.split("\n")[1] != "No universal currency":
            countries.append(i.split("\n")[0])
    for i in range(len(countries)):
        countries[i] = countries[i].lower()
    for i in range(len(countries)):
        string = countries[i][1:]
        countries[i] = countries[i][0].upper()+string
    return countries


def getting_currency(url = ""):
    all_list= getting_data(url)
    currencies = []
    for i in all_list:
        if i.split("\n")[1] != "No universal currency":
            currencies.append(i.split("\n")[2])
    return currencies

def choose_origin():
  print("Where are you from? Choose a country by number.")
  code = input("#: ")
  while not code.isdigit() or not int(code) in range(len(countries)):
    if not code.isdigit():
        print("That wasn't a number.")
    elif code not in range(len(countries)):
        print("Choose a number from the list.")
    code = input("#: ")
  return int(code)

def choose_converted():
  print("Now choose another country.")
  code = input("#: ")
  while not code.isdigit() or not int(code) in range(len(countries)):
    if not code.isdigit():
        print("That wasn't a number.")
    elif code not in range(len(countries)):
        print("Choose a number from the list.")
    code = input("#: ")
  return int(code)

def get_amount(code_from, code_to):
    print(f"How many {currencies[code_from]} do you want to convert to {currencies[code_to]}?")
    amount = input()
    while not amount.isdigit():
        print("That wasn't a number.")
        amount = input()
    return amount

def converter(money, currency_from, currency_to):
    converter_url = f"https://transferwise.com/gb/currency-converter/{currency_from}-to-{currency_to}-rate?amount={money}"
    money_request = requests.get(converter_url)
    soup = BeautifulSoup(money_request.text, "html.parser")
    rate = soup.find("div", {"class": "js-Calculator cc__header cc__header-spacing card card--with-shadow m-b-5"}).find("form").find("input")["value"]
    rate = float(rate)
    return rate * float(money)


os.system("clear")
url = "https://www.iban.com/currency-codes"
countries = getting_country(url)
currencies = getting_currency(url)
for i in range(len(countries)):
    print(f"# {i} {countries[i]}")
code_from = choose_origin()
print(countries[code_from])
code_to = choose_converted()
print(countries[code_to])

money = get_amount(code_from, code_to)
converted = converter(money, currencies[code_from], currencies[code_to])
print(f"{money} is {converted}")
