import 'package:fyp_app/models/coordinates.dart';

abstract class SocketInterface {
  void connect(); // Function to connect socket
  void sendSocketMessage(Coordinates coordinates); // function to invoke data
  void dispose(); // function to destroy sockets
}
