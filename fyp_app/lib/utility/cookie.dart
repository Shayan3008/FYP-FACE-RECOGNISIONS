import 'dart:convert';

import 'package:fyp_app/static/static_data.dart';
import 'package:http/http.dart';

class Cookie {
  String? cookie;
  Future<String?> getCookie() async {
    Response response = await get(
      Uri.parse(
        "${StaticData.httpUrl}${StaticData.portNumber}/apis/GetCookie/",
      ),
    );
    if (response.statusCode != 200) return null;
    return json.decode(response.body)['cookie'];
  }
}
