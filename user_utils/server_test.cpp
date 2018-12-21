// This is the source file to test the connectivity to the server
#include "headers/libs.hpp"

// Includes for this file specifically since its a specialty tool


// Main function
int main(int argc, char** argv){
  // Setup socket
  CSocket sock("127.0.0.1", 5623);
  sock.connect();

  return 0;
}
