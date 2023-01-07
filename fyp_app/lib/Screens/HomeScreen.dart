// ignore: file_names
import 'package:flutter/material.dart';
import 'package:fyp_app/Apis/sockets/AppSocket.dart';
import 'package:fyp_app/Apis/sockets/sockets.dart';
import 'package:fyp_app/interface/socketInterface.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

class HomeScreen extends StatelessWidget {
  final String? user;
  const HomeScreen({super.key, this.user});

  @override
  Widget build(BuildContext context) {
    SocketInterface? socket;
    socket = SocketClass();
    // initialized Socket Class in the home
    return Scaffold(
      appBar: AppBar(
        title: Text(user!),
        centerTitle: true,
      ),
      body: SafeArea(
          child: Center(
        child: GestureDetector(
          onTap: (() => {
                socket!.printSocketName(),
              }),
          child: const CircleAvatar(
            radius: 120,
            backgroundColor: Colors.red,
            child: Text(
              'Generate Alert',
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      )),
    );
  }
}
