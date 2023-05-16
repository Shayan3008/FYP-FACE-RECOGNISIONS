import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/login_screen.dart';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';

import '../configs/size_config.dart';
import '../static/static_data.dart';

class ResetPasswordScreen extends StatefulWidget {
  final String email;
  const ResetPasswordScreen({super.key, required this.email});

  @override
  State<ResetPasswordScreen> createState() => _ResetPasswordScreenState();
}

class _ResetPasswordScreenState extends State<ResetPasswordScreen>
    with SingleTickerProviderStateMixin {
  TextEditingController editingController = TextEditingController();
  TextEditingController editingController2 = TextEditingController();
  late AnimationController _animationController;
  bool showDifferentText = false;

  var checkData = false;
  @override
  void initState() {
    _animationController = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 500));
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    SizeConfig().init(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Reset Your Password',
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
                    child: AnimatedCrossFade(
                      crossFadeState: showDifferentText
                          ? CrossFadeState.showSecond
                          : CrossFadeState.showFirst,
                      duration: const Duration(milliseconds: 500),
                      firstChild: Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        child: const Text(
                          'Enter Code',
                          style: TextStyle(
                            fontSize: 20,
                            color: Colors.black87,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      secondChild: Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        child: const Text(
                          'Enter New Password',
                          style: TextStyle(
                            fontSize: 20,
                            color: Colors.black87,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
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
                        AnimatedBuilder(
                          animation: _animationController,
                          builder: (context, child) => Stack(
                            children: [
                              Transform(
                                transform: Matrix4.identity()
                                  ..rotateY(_animationController.value * 90),
                                child: Opacity(
                                  opacity: 1 - _animationController.value,
                                  child: TextField(
                                    controller: editingController,
                                    maxLength: 6,
                                    keyboardType: TextInputType.number,
                                    decoration: const InputDecoration(
                                      labelText: 'Code',
                                      border: OutlineInputBorder(
                                        borderSide: BorderSide(
                                            color: Colors.grey, width: 0.0),
                                      ),
                                      hintText:
                                          "Please Enter 6 digit Code Sent to email",
                                    ),
                                  ),
                                ),
                              ),
                              Opacity(
                                opacity: _animationController.value,
                                child: Transform(
                                  transform: Matrix4.identity()
                                    ..rotateY(
                                        (1 - _animationController.value) * 90),
                                  child: TextField(
                                    controller: editingController2,
                                    decoration: const InputDecoration(
                                      // labelText: '',
                                      border: OutlineInputBorder(
                                        borderSide: BorderSide(
                                            color: Colors.grey, width: 0.0),
                                      ),
                                      hintText: "Enter New Password",
                                    ),
                                  ),
                                ),
                              ),
                            ],
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
                      onPressed: !showDifferentText
                          ? () async => {
                                checkData = await checkCode(),
                                if (checkData)
                                  {
                                    _animationController.forward(),
                                    setState(
                                      () {
                                        showDifferentText = true;
                                      },
                                    )
                                  }
                                else
                                  {print("Error Found in checking Code")}
                              }
                          : () async => {
                                checkData = await changePass(),
                                if (checkData)
                                  {
                                    showDialog(
                                      context: context,
                                      builder: (context) => AlertDialog(
                                        title: const Text("CONGRATULATIONS"),
                                        content: const Text(
                                            "PASSWORD CHANGE SUCCESSFUL"),
                                        actions: [
                                          TextButton(
                                            child:
                                                const Text("Go Back to Login"),
                                            onPressed: () {
                                              Navigator.of(context)
                                                  .pushAndRemoveUntil(
                                                      MaterialPageRoute(
                                                          builder: (context) =>
                                                              const LoginScreen()),
                                                      (route) => false);
                                            },
                                          ),
                                        ],
                                      ),
                                    )
                                  }
                                else
                                  {print("Error Found in changing Password")}
                              },
                      child: AnimatedCrossFade(
                        crossFadeState: showDifferentText
                            ? CrossFadeState.showSecond
                            : CrossFadeState.showFirst,
                        duration: const Duration(milliseconds: 500),
                        firstChild: Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          child: const Text(
                            'Enter Code',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        secondChild: Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          child: const Padding(
                            padding: EdgeInsets.all(8),
                            child: Text(
                              'Change Password',
                              style: TextStyle(
                                fontSize: 18,
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
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

  Future<bool> checkCode() async {
    Response response = await http.post(
      Uri.parse(
          "${StaticData.httpUrl}${StaticData.portNumber}/apis/CheckCode/"),
      body: jsonEncode(
        {
          "email": widget.email,
          "code": editingController.text,
        },
      ),
    );
    if (response.statusCode == 200) {
      return true;
    }
    return false;
  }

  Future<bool> changePass() async {
    Response response = await http.post(
      Uri.parse(
          "${StaticData.httpUrl}${StaticData.portNumber}/apis/ChangePass/"),
      body: jsonEncode(
        {
          "email": widget.email,
          "password": editingController2.text,
        },
      ),
    );
    if (response.statusCode == 200) {
      return true;
    }
    return false;
  }
}
