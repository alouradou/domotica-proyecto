import * as mqtt from 'mqtt/dist/mqtt.min';

// const broker = 'test.mosquitto.org';
// const broker = '192.168.0.19';
const broker =  '192.168.137.8';
// modification du fichier /etc/mosquitto/mosquitto.conf
// puis sudo systemctl restart mosquitto
// avec ajout des lignes du tuto : https://cedalo.com/blog/enabling-websockets-over-mqtt-with-mosquitto/
// autre source : http://www.steves-internet-guide.com/mqtt-websockets/

const client = mqtt.connect('ws://'+broker, {
    port: 8080,
});

// Éléments HTML
const messageContainer = document.getElementById('messageContainer');

// Connecter le client MQTT
client.on('connect', function () {
    console.log('Connecté au broker MQTT');
    const newMessage = document.createElement('span')
    newMessage.textContent = 'Connecté au broker MQTT ' + broker;
    newMessage.style.color = 'green';
    messageContainer.appendChild(newMessage);
    messageContainer.appendChild(document.createElement("br"));

    client.subscribe('upm/mqtt/#', function (err) {
        if (!err) {
            client.publish('upm/mqtt/web', 'Web Interface Connected')
        }
    });

});

// Afficher les messages reçus
client.on('message', function (topic, message) {
    console.log('Message:', message.toString());

    // Créer un élément de paragraphe pour afficher le message
    const newMessage = document.createElement('span');
    newMessage.textContent = topic.toString() + ": " + message.toString();

    // Ajouter le message à l'élément container
    messageContainer.appendChild(newMessage);
    messageContainer.appendChild(document.createElement("br"));
});

export function sendMessage(name, channel=1) {
    client.subscribe('upm/mqtt/#', function (err) {
        if (!err) {
            client.publish('upm/mqtt/web/name'+channel.toString(), name)
        }
    });
}
