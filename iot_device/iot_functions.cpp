// This is the source file to run all the IOT functions
#include "headers/libs.hpp"

/*
  THIS PROGRAM WILL BE SPECIALIZED FOR EACH DEVICE ACCORDING TO WHAT
  FUNCTION IT PERFORMS
*/

// Main function
int main(){
  // Setup socket and connect
  ClientSock sock("127.0.0.1", 5623);
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
  sock.give("test_device");
  data = sock.take();
  std::cout << data << std::endl;

  do {
    // Wait to be given a command
    data = sock.take();
    std::cout << data << std::endl;
  } while(sock.getStatus() == S_CONNECTED);

  // Close connection
  sock.stop();

  return 0;
}
