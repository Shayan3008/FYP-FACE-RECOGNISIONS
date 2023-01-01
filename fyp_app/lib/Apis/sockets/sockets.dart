import 'package:fyp_app/interface/socketInterface.dart';
import 'package:web_socket_channel/html.dart';

class SocketClass implements SocketInterface {
  HtmlWebSocketChannel? socket;
  late String groupId;
  SocketClass(this.groupId);
  void _connect() {
    try {
      socket =
          HtmlWebSocketChannel.connect(Uri.parse("ws://127.0.0.1:8000/ws/1"));
      socket!.stream.listen((event) {
        print(event);
      });
      print(socket);
    } catch (e) {
      print(e);
    }
  }

  void printSocketName() {
    _connect();
    socket!.sink.add("Hello World");
  }
}
