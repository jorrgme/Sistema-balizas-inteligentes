import crypto

"""
#Esta clase define metodos que se utilizan en diferentes
#ocasiones en el uso del protocolo
"""

def get_msg_type(msg):
    return msg['type']
def get_client_id(msg):
    return msg['client_id']
def get_client_address(msg):
    return msg['client_ip']
def get_client_port(msg):
    return msg['client_port']
def get_ap_id(msg):
    return msg['ap_id']
def get_ap_address(msg):
    return msg['ap_ip']
def get_ap_port(msg):
    return msg['ap_port']
def get_msg_topic(msg):
    return msg['topic']
def get_msg_subtopics(msg):
    return msg['subtopics']
def get_msg_response(msg):
    return msg['response']

def get_semaphore_state(old_state):
    new = ""
    if old_state == "green":
        new = "orange"
        return new
    if old_state == "orange":
        new = "red"
        return new
    if old_state == "red":
        new = "green"
        return new
    else:
        new = "emergency"
        return new

def get_semaphore_time_remaining(state):
    if(state!='emergency'):
        return round(RandomRange(1,60))
    else:
        return -1

def get_semaphore_pedestrians(semaphore):
    print(semaphore)
    if semaphore == "green":
        return 0
    if semaphore == "orange":
        return(round(RandomRange(1,30)))
    else:
        return(round(RandomRange(1,30)))

def get_garbage_state(type):
    if(type=='inactivo'):
        return(-1)
    else:
        return round(RandomRange(1,100))
def get_garbage_type(type):
    if(type=='inactivo'):
        return('inactivo')
    else:
        types = ['Plastico', 'Papel', 'Vidrio','Organico']
        return types[round(RandomRange(0,3))]

def get_tipo_via(via):
    if(via=='cortada'):
        return 'cortada'
    else:
        vias = ["Autopista", "Urbana", "General", "Comarcal", "Provincial"]
        return(vias[round(RandomRange(0,len(vias)-1))])

def get_limite_velocidad(tipo):
    if(tipo=='cortada'):
        return -1
    else:
        limites = {
        "Autopista": [100,120],
        "Urbana":[50,40],
        "General": [100,80],
        "Comarcal": [80, 60],
        "Provincial": [60, 50]}
        lim_via = limites[tipo]
        return(lim_via[round(RandomRange(0,1))])

def Random():
   r = crypto.getrandbits(32)
   return ((r[0]<<24)+(r[1]<<16)+(r[2]<<8)+r[3])/4294967295.0

def RandomRange(rfrom, rto):
   return Random()*(rto-rfrom)+rfrom

#Distancia entre dos coordenadas
def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

#Valores en comun entre dos listas
def in_common(lst1, lst2):
    lst3 = []
    for i in lst1:
        if i in lst2:
            lst3.append(i)
    return lst3
