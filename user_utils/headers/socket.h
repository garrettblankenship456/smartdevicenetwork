// Socket class definitions
#pragma once

#include <stdio.h>

// Class
class CSocket {
private:
  char* hostname;
  int portnum;

public:
  CSocket(char* hostname, int portnum);
  ~CSocket();

  bool connect();
  void disconnect();
};
