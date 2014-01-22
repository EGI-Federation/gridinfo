#!/usr/bin/python
#
# Library to interact with GGUS creating and retrieving tickets
#
################################################################

import suds
import logging
import datetime

#logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.CRITICAL)

#################################################
# Create a connection
#################################################

def connect(type):

    if ( type == "test"):
        ################# Testing Instance ######################################
        user_name = "generic_test"
        passwd = "G1n1ric_T1st"
        wsdl_url = "https://train-ars.ggus.eu/arsys/WSDL/public/train-ars/GGUS"
    elif (type == "production"):
        ################# Production Instance ###############################
        user_name = "genac"
        passwd = "Sp6C!M8g"
        wsdl_url = "https://prod-ars.ggus.eu/arsys/WSDL/public/prod-ars/GGUS"

    client= suds.client.Client(url=wsdl_url,faults=False)
    token = client.factory.create("s0:AuthenticationInfo")
    token.userName = user_name
    token.password = passwd
    client.set_options(soapheaders=token) 
    return client

#################################################
# List a ticket
#################################################
def list_ticket (client, site_name, description):

    params = client.factory.create("s0:InputMapping6")
    params.Qualification = "'GHD_Affected Site'=\"%s\" AND \
                            'GHD_Short Description'=\"%s\"  AND \
                            'GHD_Meta Status'=\"Open\"" % (site_name, description)

    try:
        result = client.service.TicketGetList(params.Qualification)
        if ( result[0] == 200):
            return result[1][0]['GHD_Request_ID']
        else:
            return "None"
    except suds.WebFault, e:
        return "Failed to contact GGUS"

#################################################
# Create a ticket
#################################################
def create_ticket (client, site_name, long_description, mail, loginname, name, priority, description,\
                   last_modifier, last_login, carbon_copy):

    today=datetime.date.today()
    params = client.factory.create("s0:InputMapping7")

    params.GHD_Date_Time_Of_Problem = today
    params.GHD_Description = long_description
    params.GHD_Submitter_Mail = mail
    params.GHD_Internal_Diary = None
    params.GHD_Loginname = loginname
    params.GHD_Name = name
    params.GHD_Origin_ID = None
    params.GHD_Priority = priority
    params.GHD_Responsible_Unit = None
    params.GHD_Short_Description = description
    params.GHD_Status = 'assigned'
    params.GHD_Type_Of_Problem = 'Information System'
    params.GHD_Last_Modifier = last_modifier
    params.GHD_Last_Login = last_login
    params.GHD_Origin_SG = None
    params.GHD_CarbonCopy = carbon_copy
    params.GHD_Affected_Site = site_name
    params.GHD_Affected_VO = None
    params.GHD_Phone = None
    params.GHD_Related_Issue = None
    params.GHD_Public_Diary = None

    try:
        result = client.service.TicketCreate(params.GHD_Date_Time_Of_Problem, params.GHD_Description, \
                                             params.GHD_Submitter_Mail, \
                                             params.GHD_Internal_Diary, params.GHD_Loginname, params.GHD_Name, \
                                             params.GHD_Origin_ID, params.GHD_Priority, params.GHD_Responsible_Unit, \
                                             params.GHD_Short_Description, params.GHD_Status, params.GHD_Type_Of_Problem, \
                                             params.GHD_Last_Modifier, params.GHD_Last_Login, params.GHD_Origin_SG, \
                                             params.GHD_CarbonCopy, params.GHD_Affected_Site, params.GHD_Affected_VO, \
                                             params.GHD_Phone, params.GHD_Related_Issue, params.GHD_Public_Diary)
        if ( result[0] == 200):
            return result[1]
        else:
            return "GGUS ticket failed to be created"
    except suds.WebFault, e:
        return "Failed to contact GGUS"

