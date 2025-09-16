import pandas as pd
import requests

#THIS REPORT PULLS DATA FROM MOODLE VIA API AND COMBINES IT INTO A SINGLE DATAFRAME
#IT CHANGES TENANT FOR EACH ITERATION AND PULLS THE SAME REPORT FOR EACH TENANT

REPORT_ID = '12345' # ID FOR THE REPORT TO PULL FROM MOODLE. THIS CAN BE FOUND IN THE URL WHEN VIEWING THE REPORT IN MOODLE.
BASEURL = "https://yourmoodlesite.no" # BASE URL FOR YOUR MOODLE SITE. CHANGE TO YOUR MOODLE SITE.
API_TOKEN = "your_api_token" # API TOKEN FOR MOODLE. CHANGE TO YOUR API TOKEN.
USERID = '123456' # USER ID FOR THE USER TO CHANGE TENANTS FOR. CHANGE TO YOUR USER ID IF YOU HAVE MULTIPLE TENANTS.
change_tenants = False # SET TO TRUE IF YOU WANT TO CHANGE TENANTS. OTHERWISE, SET TO FALSE.
#-----------------------------------------------------------------------------------------------------#
#                       DO NOT CHANGE ANYTHING BELOW THIS LINE                                        #
#-----------------------------------------------------------------------------------------------------#

URL = BASEURL + "/webservice/rest/server.php?wstoken=" + API_TOKEN  # DO NOT CHANGE. THIS.


# Tenant information
def retrieve_tenants(): 
    web_data = requests.post(URL, data={
    'moodlewsrestformat': 'json',
    'wsfunction': 'tool_tenant_get_tenants',
    })
    if web_data.status_code == 200:
        print("Data fetched successfully.")
        return web_data
    else: 
        print("Something went wrong")
        exit()

# Change tenant
def change_tenants(tenantId): 
    web_data = requests.post(URL, data={
    'moodlewsrestformat': 'json',
    'wsfunction': 'tool_tenant_allocate_users',
    'allocations[0][userid]': USERID,
    'allocations[0][tenantid]': tenantId
    })
    if web_data.status_code == 200:
        if(web_data.text.find('"successcount":1') > -1):
            print("Tenant changed successfully.")
            return web_data
        else: 
            print('API ran, but something went wrong with changing the tenant')
    else: 
        print("Something went wrong")
        exit()



# Retrieve report
def retrieve_report(): 
    web_data = requests.post(URL, data={
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_reportbuilder_retrieve_report',
        'reportid': REPORT_ID,
        'perpage': '500000'
    })
    if web_data.status_code == 200:
        print("Data fetched successfully.")
        return web_data
    else: 
        print("Something went wrong")
        exit()

tenant_data = retrieve_tenants()
rows = []
for tenant in tenant_data.json():
    # print('Changing tenant: ' + tenant['name'])
    if change_tenants:
        change_tenants(tenant['id'])
    # print('Retrieving report...')
    report_data = retrieve_report()
    raw_data = report_data.json()["data"]
    rows = rows + raw_data["rows"]

headers = raw_data["headers"]
print(len(rows))

df = pd.DataFrame([row["columns"] for row in rows], columns=headers)
print(df)