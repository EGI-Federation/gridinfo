#
#
# Library to interact with GGUS
#
##########################################

import ggus_suds
import ggus_templates

def ggus_monitor ( site_name, template, results, extra_condition, ggus_instance ):

    client_prod=ggus_suds.connect(ggus_instance)
    ggus_out=ggus_suds.list_ticket(client_prod,site_name,ggus_templates.templates[template]['description'])
    if ( ggus_out == "Unable to contact GGUS" ):
        ggus_color = "grey"
        ggus_result = "Unreachable"
        ggus_file_url = "None"
    elif ( ggus_out == "None" ):
        # The extra condition double checks whether a site still needs to get a GGUS ticket  
        if ( extra_condition ):
            ggus_color = "orange"
            client_test=ggus_suds.connect(ggus_instance)
            complete_description = ggus_templates.templates [template]['long_description'] + results
            ggus_out=ggus_suds.create_ticket(client_test,site_name, \
                                             complete_description,
                                             ggus_templates.templates[template]['mail'],
                                             ggus_templates.templates[template]['loginname'],
                                             ggus_templates.templates[template]['name'],
                                             ggus_templates.templates[template]['priority'],
                                             ggus_templates.templates[template]['description'],
                                             ggus_templates.templates[template]['last_modifier'],
                                             ggus_templates.templates[template]['last_login'],
                                             ggus_templates.templates[template]['carbon_copy'])
            ggus_result = ggus_out
            if (ggus_out == "GGUS ticket failed to be created"):
                ggus_file_url = "None"
            else:
                if (ggus_instance == "test"):
                    ggus_file_url = "https://train.ggus.eu/ws/ticket_info.php?ticket=%s" % (ggus_result)
                elif (ggus_instance == "prod"):
                    ggus_file_url = "https://ggus.eu/ws/ticket_info.php?ticket=%s" % (ggus_result)
        else:
            ggus_color = "green"
            ggus_result = "None"
            ggus_file_url = "None"
    else:
        ggus_color = "red"
        ggus_result = ggus_out
        if (ggus_instance == "test"):
            ggus_file_url = "https://train.ggus.eu/ws/ticket_info.php?ticket=%s" % (ggus_result)
        elif (ggus_instance == "prod"):
            ggus_file_url = "https://ggus.eu/ws/ticket_info.php?ticket=%s" % (ggus_result)
 
    return ggus_color, ggus_result, ggus_file_url

