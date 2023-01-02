// ignore: file_names
import 'package:flutter/material.dart';
import 'package:fyp_app/Apis/sockets/sockets.dart';
import 'package:fyp_app/interface/socketInterface.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

class HomeScreen extends StatelessWidget {
  final String? user;
  const HomeScreen({super.key, this.user});

  @override
  Widget build(BuildContext context) {
    SocketInterface? socket;
    if (kIsWeb) {
      socket = SocketClass('25');
    } // initialized Socket Class in the home
    return Scaffold(
      appBar: AppBar(
        title: Text(user!),
        centerTitle: true,
      ),
      body: SafeArea(
          child: Center(
        child: MaterialButton(
          onPressed: (() => {socket!.printSocketName()}),
          color: Colors.blue,
          hoverColor: Colors.red,
          child: const Text('Press This Button'),
        ),
      )),
    );
  }
}
