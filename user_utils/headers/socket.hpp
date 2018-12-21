// This file just makes the sockets easier to use, atleast for me
#pragma once

// Includes
#include <string>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

// Enumerators
enum SOCKET_STATUS {S_CONNECTED, S_DISCONNECTED, S_ERROR};

// Class
class ClientSock {
private:
  // Private variables
  int sock;
  std::string address;
  int port;
  sockaddr_in hint;
  char buff[4096];
  SOCKET_STATUS sock_status;

  // Functions
  void generateHint();

public:
  // Constructors
  ClientSock(std::string address, int port);
  // Destructor
  ~ClientSock();

  // Accessors
  std::string getAddress();
  int getPort();
  SOCKET_STATUS getStatus();

  // Functions
  bool start();
  bool stop();
  bool reconnect();
  bool give(std::string data);
  std::string take();
};
