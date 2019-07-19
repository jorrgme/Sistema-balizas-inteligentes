from network import WLAN

def is_ap_message(apId,clientId, clientAddress, clientPort, topic):
    msg = '{"type": "IS_AP", "ap_id": "'
    msg+=apId
    msg+='", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientAddress
    msg+='", "client_port": "'
    msg+=str(clientPort)
    msg+='", "topic": "'
    msg+=topic
    msg+='"}'
    return msg

def confirm_ap_message(apId, apAddress, apPort, clientAddress, topic, subtopics, coordinates):
    msg = '{"type": "CONFIRM_AP", "ap_id": "'
    msg+=apId
    msg+='", "ap_ip": "'
    msg+=apAddress
    msg+='", "ap_port": "'
    msg+=str(apPort)
    msg+='", "client_ip": "'
    msg+=clientAddress
    msg+='", "topic": "'
    msg+=topic
    msg+='", "subtopics": "'
    msg+=str(subtopics)
    msg+='", "coordinates": "'
    msg+=coordinates
    msg+='"}'
    return msg

def get_info_message(apId,apAddress,clientId,clientAddress,clientPort,topic,subtopics):
    msg = '{"type": "GET_INFO", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientAddress
    msg+='", "client_port": "'
    msg+=str(clientPort)
    msg+='", "ap_id": "'
    msg+=apId
    msg+='", "ap_ip": "'
    msg+=apAddress
    msg+='", "topic": "'
    msg+=topic
    msg+='", "subtopics": "'
    msg+=str(subtopics)
    msg+='"}'
    return msg

def ans_info_message(apId, clientId, topic, response):
    msg = '{"type": "ANS_INFO", "ap_id": "'
    msg+=apId
    msg+='", "client_id": "'
    msg+=clientId
    msg+='", "topic": "'
    msg+=topic
    msg+='", "response": "'
    msg+=str(response)
    msg+='"}'
    return msg

def push_config_message(clientId, clientIp, clientPort, apId, topic, subtopics):
    msg = '{"type": "PUSH_CONFIG", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientIp
    msg+='", "client_port": "'
    msg+=str(clientPort)
    msg+='", "ap_id": "'
    msg+=apId
    msg+='", "topic": "'
    msg+=topic
    msg+='", "subtopics": "'
    msg+=str(subtopics)
    msg+='"}'
    return msg

def config_ok_message(apId,apIp,apPort,topic):
    msg = '{"type": "CONFIG_OK", "ap_id": "'
    msg+=apId
    msg+='", "ap_ip": "'
    msg+=apIp
    msg+='", "ap_port": "'
    msg+=str(apPort)
    msg+='", "topic": "'
    msg+=topic
    msg+='"}'
    return msg
#print(confirm_ap_message("ap43", address, address, "traffic_lights",
#                        ["state","time_remaining","pedestrians"], "39.491836, -0.400906"))
