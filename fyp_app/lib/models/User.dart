// ignore: file_names
import 'dart:convert';

import 'package:fyp_app/static/static_data.dart';
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
  Future<String> loginUser(String cookie) async {
    Response response = await http.post(
      Uri.parse(
        "${StaticData.httpUrl}${StaticData.portNumber}/apis/UserLogin/",
      ),
      body: jsonEncode(toJson()),
      headers: {
        'X-CSRF-Token': cookie,
        'Content-type': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      dynamic data = json.decode(response.body);
      return data["name"];
    }
    return response.body;
  }

  Future<int> signUpUser() async {
    Response response = await http.post(
      Uri.parse(
        "${StaticData.httpUrl}${StaticData.portNumber}/apis/UserSignup/",
      ),
      body: jsonEncode(toJson()),
      headers: {
        'Content-type': 'application/json',
      },
    );
    return response.statusCode;
  }
}
