# Red Flags / redflags
| Name    | Customer is a red flag if the value | Description |
| -------- | ------- | ------ |
| **customer_bankruptcy_status**  | true    | The customer has a bankruptcy record |
| **customer_related_parties_bankruptcy_status**  | true    | The customer has related parties with a bankruptcy record |
| **gearing_ratio** | more than 50     | The customer has a very high gearing ratio of {gearing_ratio/100} |
| **profit_margin**    | less than -10    | The customer had a very poor profit margin of {profit_margin} |
| **legal_status** | 1 | The customer has records of legal proceedings. In particular, with regards to {legal_status_name} on {legal_status_date}
| **msic_ssm_code** | **refer to MSIC code table  | The customer that operates in a high-risk industry |
| **trex** | true | The customer has records of negative non-bank monthly payment(s) (such as, but not limited to: rental, telco and utilities bill payments) |
| **age_of_company** | less than 450 | The customer’s age is too young, at only {age_of_company} days old. |

## Bankruptcy status
If **customer_bankruptcy_status = true**, message is:
The customer has a bankruptcy record. Please perform your due diligence and proceed with caution.

If **customer_related_parties_bankruptcy_status = true** message is:
The customer has related parties with a bankruptcy record. Please perform your due diligence and proceed with caution.

If **customer_bankruptcy_status = true and customer_related_parties_bankruptcy_status = true**, message is:
The customer and its related parties have bankruptcy records. Please perform your due diligence and proceed with caution.

## Gearing Ratio

if **gearing_ratio > 50**, then message is:
The customer has a very high gearing ratio of <gear/100>. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports.

## Profit Margin
if **profit_margin < -10**, then message is:
The customer had a very poor profit margin of {profit_margin}. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports.

## Court Cases
If **legal_status != 0**, then message is:
The customer has records of legal proceedings. In particular, with regards to {legal_status_name} on {legal_status_date}

## MSIC Codes:
The customer that operates in a high-risk industry should be flagged:
| MSIC SSM Code | Description |
|---------------|-------------|
| 94920 | Activities of political organizations |
| 92000 | Gambling and betting activities |
| 84220 | Military and civil defence services |
| 73200 | Market research and public opinion polling |
| 63910 | News syndicate and news agency activities |
| 59120 | Motion picture, video and television programme postproduction activities |
| 59110 | Motion picture, video and television programme production activities |
| 52249 | Other cargo handling activities n.e.c. |
| 52241 | Stevedoring services |
| 47736 | Retail sale of household fuel oil, cooking gas, coal, and fuel wood |
| 46619 | Wholesale of other solid, liquid and gaseous fuels and related products n.e.c. |
| 43124 | Site preparation for mining |
| 30400 | Manufacture of military fighting vehicles |
| 28240 | Manufacture of mining machinery |
| 19201 | Manufacture of refined petroleum products |
| 19100 | Manufacture of coke oven products |
| 16291 | Manufacture of wood charcoal |
| 09900 | Support activities for mining and quarrying |
| 09101 | Oil and gas extraction service activities provided on a fee or contract basis |
| 08999 | Other mining and quarrying |
| 08996 | Mining of gemstones |
| 08995 | Mining of steatite (talc) |
| 08994 | Mining of natural graphite |
| 08993 | Mining of siliceous fossil meals |
| 08992 | Mining of asbestos |
| 08991 | Mining of abrasive materials |
| 08918 | Guano mining |
| 08917 | Mining of fluorspar and earth colours |
| 08916 | Mining of borates and kieserite |
| 08915 | Mining of barium sulphate and carbonate |
| 08913 | Mining of native sulphur |
| 08912 | Mining of natural potassium salts |
| 08911 | Mining of natural phosphates |
| 08108 | Mining of clays and kaolin |
| 08107 | Quarrying of sand |
| 08104 | Mining of chalk and dolomite |
| 08103 | Mining of gypsum and anhydrite |
| 07799 | Mining of other non-ferrous metals |
| 07797 | Mining of platinum |
| 07796 | Mining of silver |
| 07795 | Mining of gold |
| 07794 | Mining of ilmenite |
| 07793 | Mining of bauxite |
| 07792 | Mining of copper |
| 07791 | Mining of tin ores |
| 07721 | Mining of uranium and thorium |
| 07701 | Mining of iron ore |
| 07605 | Mining of hydrocarbon liquids |
| 06104 | Processes to obtain crude oils (decantation, desalting, dehydration, stabilization, etc.) |
| 06103 | Production of crude petroleum from bituminous shale and sand |
| 06101 | Extraction of crude petroleum oils |
| 05100 | Mining of hard coal |
| 05200 | Mining of lignite |
| 02203 | Production of charcoal in the forest (using traditional methods), collection of bark and firewood |

## TREX
Trex status is related to the records of non-bank monthly payment(s) or credit history such as but
not limited to rental, telecommunication bill and utilities bill payments. If trex_status is True, it
indicate a red flag or high risk indicators.

If **trex_status = true**, then message is:
The customer has records of negative non-bank monthly payment(s) (such as, but not limited to: rental, telco and utilities bill payments). As such, please perform due diligence.

## Age of Company in days

If **age_of_company < 450**, then message is:
The customer’s age is too young, at only {age_of_company} days old.

