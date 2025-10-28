import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'auth_provider.dart';

/// Login screen with OTP authentication
///
/// Flow:
/// 1. User enters phone number
/// 2. Request OTP
/// 3. User enters OTP code
/// 4. Verify OTP and navigate to dashboard
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _phoneController = TextEditingController();
  final _otpController = TextEditingController();
  bool _otpSent = false;
  bool _isLoading = false;

  @override
  void dispose() {
    _phoneController.dispose();
    _otpController.dispose();
    super.dispose();
  }

  Future<void> _requestOTP() async {
    // TODO: Implement OTP request
    setState(() {
      _isLoading = true;
    });

    try {
      // Call auth provider to request OTP
      // await ref.read(authProvider.notifier).requestOTP(_phoneController.text);

      setState(() {
        _otpSent = true;
        _isLoading = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('کد تایید ارسال شد')),
        );
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('خطا: ${e.toString()}')),
        );
      }
    }
  }

  Future<void> _verifyOTP() async {
    // TODO: Implement OTP verification
    setState(() {
      _isLoading = true;
    });

    try {
      // Call auth provider to verify OTP
      // await ref.read(authProvider.notifier).verifyOTP(
      //   _phoneController.text,
      //   _otpController.text,
      // );

      setState(() {
        _isLoading = false;
      });

      // Navigate to dashboard on success
      // if (mounted) {
      //   Navigator.of(context).pushReplacement(
      //     MaterialPageRoute(builder: (context) => const DashboardScreen()),
      //   );
      // }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('خطا: ${e.toString()}')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Logo/Title
                Text(
                  'AdaptiveMed',
                  style: Theme.of(context).textTheme.displayLarge,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'پلتفرم یادگیری هوشمند برای دانشجویان پزشکی',
                  style: Theme.of(context).textTheme.bodyMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),

                // Phone number input
                TextField(
                  controller: _phoneController,
                  decoration: const InputDecoration(
                    labelText: 'شماره موبایل',
                    hintText: '09123456789',
                    prefixIcon: Icon(Icons.phone),
                  ),
                  keyboardType: TextInputType.phone,
                  textDirection: TextDirection.ltr,
                  enabled: !_otpSent,
                ),
                const SizedBox(height: 16),

                // OTP input (shown after OTP is sent)
                if (_otpSent) ...[
                  TextField(
                    controller: _otpController,
                    decoration: const InputDecoration(
                      labelText: 'کد تایید',
                      hintText: '123456',
                      prefixIcon: Icon(Icons.lock),
                    ),
                    keyboardType: TextInputType.number,
                    textDirection: TextDirection.ltr,
                    maxLength: 6,
                  ),
                  const SizedBox(height: 16),
                ],

                // Action button
                ElevatedButton(
                  onPressed:
                      _isLoading ? null : (_otpSent ? _verifyOTP : _requestOTP),
                  child: _isLoading
                      ? const CircularProgressIndicator()
                      : Text(_otpSent ? 'تایید کد' : 'ارسال کد تایید'),
                ),
              ],
            ),
          ),
        ),
      );
}
