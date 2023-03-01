// ignore: file_names
import 'dart:convert';
import 'dart:math' show cos, sqrt, asin;

import 'package:fyp_app/static/StaticData.dart';
import 'package:http/http.dart';
import 'package:http/http.dart' as http;

class Coordinates {
  int? id;
  double? long;
  double? lat;
  Coordinates({this.id, this.long, this.lat});
  int getClosestMap(List<Coordinates> list) {
    int index = 0;
    int minDistance = 100000000000;
    for (int i = 0; i < list.length; i++) {
      var p = 0.017453292519943295;
      var c = cos;
      var a = 0.5 -
          c((list[i].lat! - lat!) * p) / 2 +
          c(list[i].lat! * p) *
              c(lat! * p) *
              (1 - c((list[i].long! - long!) * p)) /
              2;
      if (minDistance > 12742 * asin(sqrt(a))) {
        index = i;
      }
    }
    return index;
  }

  static Future<List<Coordinates>> getCameraLocationsFromApis() async {
    List<Coordinates> list1 = [];
    try {
      Response response = await http.get(Uri.parse(
          "${StaticData.httpUrl}${StaticData.portNumber}/apis/coordinates/"));
      print(response.body);
      List<dynamic> data = json.decode(response.body);
      for (int i = 0; i < data.length; i++) {
        list1.add(
          Coordinates(
              id: data[i]["id"],
              lat: data[i]["latitude"],
              long: data[i]["longitude"]),
        );
      }
      return list1;
    } catch (e) {
      print(e);
    }
    return list1;
  }
}
