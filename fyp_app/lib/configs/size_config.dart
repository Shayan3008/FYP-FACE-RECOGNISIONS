// ignore: file_names
import 'package:flutter/material.dart';

class SizeConfig {
  MediaQueryData? mediaQuery;
  static double? screenHeight;
  static double? screenWidth;
  static double? horizantalAspect;
  static double? verticalAspect;
  void init(BuildContext context) {
    mediaQuery = MediaQuery.of(context);
    screenHeight = mediaQuery!.size.height;
    screenWidth = mediaQuery!.size.width;
    horizantalAspect = mediaQuery!.size.width / 100;
    verticalAspect = mediaQuery!.size.height / 100;
  }
}
