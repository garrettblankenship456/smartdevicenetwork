// This is the source file to test the connectivity to the server
#include "headers/libs.hpp"

// Main function
int main(int argc, char** argv){
  // Setup socket
  ClientSock sock("127.0.0.1", 5623);
  sock.start();

  std::string str = sock.take();
  if(sock.getStatus() == S_CONNECTED)
    std::cout << str << std::endl;
  else
    std::cout << "No connection to server" << std::endl;

  sock.stop();

  return 0;
}
