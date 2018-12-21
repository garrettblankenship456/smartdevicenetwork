// Actual definitions for the socket code
#include "../headers/socket.h"

CSocket::CSocket(char* hostname, int portnum){
  this->hostname = hostname;
  this->portnum = portnum;

  printf("Created socket to %s on port %d\n", hostname, portnum);
}
CSocket::~CSocket(){

}

bool CSocket::connect(){
  printf("Connecting to %s on port %d\n", hostname, portnum);

  return false;
}
void CSocket::disconnect(){

}
