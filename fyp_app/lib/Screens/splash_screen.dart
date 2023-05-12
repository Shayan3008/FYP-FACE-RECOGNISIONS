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
                Container(
                  color: Colors.red,
                ),
                ClipPath(
                  clipper: Clipper(),
                  child: Container(
                    height: SizeConfig.screenHeight! * 0.5,
                    color: Colors.blue,
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
