const express = require('express')
const app = express()
const bodyParser = require('body-parser');

app.set('view engine', 'ejs')
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

var PORT = 37020;
var BROADCAST_ADDR = "192.168.1.255";
var dgram = require('dgram');
var server = dgram.createSocket("udp4");
var auxsocket = dgram.createSocket("udp4");
var my_id = "web";
var coordinates="39.491836, -0.400906";
var subtopics=[];
var ap_id="Respuesta Ejemplo";
var apAddress="192.168.1.99";

var os = require( 'os' );

var ipAddress = os.networkInterfaces()['en0'][1]['address'];
console.log(ipAddress);

var time_remaining=30;
var pedestrians = 0;
var load=40;
var state="green";
var type="Vidrio";
var show_semaphore = false;
var id = "";
var road = "General";
var limit = 80;
var confirmado = false;
var apID = "";

selected_sem = false;
selected_gar = false;
selected_lim = false;

app.get('/', function (req, res) {
  res.render('index', {time_remaining: time_remaining,
                      show_semaphore: show_semaphore,
                      selected_sem: selected_sem,
                      selected_gar: selected_gar,
                      selected_lim: selected_lim,
                      state:state,
                      pedestrians:pedestrians,
                      load: load,
                      type: type,
                      road: road,
                      limit: limit,
                      ap_id: ap_id,
                      coordinates: coordinates,
                      subtopics: subtopics,
                      apID: apID
                      })
})

app.listen(3000, function () {
  console.log('Control de Earth City. Servidor desplegado')
})

app.get('/config',function(req,res){
  res.render('config',{ap_id: ap_id, ap_address: apAddress, confirmado: confirmado})
})

app.post('/config',function(req,res){
  let topic = req.body.topics;
  id = req.body.apIdText;
  subs_modif=[]
  let s1 = req.body.subtopic1;
  let v1 = req.body.value1;
  if(s1 != "" &&  v1 != ""){
    //s1 = "\""+s1+"\""
    subs_modif.push(s1);
    subs_modif.push(v1);
  }
  let s2 = req.body.subtopic2;
  let v2 = req.body.value2;
  if(s2 != "" &&  v2 != ""){
    subs_modif[s2] = v2;
  }
  let s3 = req.body.subtopic3;
  let v3 = req.body.value3;
  if(s3 != "" &&  v3 != ""){
    subs_modif[s3] = v3;
  }
  console.log(topic, id, subs_modif);
  broadcastNew(push_config_message("web",ipAddress,PORT,id,topic,subs_modif));

})

app.post('/', function (req, res) {
  let topic = req.body.topics;
  apID = req.body.ap_ID;
  console.log(topic, apID);
  if(topic == 'traffic_lights'){
    selected_sem = true;
    selected_gar = false;
    selected_lim = false;
  }
  else if(topic == 'garbage_load'){
    selected_sem = false;
    selected_gar = true;
    selected_lim = false;
  }
  else if(topic == 'speed_limit'){
    selected_sem = false;
    selected_gar = false;
    selected_lim = true;
  }
  console.log(ap_id,coordinates,subtopics);

  broadcastNew(is_ap_message(apID,my_id,ipAddress,PORT,topic));
  res.render('index', {time_remaining: time_remaining,
                      show_semaphore: show_semaphore,
                      selected_sem: selected_sem,
                      selected_gar: selected_gar,
                      selected_lim: selected_lim,
                      state:state,
                      pedestrians:pedestrians,
                      load: load,
                      type: type,
                      road: road,
                      limit: limit,
                      ap_id: ap_id,
                      coordinates: coordinates,
                      subtopics: subtopics,
                      apID: apID
                      })
})

server.bind(PORT,function() {
    server.setBroadcast(true);
});

server.on('message', function (message, remote) {
  if(remote.address!=ipAddress){
    var obj = JSON.parse(message);
    if(obj['type']=='CONFIRM_AP'){
      apAddress = obj.ap_ip;
      ap_id = obj.ap_id;
      coordinates = obj.coordinates;
      subtopics = obj.subtopics;

      if(obj.topic=='traffic_lights'){
        broadcastNew(get_info_message(obj.ap_id,apAddress,my_id,ipAddress, PORT,obj.topic,["state","time_remaining","pedestrians"]));
      } else if(obj.topic == 'garbage_load'){
        broadcastNew(get_info_message(obj.ap_id,apAddress,my_id,ipAddress, PORT,obj.topic,["load","type"]));
      } else if(obj.topic == 'speed_limit'){
        broadcastNew(get_info_message(obj.ap_id,apAddress,my_id,ipAddress, PORT,obj.topic,["road","limit"]));
      }
    }else if(obj['type']=='ANS_INFO'){
      var obj = JSON.parse(message);
      if(obj.topic == 'traffic_lights'){
        var str = obj.response.split("\'").join("\"");
        time_remaining = JSON.parse(str).time_remaining;
        state = JSON.parse(str).state;
        pedestrians = JSON.parse(str).pedestrians;

      } else if(obj.topic == 'garbage_load'){
          var str = obj.response.split("\'").join("\"");
          load = JSON.parse(str).load;
          type = JSON.parse(str).type;
      } else if(obj.topic == 'speed_limit'){
          var str = obj.response.split("\'").join("\"");
          road = JSON.parse(str).road;
          limit = JSON.parse(str).limit;
      }
    }
    else if(obj['type']=='CONFIG_OK'){
      console.log("Recibida confirmacion CONFIG_OK")
      confirmado = true;
    }
  }
});

function sendMsg(msg){
  var message = new Buffer(msg);
  server.send(message, 0, message.length, PORT, apAddress, function() {
    console.log("enviando a: "+apAddress)
  });
}

function broadcastNew(msg) {
    var message = new Buffer(msg);
    server.send(message, 0, message.length, PORT, BROADCAST_ADDR, function() {
        //console.log(message);
    });
}

function is_ap_message(apId,clientId, clientAddress, clientPort, topic){
    msg = '{"type": "IS_AP", "ap_id": "'
    msg+=apId
    msg+='", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientAddress
    msg+='", "client_port": "'
    msg+=clientPort
    msg+='", "topic": "'
    msg+=topic
    msg+='"}'
    return msg
}

function get_info_message(apId,apAddress,clientId,clientAddress,clientPort,topic,subtopics){
    msg = '{"type": "GET_INFO", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientAddress
    msg+='", "client_port": "'
    msg+=clientPort.toString()
    msg+='", "ap_id": "'
    msg+=apId
    msg+='", "ap_ip": "'
    msg+=apAddress
    msg+='", "topic": "'
    msg+=topic
    msg+='", "subtopics": "'
    msg+=subtopics.toString()
    msg+='"}'
    return msg
}

function push_config_message(clientId, clientIp, clientPort, apId, topic, subtopics){
    msg = '{"type": "PUSH_CONFIG", "client_id": "'
    msg+=clientId
    msg+='", "client_ip": "'
    msg+=clientIp
    msg+='", "client_port": "'
    msg+=clientPort.toString()
    msg+='", "ap_id": "'
    msg+=apId
    msg+='", "topic": "'
    msg+=topic
    msg+='", "subtopics": "'
    msg+=subtopics.toString()
    msg+='"}'
    return msg
}
