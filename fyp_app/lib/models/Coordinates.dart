import 'dart:convert';
import 'dart:math' show cos, sqrt, asin;

import 'package:fyp_app/static/static_data.dart';
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

  Coordinates fromJson(dynamic list) {
    return Coordinates(
        id: list["id"], lat: list["latitude"], long: list["longitude"]);
  }

  Future<List<Coordinates>> getCameraLocationsFromApis() async {
    List<Coordinates> list1 = [];
    try {
      Response response = await http.get(Uri.parse(
          "${StaticData.httpUrl}${StaticData.portNumber}/apis/coordinates/"));
      List<dynamic> data = json.decode(response.body);
      for (int i = 0; i < data.length; i++) {
        list1.add(fromJson(data[i]));
      }
      return list1;
    } catch (e) {
      print(e);
    }
    return list1;
  }
}
