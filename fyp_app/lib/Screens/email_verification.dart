import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/reset_password.dart';
import 'package:fyp_app/configs/size_config.dart';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';

import '../static/static_data.dart';

class EmailVerification extends StatefulWidget {
  const EmailVerification({super.key});

  @override
  State<EmailVerification> createState() => _EmailVerificationState();
}

class _EmailVerificationState extends State<EmailVerification> {
  TextEditingController editingController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    SizeConfig().init(context);

    bool reset;
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Verify Your Email',
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: SizedBox(
              width: SizeConfig.screenWidth! * 0.7,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    child: const Text(
                      'Enter Email For verification',
                      style: TextStyle(
                        fontSize: 20,
                        color: Colors.black87,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  SizedBox(
                    height: SizeConfig.screenHeight! * 0.02,
                  ),
                  FractionallySizedBox(
                    widthFactor: 1.0,
                    child: Column(
                      children: [
                        SizedBox(
                          height: SizeConfig.screenHeight! * 0.02,
                        ),
                        TextField(
                          controller: editingController,
                          decoration: const InputDecoration(
                            labelText: 'Email',
                            border: OutlineInputBorder(
                              borderSide:
                                  BorderSide(color: Colors.grey, width: 0.0),
                            ),
                          ),
                        ),
                        SizedBox(
                          height: SizeConfig.screenHeight! * 0.02,
                        ),
                      ],
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 10),
                    child: MaterialButton(
                      color: Colors.blueAccent,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                      onPressed: () async => {
                        reset = await sendResetMail(
                            editingController.value.toString()),
                        if (reset)
                          {
                            Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (context) => ResetPasswordScreen(
                                  email: editingController.text.toString(),
                                ),
                              ),
                            ),
                          }
                        else
                          {
                            AlertDialog(
                              title: const Text("Error"),
                              content: const Text("Cannot Send Email"),
                              actions: [
                                TextButton(
                                  child: const Text("OK"),
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                  },
                                ),
                              ],
                            ),
                          }
                      },
                      child: const Text(
                        'Verify',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Future<bool> sendResetMail(String email) async {
    Response response = await http.post(
      Uri.parse("${StaticData.httpUrl}${StaticData.portNumber}/apis/SendMail/"),
      body: jsonEncode(
        {
          "email": editingController.text,
        },
      ),
    );
    if (response.statusCode == 200) {
      return true;
    }
    return false;
  }
}
