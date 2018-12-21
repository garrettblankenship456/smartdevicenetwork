// This file runs the server and allows each device to communicate with eachother

// Requirements
const net = require("net");
const fs = require("fs");

// Read config
var config = JSON.parse(fs.readFileSync("serverconfig.json"));

// Main code
console.log("Setting up server");

// Setup basic server
var server = net.createServer((socket) => {
  socket.write("Working great!\n");
  socket.pipe(socket);
});

// Make the server listen
console.log("Server listening| Port: " + config.port + ", IP: " + config.ip);
server.listen(config.port, config.ip);
