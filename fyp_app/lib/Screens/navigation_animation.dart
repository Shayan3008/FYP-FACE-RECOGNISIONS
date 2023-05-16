import 'dart:math' show pi;

import 'package:flutter/material.dart';
import 'package:fyp_app/Screens/user_details.dart';
import 'package:fyp_app/configs/size_config.dart';

class NavbarAnimation extends StatefulWidget {
  final Widget child;
  const NavbarAnimation({super.key, required this.child});

  @override
  State<NavbarAnimation> createState() => _NavbarAnimationState();
}

// A higher order Widget which takes child as input and give animation with drawer

class _NavbarAnimationState extends State<NavbarAnimation>
    with TickerProviderStateMixin {
  late AnimationController _xControllerForChild;
  late Animation<double> _yRotationAnimationForChild;

  late AnimationController _xControllerForDrawer;
  late Animation<double> _yRotationAnimationForDrawer;
  @override
  void dispose() {
    _xControllerForChild.dispose();
    _xControllerForDrawer.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _xControllerForChild = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
    _yRotationAnimationForChild = Tween<double>(
      begin: 0,
      end: -pi / 2,
    ).animate(_xControllerForChild);

    _xControllerForDrawer = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
    _yRotationAnimationForDrawer = Tween<double>(
      begin: pi / 2.7,
      end: 0,
    ).animate(_xControllerForDrawer);

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    SizeConfig().init(context);
    return AnimatedBuilder(
      animation: Listenable.merge([
        _xControllerForChild,
        _xControllerForDrawer,
      ]),
      builder: (context, child) {
        return GestureDetector(
          onTap: () {
            _xControllerForChild.forward();
            _xControllerForDrawer.forward();
          },
          onHorizontalDragUpdate: (DragUpdateDetails details) {
            final delta = details.delta.dx / SizeConfig.screenWidth! * 0.8;
            _xControllerForChild.value += delta;
            _xControllerForDrawer.value += delta;
          },
          onHorizontalDragEnd: (DragEndDetails details) {
            if (_xControllerForChild.value < 0.5) {
              _xControllerForChild.reverse();
              _xControllerForDrawer.reverse();
            } else {
              _xControllerForChild.forward();
              _xControllerForDrawer.forward();
            }
          },
          // onTap: () {
          //   if (_xControllerForChild.isCompleted) {
          //     _xControllerForChild.reverse();
          //     _xControllerForDrawer.reverse();
          //   } else {
          //     _xControllerForChild.forward();
          //     _xControllerForDrawer.forward();
          //   }
          // },
          child: SafeArea(
            child: Stack(
              children: [
                Container(
                  color: Colors.grey,
                  child: Align(
                      alignment: Alignment.topRight,
                      child: GestureDetector(
                        onTap: () {
                          _xControllerForChild.reverse();
                          _xControllerForDrawer.reverse();
                        },
                        child: const Icon(
                          Icons.cancel,
                          color: Colors.white,
                          size: 40,
                        ),
                      )),
                ),
                Transform(
                  alignment: Alignment.centerLeft,
                  transform: Matrix4.identity()
                    ..setEntry(3, 2, 0.001)
                    ..translate(_xControllerForChild.value *
                        (SizeConfig.screenWidth! * 0.8))
                    ..rotateY(_yRotationAnimationForChild.value),
                  child: widget.child,
                ),
                Transform(
                  alignment: Alignment.centerRight,
                  transform: Matrix4.identity()
                    ..setEntry(3, 2, 0.001)
                    ..translate(-SizeConfig.screenWidth! +
                        _xControllerForDrawer.value *
                            (SizeConfig.screenWidth! * 0.8))
                    ..rotateY(
                      _yRotationAnimationForDrawer.value,
                    ),
                  child: Scaffold(
                    backgroundColor: Colors.blueGrey,
                    body: Padding(
                      padding: const EdgeInsets.all(100.0),
                      child: Row(
                        children: [
                          Column(
                            // crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              const Text(
                                'Home',
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 30,
                                    fontWeight: FontWeight.bold),
                                textAlign: TextAlign.center,
                              ),
                              SizedBox(
                                height: SizeConfig.screenHeight! * 0.05,
                              ),
                              InkWell(
                                onTap: () => {
                                  _xControllerForChild.reset(),
                                  _xControllerForDrawer.reset(),
                                  Navigator.of(context).push(
                                    MaterialPageRoute(
                                      builder: (context) =>
                                          const NavbarAnimation(
                                        child: UserDetails(
                                            userName: "Shayan",
                                            email: "shayanjawed4@gmail.com"),
                                      ),
                                    ),
                                  )
                                },
                                child: const Text(
                                  'Details',
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 30,
                                      fontWeight: FontWeight.bold),
                                  textAlign: TextAlign.center,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
