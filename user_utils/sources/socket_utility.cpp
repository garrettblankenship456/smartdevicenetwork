// This is the source file to test the connectivity to the server
#include "headers/libs.hpp"

// Functional programming structure as it does not need anything else except its self

// Main function
int main(int argc, char** argv){
  // Declarations
  std::string host;
  unsigned int port;

  // Inputs
  if(argc < 1){
    // No arguments provided, all defaults
    host = "127.0.0.1";
    port = 5623;
  } else if(argc < 2){
    // One argument provided, its the ip first and then default port
    host = argv[1];
    port = 5623;
  } else if(argc < 3){
    // Two arguments provided, ip and port
    host = argv[1];
    port = atoi(argv[2]);
  } else {
    // Return exit failure and display usage
    std::cout << "Usage: " << argv[0] << " <hostname (default: 127.0.0.1)> <port (default: 5623)>" << std::endl;
    return EXIT_FAILURE;
  }

  // Setup socket
  ClientSock sock(host, port);
  sock.start();

  if(sock.getStatus() != S_CONNECTED){
    std::cout << "No connection to server on " << host << ":" << port << std::endl;
    return EXIT_FAILURE;
  }

  // Data to user
  std::cout << "Execution past connection check, assume connected." << std::endl; 

  // Make do-while to send user input to the server
  // Declarations
  std::string str = "";
  std::string input = "";

  do {
    // Get data from server
    str = sock.take();

    // Output data received
    std::cout << str << std::endl;

    // Close socket if end has been typed
    if(str == "end"){
      std::cout << "Closing connection" << std::endl;
      sock.stop();
      break;
    }

    // Display a cursor for user input
    std::cout << "> " << std::flush;

    // Get user input from standard in
    std::getline(std::cin, input);

    // Send to the server
    sock.give(input);
  } while(sock.getStatus() == S_CONNECTED);

  // Cleanup
  sock.stop();

  // Healthy return
  return EXIT_SUCCESS;
}
