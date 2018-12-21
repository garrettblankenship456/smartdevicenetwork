// These have the code for the header file definitions
#include "../headers/socket.hpp"

// Private functions
void ClientSock::generateHint(){
  hint.sin_family = AF_INET; // Set the communication type
  hint.sin_port = htons(port); // Set the port
  inet_pton(AF_INET, address.c_str(), &hint.sin_addr); // Set IP to bytes of the address
}

// Constructor & Destructor
ClientSock::ClientSock(std::string address, int port){
  this->address = address;
  this->port = port;

  // Initialize socket and status
  this->sock = socket(AF_INET, SOCK_STREAM, 0);
  this->sock_status = S_DISCONNECTED;

  // Zero out the buffer
  memset(this->buff, 0, 4096);

  // Generate data to connect to server
  this->generateHint();
}
ClientSock::~ClientSock(){
  // Close socket when deleting socket
  close(sock);
}

// Public functions
// Accessors
std::string ClientSock::getAddress(){ return address; }
int ClientSock::getPort(){ return port; }
SOCKET_STATUS ClientSock::getStatus(){ return sock_status; }
// Functions
bool ClientSock::start(){
  int connectRes = connect(sock, (sockaddr*)&hint, sizeof(hint));
  if(connectRes == -1) return false;

  this->sock_status = S_CONNECTED;
  return true;
}
bool ClientSock::stop(){
  close(sock);

  this->sock_status = S_DISCONNECTED;
  return true;
}
bool ClientSock::reconnect(){
  if(this->stop() == true && this->start() == true) return true;

  this->sock_status = S_CONNECTED;
  return false;
}
bool ClientSock::give(std::string data){
  if(sock_status != S_CONNECTED) return false;

  int sendRes = send(sock, data.c_str(), data.size() + 1, 0);
  if(sendRes == -1) return false;

  return true;
}
std::string ClientSock::take(){
  if(sock_status != S_CONNECTED) return "";

  memset(buff, 0, 4096);
  int bytesReceived = recv(sock, buff, 4096, 0);
  std::string byteString = std::string(buff, bytesReceived);

  return byteString;
}
