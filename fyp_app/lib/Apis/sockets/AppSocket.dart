import 'package:fyp_app/interface/socketInterface.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
// import 'package:web_socket_channel/html.dart';

class SocketClass implements SocketInterface {
  WebSocketChannel? socket;
  SocketClass();

  @override
  void connect() {
    try {
      socket =
          WebSocketChannel.connect(Uri.parse("ws://127.0.0.1:8000/ws/admin"));
      socket!.stream.listen((event) {
        print(event);
      });
    } catch (e) {
      print(e);
    }
  }

  @override
  void printSocketName() {
    connect();
    socket!.sink.add("1");
  }
}
