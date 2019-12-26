// This file runs the server and allows each device to communicate with eachother

// Requirements
const net = require("net");
const fs = require("fs");

// Read config
var config = JSON.parse(fs.readFileSync("serverconfig.json"));

// Initialize some variables
var updateNum = 0;
var connectedClients = {};

// Functions
function getID(s){
  Object.keys(connectedClients).forEach((index) => {
    if(connectedClients[index] == s){
      return index;
    }
  });
}
function getSock(i, callback){
  callback(connectedClients[i]);
}

// Main code
console.log("Setting up server");

// Setup update server
var server = net.createServer((socket) => {
  try {
    console.log("Client connected");
    socket.setEncoding("utf8");

    // Let the user you know your there
    socket.write("handshake");

    var setupFinished = false;
    var id = "";

    // Read data
    socket.on("data", (data) => {
      // Remove null character
      data = data.replace(/\0[\s\S]*$/g, "");

      // Setup ID
      if(setupFinished == false){
        id = data;
        setupFinished = true;

        // Excempt any update requests as being a user
        if(id != "update_id"){
          connectedClients[id] = socket;
          console.log("New ID: " + id);
        } else {
          console.log("Update user excempt!");
        }

        socket.write("handshake");
        return;
      }

      // Different server requests
      if(data == "test"){ // Test
        socket.write("server_test_echo");
      } else if(data == "new_update"){ // Sending out new update
        updateNum++;
        socket.write("handshake");
      } else if(data == "check_update"){ // Checking update number
        socket.write(updateNum.toString());
      } else if(data.startsWith("broadcast")){
        console.log("Broadcasting command!");
        // Get the command to send
        var cmd = data.split(" ").splice(1).join(" ");

        // Loop through each connected device and send command
        Object.keys(connectedClients).forEach((index) => {
          var val = connectedClients[index];
          if(val != socket){
            val.write(cmd);
          }
        });

        socket.write("handshake");
      } else if(data.startsWith("route")) {
        // Get the data from the given command
        var sender = id;
        var destination = data.split(" ")[1];

        // Create command
        var command = data.split(" ").slice(2);
        command.unshift(sender);
        command.join(" ");

        console.log("Routing command from '" + sender + "', destination: '" + destination + "' with the command '" + command + "'");

        // Get the socket of the destination id and send command
        getSock(destination, (target) => {
          if(target != undefined){
            target.write(command);
            console.log(" - SENT");

            socket.write("sent");
          } else {
            console.log(" - DESTINATION INVALID");

            socket.write("dest_invalid");
          }
        });
      } else if(data == "exit"){
        socket.write("end");
      } else { // Unknown
        socket.write("unknown_req");
      }
    });
  } catch(e){
    console.log(e);
    socket.close();
  }

  // Handle disconnect
  socket.on("end", () => {
    Object.keys(connectedClients).forEach((index) => {
      var val = connectedClients[index];
      if(val == socket){
        delete connectedClients[index];
        console.log("Removed " + index + " from connected clients list");
      }
    });
  })
});

// Make the server listen
console.log("Server listening| Port: " + config.port + ", IP: " + config.ip);
server.listen(config.port, config.ip);
