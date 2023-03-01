import 'dart:convert';

import 'package:fyp_app/interface/socketInterface.dart';
import 'package:fyp_app/models/Coordinates.dart';
import 'package:fyp_app/static/StaticData.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
// import 'package:web_socket_channel/html.dart';

class SocketClass implements SocketInterface {
  WebSocketChannel? socket;
  SocketClass();

  @override
  void connect() {
    try {
      socket = WebSocketChannel.connect(Uri.parse(
          "${StaticData.socketUrl}${StaticData.portNumber}/ws/admin"));
      socket!.stream.listen((event) {
        print(event);
      });
    } catch (e) {
      print(e);
    }
  }

  @override
  void sendSocketMessage(Coordinates coordinates) {
    connect();
    socket!.sink.add(jsonEncode(<String, dynamic>{
      "id": coordinates.id,
      "latitude": coordinates.lat,
      "longitude": coordinates.long
    }));
  }

  @override
  void dispose() {
    socket!.sink.close(status.goingAway);
  }
}
