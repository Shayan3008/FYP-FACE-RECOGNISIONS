import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/HomeScreen.dart';
import 'package:fyp_app/Screens/Signup.dart';
import 'package:fyp_app/models/User.dart';
import 'package:fyp_app/utility/ValidationChecks.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool userValidation = false;
  bool emailValidation = false;
  bool passValidation = false;
  @override
  Widget build(BuildContext context) {
    TextEditingController userName = TextEditingController();
    TextEditingController email = TextEditingController();
    TextEditingController password = TextEditingController();
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
                              labelText: 'email',
                              errorText: emailValidation == true
                                  ? "Enter Valid Email"
                                  : null,
                            ),
                          ),
                          TextField(
                            controller: password,
                            decoration: InputDecoration(
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
                        onPressed: () async => loginMethod(
                          email.text,
                          password.text,
                          context,
                        ),
                        child: const Text(
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

  void loginMethod(String email, String password, BuildContext context) {
    setState(() {
      emailValidation = email.isEmpty || !isValidEmail(email);
      passValidation = password.length < 6;
    });
    if (emailValidation || passValidation) {
      Future.delayed(const Duration(seconds: 5), (() {
        setState(() {
          emailValidation = false;
          passValidation = false;
        });
      }));
      return;
    }
    User user = User("", email, password);
    print(user.LoginUser());
    // Navigator.of(context).pushReplacement(
    //   MaterialPageRoute(
    //     builder: (ctx) => HomeScreen(
    //       user: email,
    //     ),
    //   ),
    // );
  }
}
