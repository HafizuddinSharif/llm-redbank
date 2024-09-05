import xmltodict
from xml.dom.minidom import parseString
from datetime import datetime
from datetime import date
import time

xmlDictWithBrn = {}

def extract_bankruptcy_status(brn):
    #print("Call extract_bankruptcy_status with brn:" + brn)
    
    xml_dict = xmlDictWithBrn[brn]
    bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['bankruptcy']
    #print("bankruptcy status = " + bankruptcy)
    for label, value in bankruptcy.items():
        #print(f"{label}: {value}")
        bankruptcy_status = value
        #print("bankruptcy status = " + bankruptcy_status)

    return bankruptcy_status
    
    
def extract_related_parties_bankruptcy(brn):
    #print("Call extract_related_parties_bankruptcy with brn:" + brn)

    xml_dict = xmlDictWithBrn[brn]
    related_parties_bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['related_parties']['bankruptcy']
    for label, value in related_parties_bankruptcy.items():
        #print(f"{label}: {value}")
        related_parties_bankruptcy_status = value
        #print("related_parties_bankruptcy_status = " + related_parties_bankruptcy_status)

    return related_parties_bankruptcy_status

def extract_gear_ratio(brn):
    #print("Call extract_related_parties_bankruptcy with brn:" + brn)

    try :
        file_name = 'ctos_data/full-' + brn + '-response.xml'
        print(file_name)
        with open(file_name, 'r') as file:
            xml_content = file.read()
    except:
        return None
    
    xml_dict = xmltodict.parse(xml_content)
    accounts = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account']

    # Define the tags to extract
    tags_to_extract = {
        'gear': 'Gearing Ratio'
    }

    # Extract and print the values
    dom = parseString(xml_content)
    totalNumberOfAccount = int(len(dom.getElementsByTagName('account')) / 2)
    #print("find number of account: " + str(totalNumberOfAccount))

    latestYear = 0
    latestGearRatio = 0.0

    for i in range(totalNumberOfAccount):
        date = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account'][i]['pldd']
        #print("current date is: " + date)

        currentYear =  date[6:10]
        #print("current year is: " + currentYear)

        for key, label in tags_to_extract.items():
            
            if accounts[i][key] is None:
                accounts[i][key] = 0.0

            if int(currentYear) > latestYear:
                latestYear = int(currentYear)
                latestGearRatio = accounts[i][key]
                #print("latestGearRatio found: " + latestGearRatio)
        
    return latestGearRatio

def extract_profit_margin(brn):
    #print("Call extract_profit_margin with brn:" + brn)

    try :
        file_name = 'ctos_data/full-' + brn + '-response.xml'
        print(file_name)
        with open(file_name, 'r') as file:
            xml_content = file.read()
    except:
        return None
    
    xml_dict = xmltodict.parse(xml_content)
    
    accounts = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account']

    # Define the tags to extract
    tags_to_extract = {
        'profit_margin': 'Profit Margin'
    }

    # Extract and print the values
    dom = parseString(xml_content)
    totalNumberOfAccount = int(len(dom.getElementsByTagName('account')) / 2)
    #print("find number of account: " + str(totalNumberOfAccount))

    latestYear = 0
    latestProfitMargin = 0.0

    for i in range(totalNumberOfAccount):
        date = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account'][i]['pldd']
        #print("current date is: " + date)

        currentYear =  date[6:10]
        #print("current year is: " + currentYear)

        for key, label in tags_to_extract.items():
            
            if accounts[i][key] is None:
                accounts[i][key] = 0.0

            if int(currentYear) > latestYear:
                latestYear = int(currentYear)
                latestProfitMargin = accounts[i][key]
                #print("latestProfitMargin found: " + latestProfitMargin)

    return latestProfitMargin

def extract_legal_status(brn):
    #print("Call extract_legal_status with brn:" + brn)

    xml_dict = xmlDictWithBrn[brn]
    legal = xml_dict['report']['enq_report']['enquiry']['section_ccris']['summary']['legal']

    legalStatus = legal['@status']
    #print("legal_status: " + legalStatus)

    if int(legalStatus) == 1:
        accounts = xml_dict['report']['enq_report']['enquiry']['section_ccris']['accounts']['account']

        tags_to_extract = {
            'legal': 'legal'
        }

        dictLen = len(accounts)
        #print("dictlen = " + str(dictLen))
        #print(accounts[1])

        for i in range(dictLen):
            for key, label in tags_to_extract.items():
                legalTag = accounts[i][key]
                #print("legalTag: " + str(legalTag))

                if 'name' in legalTag:
                    name = legalTag['name']
                    #print("name is found:" + name)
                    date = legalTag['date']
                    #print("date is found:" + date)
                    return {'legalStatus':legalStatus,'name':name,'date':date}
                else:
                    print("no name tag, skip")
                    break
    else:
        print("legal status not 1")
        return {0}

def extract_msic_codes(brn):
    #print("Call extract_msic_codes with brn:" + brn)
    xml_dict = xmlDictWithBrn[brn]
    msic_ssms = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['msic_ssms']['msic_ssm']
    #print(str(msic_ssms))

    msic_code = msic_ssms['@code']
    #print(msic_code)

    return (msic_code)   

def extract_trex(brn):
    #print("Call extract_trex with brn:" + brn)

    xml_dict = xmlDictWithBrn[brn]
    trexRef = xml_dict['report']['enq_report']['enquiry']['section_summary']['tr']['trex_ref']
    #print(str(trexRef))

    trexRefNegative = trexRef['@negative']
    trexRefPositive = trexRef['@positive']
    #print("negative: " +  trexRefNegative + ", positive: " + trexRefPositive)

    if trexRefNegative == '0' and trexRefPositive == '0':
        return(0)
    else:
        return(1)
    
def extract_age_of_company(brn):
    #print("Call extract_age_of_company with brn:" + brn)

    xml_dict = xmlDictWithBrn[brn]
    registerDate = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['register_date']
    #print(str(registerDate))

    registerDateObj = datetime.strptime(registerDate, '%d-%m-%Y').date()
    #print(type(registerDateObj))
    #print(registerDateObj)  # printed in default format

    today = date.today()  
    #print("Today date is: ", today)

    numOfDays = days_between_dates(str(registerDateObj),str(today))
    #print("age: ", numOfDays)

    return(numOfDays)


def days_between_dates(dt1, dt2):
    date_format = "%Y-%m-%d"
    a = time.mktime(time.strptime(dt1, date_format))
    b = time.mktime(time.strptime(dt2, date_format))
    delta = b - a
    return int(delta / 86400)

def storeXmlDict(brn):
    print("Calling storeXmlDict with brn: ", brn)
    try :
        file_name = 'ctos_data/full-' + brn + '-response.xml'
        print(file_name)
        with open(file_name, 'r') as file:
            xml_content = file.read()
    except:
        return None

    xml_dict = xmltodict.parse(xml_content)

    if brn not in xmlDictWithBrn:
        xmlDictWithBrn.update({brn:xml_dict})

    #print(xmlDictWithBrn)
    for x in xmlDictWithBrn:
        print(xmlDictWithBrn[x])


def extract_xml(brn):
    try :
        file_name = 'ctos_data/full-' + brn + '-response.xml'
        print(file_name)
        with open(file_name, 'r') as file:
            xml_content = file.read()
    except:
        return None

    xml_dict = xmltodict.parse(xml_content)
    accounts = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account']

    # Define the tags to extract
    tags_to_extract = {
        'turnover': 'Total Revenue',
        'plnpbt': 'Profit Before Tax',
        'plnpat': 'Profit After Tax',
        'turnover_growth': 'Revenue Growth',
        'profit_margin': 'Profit Margin',
        'return_on_equity': 'ROE',
        'currat': 'Current Ratio',
        'workcap': 'Working Capital',
        'gear': 'Gearing Ratio',
        'networth': 'Net Worth',
        'totass': 'Total Asset'
    }

    # Extract and print the values
    extracted_data = {}
    '''
    for key, label in tags_to_extract.items():
        # element = root.find(f".//{key}")
        element = accounts[0][key]
        if element is not None:
            extracted_data[label] = element
        else:
            extracted_data[label] = None
    '''

    dom = parseString(xml_content)
    totalNumberOfAccount = int(len(dom.getElementsByTagName('account')) / 2)
    #print("find number of account: " + str(totalNumberOfAccount))

    for i in range(totalNumberOfAccount):
        date = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account'][i]['pldd']
        #print("current date is: " + date)

        currentYear =  date[6:10]
        #print("current year is: " + currentYear)

        for key, label in tags_to_extract.items():
            
            if accounts[i][key] is None:
                accounts[i][key] = 0.0

            extracted_data[label + " in " + currentYear] = accounts[i][key]

    # Print the extracted data
    # for label, value in extracted_data.items():
    #     print(f"{label}: {value}")

    return extracted_data