// This is the source file to run all the IOT functions
#include "headers/libs.hpp"

/*
  THIS PROGRAM WILL BE SPECIALIZED FOR EACH DEVICE ACCORDING TO WHAT
  FUNCTION IT PERFORMS
*/

// Main function
int main(int argc, char** argv){
  // Setup socket and connect
  ClientSock sock("10.0.0.191", 5623);
  sock.start();

  // End if the connection hasnt been made
  if(sock.getStatus() != S_CONNECTED){
    std::cout << "Connection cannot be made!" << std::endl;
    return -1;
  }

  // IOT functions


  // Server data handling
  std::string data = "";

  // Check the server
  data = sock.take();

  // Give the server a default ID is none specified in the launch params
  if(argc > 1)
    sock.give(argv[1]);
  else
    sock.give("test_device");

  data = sock.take();
  std::cout << data << std::endl;

  do {
    // Wait to be given a command
    data = sock.take();
    std::cout << data << std::endl;

    if(data == "end") break;
  } while(sock.getStatus() == S_CONNECTED);

  // Close connection
  sock.stop();

  return 0;
}
