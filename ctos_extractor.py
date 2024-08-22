import xmltodict
from xml.dom.minidom import parseString

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
    print("find number of account: " + str(totalNumberOfAccount))

    for i in range(totalNumberOfAccount):
        date = xml_dict['report']['enq_report']['enquiry']['section_a']['record']['accounts']['account'][i]['pldd']
        print("current date is: " + date)

        currentYear =  date[6:10]
        print("current year is: " + currentYear)

        for key, label in tags_to_extract.items():
            
            if accounts[i][key] is None:
                accounts[i][key] = 0.0

            extracted_data[label + " in " + currentYear] = accounts[i][key]

    # Print the extracted data
    # for label, value in extracted_data.items():
    #     print(f"{label}: {value}")

    return extracted_data