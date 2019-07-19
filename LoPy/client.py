import socket, machine, ujson
import time, prot_earth, earth_utils
from network import WLAN

TOPIC = "traffic_lights"
INTERESTS = ['state','pedestrians']

CLI_ID = "lopy237"
CLI_PORT = 44444

POSITION = (39.593090, -0.299751)

SENT = False

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET,32, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
client.settimeout(1.0)
client.bind(("", CLI_PORT))

wlan=WLAN(mode=(WLAN.STA))
address=wlan.ifconfig()[0]

while True:
    if(not SENT):
        #Envio mensaje busqueda APs
        message = prot_earth.is_ap_message(CLI_ID, address, CLI_PORT, TOPIC)
        client.sendto(message, ('255.255.255.255', 37020))
        print("\n\n======================================")
        print("Sent IS_AP message")
        SENT = True

    data, addr = client.recvfrom(1024)
    #Nos llega un mensaje
    if(data):
        content = ujson.loads(data)
        #CONFIRM_AP recibido desde el AP
        if(earth_utils.get_msg_type(content) == 'CONFIRM_AP'):
            ap_address = earth_utils.get_ap_address(content)
            ap_port = earth_utils.get_ap_port(content)
            print("\nCONFIRM_AP received from: "+ap_address+" PORT: "+ap_port)
            #subtopics que trata el ap
            subtopics = earth_utils.get_msg_subtopics(content)
            #Subtopics en comun entre intereses del cliente y los del AP
            our_interests = earth_utils.in_common(INTERESTS,subtopics)

            #Sabemos los sutopics, ahora podemos preguntar sobre ellos
            message = prot_earth.get_info_message(earth_utils.get_ap_id(content),
                                                ap_address,
                                                CLI_ID, address, CLI_PORT,
                                                TOPIC, our_interests)
            client.sendto(message, (ap_address, int(ap_port)))
            print("\nSent GET_INFO message to: " + ap_address+" PORT: "+ap_port)
        if(earth_utils.get_msg_type(content) == 'ANS_INFO'):
            ap_id = earth_utils.get_ap_id(content)
            response = earth_utils.get_msg_response(content)
            print("\nGot response to GET_INFO from: "+ap_id)
            print("With content: "+str(response))
            print("\n\n======================================")
            SENT = False
    time.sleep(5)
