import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/navigation_animation.dart';
import 'package:fyp_app/Screens/home_screen.dart';
import 'package:fyp_app/Screens/login_screen.dart';
import 'package:fyp_app/configs/size_config.dart';

import '../models/user.dart';
import '../utility/shared_preference_data.dart';
import '../utility/validation_check.dart';

class SIGNUPScreen extends StatefulWidget {
  const SIGNUPScreen({super.key});

  @override
  State<SIGNUPScreen> createState() => _SIGNUPScreenState();
}

class _SIGNUPScreenState extends State<SIGNUPScreen> {
  bool userValidation = false;

  bool emailValidation = false;

  bool passValidation = false;

  bool showPass = false;

  late ValidationChecker checker;

  late SharedPreferenceData storage;

  bool loading = false;
  TextEditingController email = TextEditingController();
  TextEditingController userName = TextEditingController();
  TextEditingController password = TextEditingController();
  @override
  Widget build(BuildContext context) {
    checker = ValidationChecker();
    storage = SharedPreferenceData();
    SizeConfig().init(context);
    // print(SizeConfig.verticalAspect!);
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: SizedBox(
              width: size.width * 0.7,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    child: const Text(
                      'SIGNUP Screen',
                      style: TextStyle(
                        fontSize: 20,
                        color: Colors.black87,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  SizedBox(
                    height: SizeConfig.screenHeight! * 0.3,
                    child: Image.asset('assets/tracking.jpg'),
                  ),
                  SizedBox(
                    height: SizeConfig.screenHeight! * 0.02,
                  ),
                  FractionallySizedBox(
                    widthFactor: 1.0,
                    child: Column(
                      children: [
                        TextField(
                          controller: userName,
                          decoration: InputDecoration(
                            labelText: 'Name',
                            errorText: userValidation == true
                                ? "Username must not be empty"
                                : null,
                            border: const OutlineInputBorder(
                              borderSide:
                                  BorderSide(color: Colors.grey, width: 0.0),
                            ),
                          ),
                        ),
                        SizedBox(
                          height: SizeConfig.screenHeight! * 0.02,
                        ),
                        TextField(
                          controller: email,
                          decoration: InputDecoration(
                            labelText: 'Email',
                            errorText: emailValidation == true
                                ? "Enter Valid Email"
                                : null,
                            border: const OutlineInputBorder(
                              borderSide:
                                  BorderSide(color: Colors.grey, width: 0.0),
                            ),
                          ),
                        ),
                        SizedBox(
                          height: SizeConfig.screenHeight! * 0.02,
                        ),
                        TextField(
                          controller: password,
                          decoration: InputDecoration(
                            suffixIcon: InkWell(
                              onTap: () {
                                setState(() {
                                  showPass = !showPass;
                                });
                              },
                              child: showPass
                                  ? const Icon(
                                      Icons.remove_red_eye,
                                    )
                                  : const Icon(Icons.remove_red_eye_outlined),
                            ),
                            labelText: 'Password',
                            errorText: passValidation == true
                                ? "Pass must be greater than 6 characters"
                                : null,
                            border: const OutlineInputBorder(
                              borderSide:
                                  BorderSide(color: Colors.grey, width: 0.0),
                            ),
                          ),
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
                        // signUpMethod(
                        //     userName.text, email.text, password.text, context)
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (ctx) => const NavbarAnimation(
                              child: HomeScreen(
                                user: 'UI TESTING',
                              ),
                            ),
                          ),
                        ),
                      },
                      child: const Text(
                        'SIGNUP',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 10),
                    child: InkWell(
                      onTap: () {
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (ctx) => const LoginScreen(),
                          ),
                        );
                      },
                      child: const Text('Have An Account? Login!!'),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  void signUpMethod(String userName, String email, String password,
      BuildContext context) async {
    setState(() {
      loading = true;
      userValidation = userName.isEmpty;
      emailValidation = email.isEmpty || !checker.isValidEmail(email);
      passValidation = password.length < 6;
    });
    if (emailValidation || passValidation || userValidation) {
      Future.delayed(const Duration(seconds: 5), (() {
        setState(() {
          userValidation = false;
          emailValidation = false;
          passValidation = false;
          loading = false;
        });
      }));
      return;
    }
    User user = User(userName, email, password);
    int status = await user.signUpUser();
    setState(() {
      loading = false;
    });
    if (status == 200) {
      // ignore: use_build_context_synchronously
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (ctx) => HomeScreen(
            user: userName,
          ),
        ),
      );
    }
    // if (name.contains('Email') || name.contains('password')) {
    //   // ignore: use_build_context_synchronously
    //   showDialog(
    //     context: context,
    //     builder: (BuildContext context) {
    //       return AlertDialog(
    //         title: const Text('Login Error'),
    //         content: Text(name),
    //         actions: [
    //           TextButton(
    //             onPressed: () {
    //               Navigator.of(context).pop();
    //             },
    //             child: const Text('OK'),
    //           ),
    //         ],
    //       );
    //     },
    //   );
    // } else {
    //   // ignore: use_build_context_synchronously
    //   Navigator.of(context).pushReplacement(
    //     MaterialPageRoute(
    //       builder: (ctx) => HomeScreen(
    //         user: name,
    //       ),
    //     ),
    //   );
    // }
  }
}
