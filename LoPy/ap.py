import socket, ujson, prot_earth, earth_utils
from network import WLAN

SUBTOPICS = ["state","time_remaining","pedestrians"]
AP_TOPIC = ['traffic_lights','garbage_load','speed_limit']
wlan=WLAN(mode=(WLAN.STA))
address=wlan.ifconfig()[0]

state = "green"
time_remaining = 60
pedestrians = 50
via = "General"
limit = 120
load = 65
type = "Vidrio"
my_id = "ap43"

AP_PORT = 37020

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
server.setsockopt(socket.SOL_SOCKET, 32, 1)
server.bind(("", AP_PORT))
while True:
    data, addr = server.recvfrom(1024)
    content = ujson.loads(data)
    if('ap_id' in content):
        ap_id = earth_utils.get_ap_id(content)
    else:
        ap_id = ""
    if (earth_utils.get_msg_type(content) == "IS_AP"
    and earth_utils.get_msg_topic(content) in AP_TOPIC
    and(ap_id==my_id or ap_id=="")):
        #Envia confirmacion porque es AP y tiene entre sus topics el solicitado
        clientAddress = earth_utils.get_client_address(content)
        client_port = earth_utils.get_client_port(content)
        client_topic = earth_utils.get_msg_topic(content)
        print("\n\n======================================")
        print('Sending confirmation to address: '+ clientAddress)
        message = prot_earth.confirm_ap_message(my_id, address, AP_PORT, clientAddress, client_topic, SUBTOPICS, "39.491836, -0.400906")
        server.sendto(message, (clientAddress, int(client_port)))

    #Recibimos mensaje de peticion de informacion
    elif earth_utils.get_msg_type(content) == "GET_INFO":
        clientAddress = earth_utils.get_client_address(content)
        client_port = earth_utils.get_client_port(content)
        client_id = earth_utils.get_client_id(content)
        #Anadido despues
        client_topic = earth_utils.get_msg_topic(content)
        print("\nInfo acquisition message arrived from: "+clientAddress+" PORT: "+client_port)

        #Respuesta al topic semaforos
        if(client_topic == 'traffic_lights'):
            print('Preguntado por semaforos')
            #Gestionar la informacion pedida para devolver una respuesta
            ans_info = earth_utils.get_msg_subtopics(content)
            ans_info = ans_info.replace(',',' ').replace('[',' ').replace(']',' ').replace("'",' ').split()
            response = {}
            for sub in ans_info:
                if(sub == 'state'):
                    state = earth_utils.get_semaphore_state(state)
                    print(state)
                    response[sub] = state
                elif(sub == "time_remaining"):
                    time_remaining = earth_utils.get_semaphore_time_remaining(state)
                    response[sub] = time_remaining
                elif(sub == "pedestrians"):
                    pedestrians = earth_utils.get_semaphore_pedestrians(state)
                    response[sub] = pedestrians
                else:
                    print("Asked for a topic not in database: "+sub)
                    response[str(sub)] = "Error. Subtopic not available on this context"
            message = prot_earth.ans_info_message(my_id,client_id, 'traffic_lights', str(response))
            server.sendto(message,(clientAddress, int(client_port)))
            print("Information sent to client: "+clientAddress+" PORT: "+client_port)
            print("\n\n======================================")

        #Respuesta al topic basura
        elif(client_topic == 'garbage_load'):
            #Gestionar la informacion pedida para devolver una respuesta
            ans_info = earth_utils.get_msg_subtopics(content)
            ans_info = ans_info.replace(',',' ').replace('[',' ').replace(']',' ').replace("'",' ').split()
            response = {}
            for sub in ans_info:
                if(sub == 'load'):
                    state = earth_utils.get_garbage_state(type)
                    print(state)
                    response[sub] = state
                elif(sub == "type"):
                    type = earth_utils.get_garbage_type(type)
                    response[sub] = type
                else:
                    print("Asked for a topic not in database: "+sub)
                    response[str(sub)] = "Error. Subtopic not available on this context"
            message = prot_earth.ans_info_message(my_id,client_id, 'garbage_load', str(response))
            server.sendto(message,(clientAddress, int(client_port)))
            print("Information sent to client: "+clientAddress+" PORT: "+client_port)
            print("\n\n======================================")

        #Respuesta al topic velocidad
        elif(client_topic == 'speed_limit'):
                #Gestionar la informacion pedida para devolver una respuesta
                ans_info = earth_utils.get_msg_subtopics(content)
                ans_info = ans_info.replace(',',' ').replace('[',' ').replace(']',' ').replace("'",' ').split()
                response = {}
                for sub in ans_info:
                    if(sub == 'road'):
                        via = earth_utils.get_tipo_via(via)
                        print(state)
                        response[sub] = via
                    elif(sub == "limit"):
                        limit = earth_utils.get_limite_velocidad(via)
                        response[sub] = limit
                    else:
                        print("Asked for a topic not in database: "+sub)
                        response[str(sub)] = "Error. Subtopic not available on this context"
                message = prot_earth.ans_info_message(my_id,client_id, 'speed_limit', str(response))
                server.sendto(message,(clientAddress, int(client_port)))
                print("Information sent to client: "+clientAddress+" PORT: "+client_port)
                print("\n\n======================================")
        else:
            print("GET_INFO arrived for topic I do not talk about: "+client_topic)
    elif(earth_utils.get_msg_type(content)=='PUSH_CONFIG' and earth_utils.get_ap_id(content)):
        print("Recibido un push config")
        clientAddress = earth_utils.get_client_address(content)
        client_port = earth_utils.get_client_port(content)
        topic = earth_utils.get_msg_topic(content)
        subtopics = earth_utils.get_msg_subtopics(content)
        subtopics = subtopics.replace('{','').replace('}','').split(',')
        if(topic=='traffic_lights'):
            for sub in subtopics:
                if(sub=='state'):
                    state=subtopics[subtopics.index('state')+1]
                if(sub=='time_remaining'):
                    time_remaining=subtopics[subtopics.index('time_remaining')+1]
                if(sub=='pedestrians'):
                    pedestrians=subtopics[subtopics.index('pedestrians')+1]
        elif(topic=='garbage_load'):
            for sub in subtopics:
                if(sub=='load'):
                    load=subtopics[subtopics.index('load')+1]
                if(sub=='type'):
                    type=subtopics[subtopics.index('type')+1]
                    print('Tipo: '+type)
        elif(topic=='speed_limit'):
            for sub in subtopics:
                if(sub=='road'):
                    via=subtopics[subtopics.index('road')+1]
                if(sub=='limit'):
                    limit=subtopics[subtopics.index('limit')+1]

        message = prot_earth.config_ok_message(my_id,address,AP_PORT,topic)
        server.sendto(message,(clientAddress, int(client_port)))
