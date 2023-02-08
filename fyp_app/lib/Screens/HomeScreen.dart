// ignore: file_names
import 'package:location/location.dart';
import 'package:flutter/material.dart';
import 'package:fyp_app/Apis/sockets/AppSocket.dart';
import 'package:fyp_app/interface/socketInterface.dart';
import 'package:url_launcher/url_launcher.dart';

class HomeScreen extends StatefulWidget {
  final String? user;

  const HomeScreen({super.key, this.user});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _location = Location();
  PermissionStatus? permissionStatus;
  LocationData? locationData;
  Future<void> getPermission() async {
    bool serviceEnabled;
    serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await _location.requestService();
      if (!serviceEnabled) {
        return;
      }
    }

    permissionStatus = await _location.hasPermission();
    if (permissionStatus == PermissionStatus.denied) {
      permissionStatus = await _location.requestPermission();
      if (permissionStatus != PermissionStatus.granted) {
        return;
      }
    }
    return;
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getPermission().then((value) => {});
  }

  @override
  Widget build(BuildContext context) {
    SocketInterface? socket;
    socket = SocketClass();
    // initialized Socket Class in the home
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.user!),
        centerTitle: true,
      ),
      body: SafeArea(
          child: Center(
        child: GestureDetector(
          onTap: (() async => {
                if (permissionStatus == PermissionStatus.granted)
                  {
                    locationData = await _location.getLocation(),
                    print(locationData)
                  }
                // socket!.printSocketName(),
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
