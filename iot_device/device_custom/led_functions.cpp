// This is the source file to run an LED
#include "../headers/libs.hpp"

/*
  THIS PROGRAM WILL BE SPECIALIZED FOR EACH DEVICE ACCORDING TO WHAT
  FUNCTION IT PERFORMS
*/

// Main function
int main(int argc, char** argv){
  // Setup socket and connect
  ClientSock sock("10.0.0.191", 5623);
  sock.start();

  // Setup the GPIO pins
  system("gpio -g mode 18 out");

  // End if the connection hasnt been made
  if(sock.getStatus() != S_CONNECTED){
    std::cout << "Connection cannot be made!" << std::endl;
    return -1;
  }

  // IOT functions
  auto led_on = [&](){
    std::cout << "LED on" << std::endl;
    system("gpio -g write 18 1");
  };
  auto led_off = [&](){
    std::cout << "LED off" << std::endl;
    system("gpio -g write 18 0");
  };

  // Server data handling
  std::string data = "";

  // Check the server
  data = sock.take();

  // Give the server a default ID is none specified in the launch params
  if(argc > 1)
    sock.give(argv[1]);
  else
    sock.give("led_device");

  data = sock.take();
  std::cout << data << std::endl;

  do {
    // Wait to be given a command
    data = sock.take();

    // Controls wether the LED is on or off
    if(data == "led_on")
      led_on();
    if(data == "led_off")
      led_off();

    if(data == "end") break;
    if(data == "poweroff") system("sudo shutdown -r now");
  } while(sock.getStatus() == S_CONNECTED);

  // Close connection
  sock.stop();

  return 0;
}
