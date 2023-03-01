// ignore: file_names
import 'package:fyp_app/models/Coordinates.dart';
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
  List<Coordinates> list1 = [
    Coordinates(lat: 24.954026378293587, long: 67.05843673597522),
    Coordinates(lat: 24.946861240743132, long: 67.05332256849731)
  ];
  SocketInterface? socket;
  final _location = Location();
  PermissionStatus? permissionStatus;
  LocationData? locationData;

  @override
  void initState() {
    super.initState();
    socket = SocketClass();

    getPermission().then((value) => {});
  }

  @override
  void dispose() {
    super.dispose();
    socket!.dispose();
  }

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

  //
  Future<void> openGoogleLocation() async {
    if (permissionStatus == PermissionStatus.granted) {
      locationData = await _location.getLocation();
      Coordinates location = Coordinates(
          long: locationData!.longitude, lat: locationData!.latitude);
      List<Coordinates> list1 = await Coordinates.getCameraLocationsFromApis();
      int index = location.getClosestMap(list1);
      socket!.sendSocketMessage(list1[index]);
    } else {
      getPermission();
    }
  }

  @override
  Widget build(BuildContext context) {
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
                // await openGoogleLocation(),
                // socket!.printSocketName(),
                await openGoogleLocation(),
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
