import 'dart:convert';

import 'package:fyp_app/static/StaticData.dart';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';

class User {
  String userName;
  String email;
  String password;
  User(this.userName, this.email, this.password);
  Map toJson() => {
        "name": userName,
        "email": email,
        "password": password,
      };
  Future<String?> LoginUser() async {
    Response response = await http.post(
        Uri.parse(
          "${StaticData.httpUrl}${StaticData.portNumber}/apis/UserLogin/",
        ),
        body: jsonEncode(toJson()),
        headers: {"Referer": "http://127.0.0.1:8000"});
    print(response.body);
    if (response.statusCode == 200) {
      dynamic data = json.decode(response.body);
      print(data);
      return data["name"];
    }
    return null;
  }
}
