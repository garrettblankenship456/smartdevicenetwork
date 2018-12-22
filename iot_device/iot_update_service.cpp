// This is the source file for updating all the devices via server
#include "headers/libs.hpp"

// Main function
int main(){
  // Setup socket and connect
  ClientSock sock("10.0.0.191", 5623);
  sock.start();

  // End if the connection hasnt been made
  if(sock.getStatus() != S_CONNECTED){
    std::cout << "Connection cannot be made!" << std::endl;
    return -1;
  }

  // Update lambda
  auto updateFiles = [&](){
    system("git fetch");
    system("../scripts/buildall.sh");
  };

  // If it does work then check at an interval if theres been an update
  int cachedUpdate = 0; // The update the client has
  int currentUpdate = 0; // Update interval cached on client
  std::string data = "";

  // Set ID
  data = sock.take();
  sock.give("update_id");
  data = sock.take();
  std::cout << data << std::endl;

  while(sock.getStatus() == S_CONNECTED){
    // Check for update
    sock.give("check_update");
    currentUpdate = stoi(sock.take());

    // If you dont have the same update then, update it
    if(currentUpdate != cachedUpdate){
      cachedUpdate = currentUpdate;
      std::cout << "New update found!" << std::endl;

      // Run update function
      updateFiles();
    }

    // Wait some time before checking again
    usleep(1000000);
  }

  // Close connection
  sock.stop();

  return 0;
}
