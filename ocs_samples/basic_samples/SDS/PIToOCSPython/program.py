# This exercise is done in order to take the data from the OAKPI-SLTC01 data archive,
# and analyze them hour wise for 1 dayw wrt some parameters as to what and how much
# data each floor of the headquarters in San Leandro is using.

import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt 

# To get the data, make the connection
tokenEndpoint = "https://staging.osipi.com/identity/connect/token?"
clientId = "f37b6c6a-6236-4f24-ad83-d32224c3e533"
clientSecret = "U2tVI3yypXp+eBjcoiTjApvWeTnWyqJK0+sgAFg6DnY="

tokenInformation = requests.post(tokenEndpoint,
data = {"client_id" : clientId,
    "client_secret" : clientSecret,
    "grant_type" : "client_credentials"})

token = json.loads(tokenInformation.content)

header = { 'Authorization' : 'Bearer ' + token.get('access_token')}

url = 'https://staging.osipi.com/api/Tenants/1f11c599-be17-4812-a72f-00921b7716df/Namespaces/Julija/Streams'

omfURL = "https://staging.osipi.com/api/Tenants/1f11c599-be17-4812-a72f-00921b7716df/Namespaces/Julija/omf"

omfHeader = {'Authorization' : 'Bearer ' + token.get('access_token'), "omfversion" : "1.1", "messagetype" : "", "messageformat" : "json", "action" : "create", "Content-Type" : "application/json",
    "producertoken" : "b7CNvN36cq" }

# Method to get the data for different floors (maximum temperature, humiduty, CO2). We needed a better method name.
def singleDataPoint(startIndex, endIndex):
    timeWindow = '/Data?startIndex=' + str(startIndex) + '&endIndex=' + str(endIndex)
    humidityDataURL = '?query=name contains floor_*.humidity'

    # To store floor wise data
    f1 = {}
    f2 = {}
    f3 = {}
    f4 = {}
    f5 = {}
    f6 = {}

    r = requests.get(url+ humidityDataURL, headers=header)
    humidityList = r.json()

    # Timestamp start at the beginning of every hour, and all data (temp, humidity, co2 levels), will be aggregated for the whole hour, into one value (for each parameter) for one timestamp.
    # Timestamp 2019-05-28T00:00:00Z will have an averaged value of temp, humidity, co2 levels for the whole hour.
    f1['Timestamp'] = str(startIndex)
    f2['Timestamp'] = str(startIndex)
    f3['Timestamp'] = str(startIndex)
    f4['Timestamp'] = str(startIndex)
    f5['Timestamp'] = str(startIndex)
    f6['Timestamp'] = str(startIndex)

    # Get the humidity for all the floors
    i = 1
    while(i <= 6):
        for x in humidityList:
            final = []
            if (('Floor_' + str(i)) in x.get('Name')):
                if 'Average' in x.get('Name'):
                    r = requests.get(url + ('/') + x.get('Id') + timeWindow, headers=header)
                    hvals = r.json()
                    for val in hvals:
                        final.append(val.get('Value'))
                    if i == 1:
                        if len(final) != 0:
                            f1['Humidity'] = sum(final)/len(final)

                    if i == 2:
                        if len(final) != 0:
                            f2['Humidity'] = sum(final)/len(final)

                    if i == 3:
                        if len(final) != 0:                        
                            f3['Humidity'] = sum(final)/len(final)

                    if i == 4:
                        if len(final) != 0:
                            f4['Humidity'] = sum(final)/len(final)
                    
                    if i == 5:
                        if len(final) != 0:                      
                            f5['Humidity'] = sum(final)/len(final)

                    if i == 6:
                        if len(final) != 0:                        
                            f6['Humidity'] = sum(final)/len(final)

        i += 1

    # Get the CO2 for all the floors
    co2DataURL = '?query=name contains floor_*.co2'

    r = requests.get(url+ co2DataURL, headers=header)
    co2List = r.json()

    i = 1
    while(i <= 6):
        for x in co2List:
            final = []
            if (('Floor_' + str(i)) in x.get('Name')):
                r = requests.get(url + ('/') + x.get('Id') + timeWindow, headers=header)
                hvals = r.json()
                for val in hvals:
                    final.append(val.get('Value'))

                    if i == 1:
                        f1['CO2'] = sum(final)/len(final)

                    if i == 2:
                        f2['CO2'] = sum(final)/len(final)

                    if i == 3:
                        f3['CO2'] = sum(final)/len(final)

                    if i == 4:
                        f4['CO2'] = sum(final)/len(final)
                    
                    if i == 5:
                        f5['CO2'] = sum(final)/len(final)

                    if i == 6:
                        f6['CO2'] = sum(final)/len(final)

        i += 1        

    # Get the max temperature for all the floors
    tempDataURL = '?query=name contains *Temp_Max*'

    r = requests.get(url+ tempDataURL, headers=header)
    tempList = r.json()

    i = 1
    while(i <= 6):
        for x in tempList:
            final = []
            if (('Floor_' + str(i)) in x.get('Name')):
                r = requests.get(url + ('/') + x.get('Id') + timeWindow, headers=header)
                hvals = r.json()
                for val in hvals:
                    final.append(val.get('Value'))

                    if i == 1:
                        f1['MaxTemp'] = sum(final)/len(final)

                    if i == 2:
                        f2['MaxTemp'] = sum(final)/len(final)

                    if i == 3:
                        f3['MaxTemp'] = sum(final)/len(final)

                    if i == 4:
                        f4['MaxTemp'] = sum(final)/len(final)
                    
                    if i == 5:
                        f5['MaxTemp'] = sum(final)/len(final)

                    if i == 6:
                        f6['MaxTemp'] = sum(final)/len(final)

        i += 1
    
    dp = {'f1': f1, 'f2': f2, 'f3': f3,
            'f4': f4, 'f5': f5, 'f6': f6 }

    return dp

def main():
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    f6 = []

    # Get the data for the past 24 hours for a day (We can do this for any time  range of course)
    for i in range(0, 23):
        startIndex = datetime(2019, 5, 28, i, 0, 0)
        endIndex = datetime(2019, 5, 28, i+1, 0, 0)
        dp = singleDataPoint(startIndex, endIndex)
        f1.append(dp['f1'])
        f2.append(dp['f2'])
        f3.append(dp['f3'])
        f4.append(dp['f4'])
        f5.append(dp['f5'])
        f6.append(dp['f6'])

    # Calls to create a type, stream, and then finally send the data into the stream.
    typeID = createType()
    createStreams(typeID)
    sendData(f1, f2, f3, f4, f5, f6)

    showGraph(f1, f2, f3, f4, f5, f6, 'Humidity')
    showGraph(f1, f2, f3, f4, f5, f6, 'CO2')
    showGraph(f1, f2, f3, f4, f5, f6, 'MaxTemp')
    
# An explicit attempt to show graphs using Matplotlib library in Python (Not so efficient. Had time constraints)
def showGraph(f1, f2, f3, f4, f5, f6, yAXIS):
    listTimestamp = []
    listYAXIS = []

    for x in range(len(f1)):
        listTimestamp.append(f1[x].get('Timestamp'))
        listYAXIS.append(f1[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor1")

    listTimestamp = []
    listYAXIS = []

    for x in range(len(f2)):
        listTimestamp.append(f2[x].get('Timestamp'))
        listYAXIS.append(f2[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor2")

    listTimestamp = []
    listYAXIS = []

    for x in range(len(f3)):
        listTimestamp.append(f3[x].get('Timestamp'))
        listYAXIS.append(f3[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor3")

    listYAXIS = []
    listTimestamp = []

    for x in range(len(f4)):
        listTimestamp.append(f4[x].get('Timestamp'))
        listYAXIS.append(f4[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor4")

    listYAXIS = []
    listTimestamp = []

    for x in range(len(f5)):
        listTimestamp.append(f5[x].get('Timestamp'))
        listYAXIS.append(f5[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor5")

    listYAXIS = []
    listTimestamp = []

    for x in range(len(f6)):
        listTimestamp.append(f6[x].get('Timestamp'))
        listYAXIS.append(f6[x].get(yAXIS))

    plt.plot(listTimestamp, listYAXIS, label="Floor6")

    plt.xlabel('Timestamp')
    plt.ylabel(yAXIS)
    stri = 'Timestamp against '+ yAXIS + ' for 6 floors OSIsoft'
    plt.title(stri)
    plt.legend()
    plt.show()

# sending the actual data to OCS using OMF.
def sendData(f1, f2, f3, f4, f5, f6):

    omfHeader['messagetype'] = "data"

    # send the data floorwise to their respective containers (streams)
    data = [{
        "containerid": "Floor_1_Measurements",
        "values":  f1 },
        {
        "containerid": "Floor_2_Measurements",
        "values":  f2 },
        {
        "containerid": "Floor_3_Measurements",
        "values":  f3 },
        {
        "containerid": "Floor_4_Measurements",
        "values":  f4 },
        {
        "containerid": "Floor_5_Measurements",
        "values":  f5 },
        {
        "containerid": "Floor_6_Measurements",
        "values":  f6 
        }]

    r = requests.post(omfURL, json=data, headers=omfHeader)

    print(r.status_code)

# Self explanatory
def createStreams(type):
    omfHeader['messagetype'] = "container"

    data = [{
        "id": "Floor_1_Measurements",
        "typeid": "Floor"
        },
        {
                "id": "Floor_2_Measurements",
                "typeid": "Floor"
        },
        {
                "id": "Floor_3_Measurements",
                "typeid": "Floor"
        },
        {
                "id": "Floor_4_Measurements",
                "typeid": "Floor"
        },
        {
                "id": "Floor_5_Measurements",
                "typeid": "Floor"
        },
        {
                "id": "Floor_6_Measurements",
                "typeid": "Floor"
        }]

    r = requests.post(omfURL, json=data, headers=omfHeader)

# Create type in a structure as to what is there in the OCS. 
def createType():
    omfHeader['messagetype'] = "type"

    data1 = [{
        "id": "Floor",
        "classification": "dynamic",
        "type": "object",
        "properties": {
            "Timestamp": {
                "type": "string",
                "format": "date-time",
                "isindex": "true"
            },
            "Humidity": {
                "type": "number",
                "format": "float64",
                "isindex": "false"
            },
            "CO2": {
                "type": "number",
                "format": "float64",
                "isindex": "false"
            },
            "MaxTemp": {
                "type": "number",
                "format": "float64",
                "isindex": "false"
            }
        }
    }]

    r = requests.post(omfURL, json=data1 , headers=omfHeader)

    # return the typeId that will used to create streams of this type.
    return data1[0].get('id')

main()
