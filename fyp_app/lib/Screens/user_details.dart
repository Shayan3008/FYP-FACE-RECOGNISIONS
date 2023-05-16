import 'package:flutter/material.dart';
import 'package:fyp_app/configs/size_config.dart';

class UserDetails extends StatelessWidget {
  final String userName;
  final String email;
  const UserDetails({super.key, required this.userName, required this.email});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.only(top: 0),
          child: Column(
            children: [
              Container(
                color: Colors.blue,
                child: Padding(
                  padding: const EdgeInsets.only(left: 10, top: 5, bottom: 20),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          CircleAvatar(
                            radius: SizeConfig.verticalAspect! * 4.5,
                            child: Text(
                              userName[0].toUpperCase() +
                                  userName[1].toUpperCase(),
                            ),
                          ),
                          SizedBox(
                            width: SizeConfig.screenWidth! * 0.03,
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                userName,
                                style: TextStyle(
                                    fontSize: SizeConfig.verticalAspect! * 3,
                                    color: Colors.white),
                              ),
                              const Text(
                                "Edit Profile",
                                style: TextStyle(color: Colors.white),
                              ),
                            ],
                          ),
                        ],
                      ),
                      const Padding(
                        padding: EdgeInsets.only(right: 20),
                        child: Icon(
                          Icons.edit,
                          color: Colors.white,
                        ),
                      )
                    ],
                  ),
                ),
              ),
              SizedBox(
                height: SizeConfig.screenHeight! * 0.05,
              ),
              Card(
                child: SizedBox(
                  width: SizeConfig.screenWidth! * 0.95,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(20),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Account",
                              style: TextStyle(
                                  color: Colors.indigo,
                                  fontSize: SizeConfig.verticalAspect! * 2.5),
                            ),
                            SizedBox(
                              height: SizeConfig.screenHeight! * 0.009,
                            ),
                            Text(
                              email,
                              style: TextStyle(
                                  color: Colors.indigo,
                                  fontSize: SizeConfig.verticalAspect! * 2),
                            ),
                            SizedBox(
                              height: SizeConfig.screenHeight! * 0.003,
                            ),
                            Text(
                              "Email",
                              style: TextStyle(
                                  color: Colors.grey,
                                  fontWeight: FontWeight.w400,
                                  fontSize: SizeConfig.verticalAspect! * 2),
                            ),
                            SizedBox(
                              height: SizeConfig.screenHeight! * 0.009,
                            ),
                            Text(
                              userName,
                              style: TextStyle(
                                  color: Colors.indigo,
                                  fontSize: SizeConfig.verticalAspect! * 2),
                            ),
                            SizedBox(
                              height: SizeConfig.screenHeight! * 0.003,
                            ),
                            Text(
                              "User Name",
                              style: TextStyle(
                                  color: Colors.grey,
                                  fontWeight: FontWeight.w400,
                                  fontSize: SizeConfig.verticalAspect! * 2),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
