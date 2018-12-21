// This file runs the server and allows each device to communicate with eachother

// Requirements
const net = require("net");
const fs = require("fs");

// Read config
var config = JSON.parse(fs.readFileSync("serverconfig.json"));

// Initialize some variables
var updateNum = 0;

// Main code
console.log("Setting up server");

// Setup update server
var server = net.createServer((socket) => {
  socket.setEncoding("utf8");
  console.log("Client connected");

  // Let the user you know your there
  socket.write("handshake");

  // Read data
  socket.on("data", (data) => {
    console.log(data);
    // Different server requests
    if(data == "test\u0000"){ // Test
      socket.write("server_test_echo");
    } else if(data == "new_update\u0000"){ // Sending out new update
      updateNum++;
      socket.write("handshake");
    } else if(data == "check_update\u0000"){ // Checking update number
      socket.write(updateNum.toString());
    } else if(data == "exit\u0000"){
      console.log("Dropped client gracefully!");
      socket.write("end");
    } else { // Unknown
      socket.write("unknown_req");
    }
  });
});

// Make the server listen
console.log("Server listening| Port: " + config.port + ", IP: " + config.ip);
server.listen(config.port, config.ip);
