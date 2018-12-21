// This is the source file for updating all the devices via server
#include "headers/libs.hpp"

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

  // If it does work then check at an interval if theres been an update
  int cachedUpdate = 0; // The update the client has
  int currentUpdate = 0; // Update interval cached on client
  std::string data = "";

  // Check the server
  data = sock.take();
  std::cout << data << std::endl;

  do {
    // Check for update
    sock.give("check_update");
    currentUpdate = stoi(sock.take());

    // If you dont have the same update then, update it
    if(currentUpdate != cachedUpdate){
      cachedUpdate = currentUpdate;
      std::cout << "New update found!" << std::endl;
    }

    // Wait some time before checking again
    usleep(1000000);
  } while(sock.getStatus() == S_CONNECTED);

  // Close connection
  sock.stop();

  return 0;
}
