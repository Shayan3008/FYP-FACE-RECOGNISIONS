import 'package:flutter/material.dart';
// import 'package:fyp_app/Screens/home_screen.dart';
import 'package:fyp_app/Screens/signup_screen.dart';
import 'package:fyp_app/models/user.dart';
import 'package:fyp_app/utility/shared_preference_data.dart';
import 'package:fyp_app/utility/validation_check.dart';

import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool userValidation = false;
  bool emailValidation = false;
  bool passValidation = false;
  bool showPass = true;
  late ValidationChecker checker;
  late SharedPreferenceData storage;
  bool loading = false;
  TextEditingController email = TextEditingController();
  TextEditingController password = TextEditingController();
  @override
  Widget build(BuildContext context) {
    checker = ValidationChecker();
    storage = SharedPreferenceData();

    // TextEditingController userName = TextEditingController();

    Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: SafeArea(
            child: Center(
              child: SizedBox(
                width: size.width * 0.7,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: const Text(
                        'Login Screen',
                        style: TextStyle(
                          fontSize: 20,
                          color: Colors.black87,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    SizedBox(
                      height: size.height * 0.3,
                      child: Image.asset('assets/tracking.jpg'),
                    ),
                    SizedBox(
                      height: size.height * 0.02,
                    ),
                    FractionallySizedBox(
                      widthFactor: 1.0,
                      child: Column(
                        children: [
                          TextField(
                            controller: email,
                            decoration: InputDecoration(
                              labelText: 'Email',
                              errorText: emailValidation == true
                                  ? "Enter Valid Email"
                                  : null,
                            ),
                          ),
                          TextField(
                            controller: password,
                            obscureText: showPass,
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
                        onPressed: () => loginMethod(
                          email.text,
                          password.text,
                          context,
                        ),
                        child: loading
                            ? const CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 1,
                              )
                            : const Text(
                                'LOGIN',
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
                              builder: (ctx) => const SIGNUPScreen(),
                            ),
                          );
                        },
                        child: const Text('No Account Signup!!'),
                      ),
                    )
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  void loginMethod(String email, String password, BuildContext context) async {
    setState(() {
      loading = true;
      emailValidation = email.isEmpty || !checker.isValidEmail(email);
      passValidation = password.length < 6;
    });
    if (emailValidation || passValidation) {
      Future.delayed(const Duration(seconds: 5), (() {
        setState(() {
          emailValidation = false;
          passValidation = false;
          loading = false;
        });
      }));
      return;
    }
    User user = User("", email, password);
    String name = await user.loginUser(await storage.getCookie());
    setState(() {
      loading = false;
    });
    if (name.contains('Email') || name.contains('password')) {
      // ignore: use_build_context_synchronously
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Login Error'),
            content: Text(name),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('OK'),
              ),
            ],
          );
        },
      );
    } else {
      // ignore: use_build_context_synchronously
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (ctx) => HomeScreen(
            user: name,
          ),
        ),
      );
    }
  }
}
