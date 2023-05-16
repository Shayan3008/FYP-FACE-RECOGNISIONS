import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/login_screen.dart';

import '../configs/size_config.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _tween;
  late PageController _pageController;
  ScrollPhysics? physics;
  @override
  void initState() {
    print('Helo OW');
    _pageController = PageController(initialPage: 0);
    _animationController = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 500));
    _tween = Tween<double>(
      begin: 0,
      end: 1,
    ).animate(_animationController);
    _animationController.repeat();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    SizeConfig().init(context);
    return Scaffold(
      body: SafeArea(
        child: PageView(
          onPageChanged: (int page) {
            if (page == 1) {
              setState(() {
                physics = const NeverScrollableScrollPhysics();
              });
            }
          },
          controller: _pageController,
          physics: physics,
          children: [
            Stack(
              children: [
                Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Container(
                      margin: EdgeInsets.only(
                          bottom: 150, left: SizeConfig.screenWidth! / 4.5),
                      child: Column(
                        children: [
                          Text(
                            "Swipe to Login",
                            style: TextStyle(
                              fontSize: SizeConfig.horizantalAspect! * 8,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          Image.asset('assets/arrow.gif')
                        ],
                      ),
                    ),
                  ],
                ),
                ClipPath(
                  clipper: Clipper(),
                  child: Container(
                    height: SizeConfig.screenHeight! * 0.5,
                    color: const Color.fromARGB(255, 123, 196, 255),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Expanded(
                            child: Text(
                          "Welcome to Vigilant Watcher",
                          style: TextStyle(
                            fontSize: SizeConfig.horizantalAspect! * 8.5,
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        )),
                      ],
                    ),
                  ),
                )
              ],
            ),
            const LoginScreen(),
          ],
        ),
      ),
    );
  }
}

class Clipper extends CustomClipper<Path> {
  @override
  Path getClip(Size size) {
    var path = Path();
    path.lineTo(0, size.height / 2);
    path.cubicTo(size.width / 4, 3 * (size.height / 2), 3 * (size.width / 4),
        size.height / 2, size.width, size.height * 0.9);
    path.lineTo(size.width, 0);
    return path;
  }

  @override
  bool shouldReclip(covariant CustomClipper<Path> oldClipper) => true;
}
