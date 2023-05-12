import 'package:fyp_app/utility/cookie.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SharedPreferenceData {
  late SharedPreferences _data;
  late Cookie cookie;
  Future<void> _instantiate() async {
    _data = await SharedPreferences.getInstance();
    cookie = Cookie();
  }

  SharedPreferenceData() {
    _instantiate();
  }

  Future<void> _storeCookie(String? cookie) async {
    await _data.setString('cookie', cookie!);
  }

  Future<String> getCookie() async {
    if (_data.getString('cookie') == null) {
      _storeCookie(await cookie.getCookie());
    }
    return _data.getString('cookie')!;
  }
}
