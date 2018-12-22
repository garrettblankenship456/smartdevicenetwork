// This is the source file to test the connectivity to the server
#include "headers/libs.hpp"

// Main function
int main(int argc, char** argv){
  // Setup socket
  ClientSock sock("127.0.0.1", 5623);
  sock.start();

  if(sock.getStatus() != S_CONNECTED){
    std::cout << "No connection to server" << std::endl;
    return -1;
  }

  // Make do-while to ask the user to make it more flexable
  std::string str = "";
  std::string input = "";
  do {
    str = sock.take();
    std::cout << str << std::endl;

    if(str == "end"){
      std::cout << "Closing connection" << std::endl;
      sock.stop();
      break;
    }

    std::cout << "> " << std::flush;
    
    std::getline(std::cin, input);
    sock.give(input);
  } while(sock.getStatus() == S_CONNECTED);

  sock.stop();

  return 0;
}
