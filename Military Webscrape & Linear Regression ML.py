import requests
import sys
def findNames(https):
    response = requests.get(https, timeout = 2)
    #print(f"response: {response.text}")
    print(type(response.text))

    sfnIndeces = []
    countryNames = []

    if response.status_code == 200:
        index = response.text.find('class="longFormName"')
        sfnIndeces.append(index)
        while index != -1:
            index = response.text.find('class="longFormName"', index+1)
            if index != -1:
                sfnIndeces.append(index)
        #print(sfnIndeces)
        for index in sfnIndeces:
            delimitor = response.text[index+93:index+200].find("<")
            countryNames.append(response.text[index+93:index+93+delimitor-20])
        return countryNames
    else:
        return []

#Power Index Scraping
powerIndexHTTPS = "https://www.globalfirepower.com/countries-listing.php"
response = requests.get(powerIndexHTTPS)
if len(findNames(powerIndexHTTPS)) == 0:
    print("There was an error in processing your https request (Country Names)")
    sys.exit()

if response.status_code == 200:
    powerIndeces = []
    pi_dict = {}
    index = response.text.find('class="pwrIndxContainer"')
    powerIndeces.append(response.text[index+84:index+90])
    while index != -1:
        index = response.text.find('class="pwrIndxContainer"', index+1)
        if index != -1:
            powerIndeces.append(float(response.text[index+84:index+90]))
    #print(powerIndeces)
    
    pi_dict = dict(zip(findNames(powerIndexHTTPS), powerIndeces))
    print(pi_dict)
else:
    print("There was an error processing your https request (Power Indeces)")

#Military Budget Scraping
militaryBudgetHTTPS = "https://www.globalfirepower.com/defense-spending-budget.php"
response = requests.get(militaryBudgetHTTPS)
if len(findNames(militaryBudgetHTTPS)) == 0:
    print("There was an error in processing your https request (Names: Power Index)")
    sys.exit()

if response.status_code == 200:
    militaryBudgets = []
    mb_dict = {}
    index = response.text.find('class="valueContainer"')
    delimiter = response.text[index+227: index+300].find(" ")
    number = response.text[index+227:index+227+delimiter]
    while number.find(",") != -1:
        number = number.replace("," , "")
    militaryBudgets.append(number)
    while index != -1:
        index = response.text.find('class="valueContainer"', index+1)
        delimiter = response.text[index+227: index+300].find(" ")
        number = response.text[index+227:index+227+delimiter]
        while number.find(",") != -1:
            number = number.replace("," , "")
        militaryBudgets.append(number)

    mb_dict = dict(zip(findNames(militaryBudgetHTTPS), militaryBudgets))
    print(mb_dict)
    print(index)
else:
    print("There was an error processing your https request (Military Budget)")