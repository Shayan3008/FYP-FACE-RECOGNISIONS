import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/HomeScreen.dart';
import 'package:fyp_app/Screens/Signup.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    TextEditingController userName = TextEditingController();
    TextEditingController password = TextEditingController();
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      body: SafeArea(
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
                FractionallySizedBox(
                  widthFactor: 1.0,
                  child: Column(
                    children: [
                      TextField(
                        controller: userName,
                        decoration: const InputDecoration(
                          labelText: 'Name',
                        ),
                      ),
                      TextField(
                        controller: password,
                        decoration: const InputDecoration(
                          labelText: 'Password',
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
                      if (userName.text.isNotEmpty)
                        {
                          Navigator.of(context).pushReplacement(
                            MaterialPageRoute(
                              builder: (ctx) => HomeScreen(
                                user: userName.text,
                              ),
                            ),
                          )
                        }
                    },
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
    );
  }
}
