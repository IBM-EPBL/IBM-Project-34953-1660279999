console.log("first")
var client = new Paho.MQTT.Client("test.mosquitto.org", 8080, "clientId");
console.log("Connected")
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({ onSuccess: onConnect });

function onConnect() {
  console.log("onConnect");
  client.subscribe("sensor/distance");

}
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function onMessageArrived(message) {
  console.log(Number(message.payloadString));
  const h1 = document.getElementsByClassName("random")[0];
  h1.innerHTML = message.payloadString;
}
