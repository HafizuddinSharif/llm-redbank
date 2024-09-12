import xmltodict
from xml.dom.minidom import parseString

from datetime import date
from datetime import datetime
import time


def extract_redflags(brn):
    print("extract_redflags:")

    try :
        file_name = 'ctos_data/full-' + brn + '-response.xml'
        #print(file_name)
        with open(file_name, 'r') as file:
            xml_content = file.read()
    except:
        return None

    redflags_data = {}
    xml_dict = xmltodict.parse(xml_content)

    # extract bankruptcy status
    bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['bankruptcy']
    bankruptcy_status = bankruptcy['@status']
    #print("bankruptcy_status: ", bankruptcy_status)
    if(int(bankruptcy_status) == 1):
        redflags_data['customer_bankruptcy_status'] = True
    else:
        redflags_data['customer_bankruptcy_status'] = False

    related_parties_bankruptcy = related_parties_bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['related_parties']['bankruptcy']
    related_parties_bankruptcy_status = related_parties_bankruptcy['@status']
    #print("related_parties_bankruptcy_status: ", related_parties_bankruptcy_status)
    if(int(related_parties_bankruptcy_status) == 1):
        redflags_data['customer_related_parties_bankruptcy_status'] = True
    else:
        redflags_data['customer_related_parties_bankruptcy_status'] = False

    # extract gearing ratio
    gear_accounts = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account']

    # Define the tags to extract
    gear_tags_to_extract = {
        'gear': 'Gearing Ratio'
    }

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

        for key, label in gear_tags_to_extract.items():
            
            if gear_accounts[i][key] is None:
                gear_accounts[i][key] = 0.0

            if int(currentYear) > latestYear:
                latestYear = int(currentYear)
                latestGearRatio = gear_accounts[i][key]

    #print("latestGearRatio:" , latestGearRatio , ", for latestYear:", latestYear)
    redflags_data['gearing_ratio'] = latestGearRatio

    ## extract profit_margin
    latestYear = 0
    latestProfitMargin = 0.0

    # Define the tags to extract
    profit_margin_tags_to_extract = {
        'profit_margin': 'Profit Margin'
    }

    accounts = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account']

    for i in range(totalNumberOfAccount):
        date = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account'][i]['pldd']
        #print("current date is: " + date)

        currentYear =  date[6:10]
        #print("current year is: " + currentYear)

        for key, label in profit_margin_tags_to_extract.items():
            
            if accounts[i][key] is None:
                accounts[i][key] = 0.0

            if int(currentYear) > latestYear:
                latestYear = int(currentYear)
                latestProfitMargin = accounts[i][key]

    #print("latestProfitMargin:" , latestProfitMargin , ", for latestYear:", latestYear)
    redflags_data['profit_margin'] = latestProfitMargin


    ## extract legal details
    legal = xml_dict['report']['enq_report']['enquiry']['section_ccris']['summary']['legal']

    legalStatus = legal['@status']
    #print("legal_status: " + legalStatus)

    if int(legalStatus) == 1:
        legal_accounts = xml_dict['report']['enq_report']['enquiry']['section_ccris']['accounts']['account']

        legal_tags_to_extract = {
            'legal': 'legal'
        }

        dictLen = len(legal_accounts)
        #print("dictlen = " + str(dictLen))
        #print(legal_accounts[1])

        for i in range(dictLen):
            for key, label in legal_tags_to_extract.items():
                legalTag = legal_accounts[i][key]
                #print("legalTag: " + str(legalTag))

                if 'name' in legalTag:
                    name = legalTag['name']
                    #print("name is found:" + name)
                    date = legalTag['date']
                    #print("date is found:" + date)

                    redflags_data['legal_status'] = legalStatus
                    redflags_data['legal_status_name'] = name
                    redflags_data['legal_status_date'] = date


    ## extract msic_ssm_code
    msic_ssm = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['msic_ssms']['msic_ssm']
    #print(str(msic_ssms))

    msic_ssm_code = msic_ssm['@code']
    redflags_data['msic_ssm_code'] = msic_ssm_code

    trexRef = xml_dict['report']['enq_report']['enquiry']['section_summary']['tr']['trex_ref']
    #print(str(trexRef))

    trexRefNegative = trexRef['@negative']
    trexRefPositive = trexRef['@positive']

    if trexRefNegative == '0' and trexRefPositive == '0':
        redflags_data['trex_status'] = False
    else:
        redflags_data['trex_status'] = True


    ## extract numOfDays
    
    registerDate = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['register_date']
    #print(str(registerDate))

    registerDateObj = datetime.strptime(registerDate, '%d-%m-%Y').date()
    #print(type(registerDateObj))
    #print(registerDateObj)  # printed in default format

    now = datetime.now()
    #print("now =", now)
    todayDate = now.strftime("%Y-%m-%d")
    #print("todayDate =", todayDate)

    #today = date.today()
    #print("Today's date:", today)

    numOfDays = days_between_dates(str(registerDateObj),str(todayDate))
    #print("age: ", numOfDays)
    redflags_data['age_of_company in days'] = numOfDays
    


    return redflags_data

def days_between_dates(dt1, dt2):
    date_format = "%Y-%m-%d"
    a = time.mktime(time.strptime(dt1, date_format))
    b = time.mktime(time.strptime(dt2, date_format))
    delta = b - a
    return int(delta / 86400)


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


    # To include redflags data into initial data submitted to chatbot
    # extract bankruptcy status
    bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['bankruptcy']
    bankruptcy_status = bankruptcy['@status']
    print("bankruptcy_status: ", bankruptcy_status)
    if(int(bankruptcy_status) == 1):
        extracted_data['customer_bankruptcy_status'] = True
    else:
        extracted_data['customer_bankruptcy_status'] = False

    related_parties_bankruptcy = related_parties_bankruptcy = xml_dict['report']['enq_report']['enquiry']['section_summary']['ctos']['related_parties']['bankruptcy']
    related_parties_bankruptcy_status = related_parties_bankruptcy['@status']
    print("related_parties_bankruptcy_status: ", related_parties_bankruptcy_status)
    if(int(related_parties_bankruptcy_status) == 1):
        extracted_data['customer_related_parties_bankruptcy_status'] = True
    else:
        extracted_data['customer_related_parties_bankruptcy_status'] = False


    legal = xml_dict['report']['enq_report']['enquiry']['section_ccris']['summary']['legal']

    legalStatus = legal['@status']
    print("legal_status: " + legalStatus)

    if int(legalStatus) == 1:
        legal_accounts = xml_dict['report']['enq_report']['enquiry']['section_ccris']['accounts']['account']

        legal_tags_to_extract = {
            'legal': 'legal'
        }

        dictLen = len(legal_accounts)
        #print("dictlen = " + str(dictLen))
        #print(legal_accounts[1])

        for i in range(dictLen):
            for key, label in legal_tags_to_extract.items():
                legalTag = legal_accounts[i][key]
                #print("legalTag: " + str(legalTag))

                if 'name' in legalTag:
                    name = legalTag['name']
                    #print("name is found:" + name)
                    date = legalTag['date']
                    #print("date is found:" + date)

                    extracted_data['legal_status'] = legalStatus
                    extracted_data['legal_status_name'] = name
                    extracted_data['legal_status_date'] = date
    
    msic_ssm = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['msic_ssms']['msic_ssm']
    #print(str(msic_ssms))

    msic_ssm_code = msic_ssm['@code']
    extracted_data['msic_ssm_code'] = msic_ssm_code

    trexRef = xml_dict['report']['enq_report']['enquiry']['section_summary']['tr']['trex_ref']
    #print(str(trexRef))

    trexRefNegative = trexRef['@negative']
    trexRefPositive = trexRef['@positive']

    if trexRefNegative == '0' and trexRefPositive == '0':
        extracted_data['trex_status'] = False
    else:
        extracted_data['trex_status'] = True


    ## extract numOfDays
    
    registerDate = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['register_date']
    print(str(registerDate))

    registerDateObj = datetime.strptime(registerDate, '%d-%m-%Y').date()
    #print(type(registerDateObj))
    print(registerDateObj)  # printed in default format

    now = datetime.now()
    #print("now =", now)
    todayDate = now.strftime("%Y-%m-%d")
    print("todayDate =", todayDate)

    #today = date.today()
    #print("Today's date:", today)

    numOfDays = days_between_dates(str(registerDateObj),str(todayDate))
    print("age: ", numOfDays)
    extracted_data['age_of_company in days'] = numOfDays

    return extracted_data