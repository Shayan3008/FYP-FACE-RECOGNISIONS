// ignore: file_names
import 'dart:math' show cos, sqrt, asin;

class Coordinates {
  double? long;
  double? lat;
  Coordinates({this.long, this.lat});
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
}
