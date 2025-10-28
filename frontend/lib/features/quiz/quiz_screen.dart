import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'quiz_provider.dart';
import '../../widgets/quiz_option_tile.dart';

/// Quiz screen for answering MCQ questions
/// 
/// Features:
/// - Display clinical vignette questions
/// - Four option selection
/// - Timer for response time tracking
/// - Immediate feedback after submission
class QuizScreen extends ConsumerStatefulWidget {
  final int topicId;
  
  const QuizScreen({
    super.key,
    required this.topicId,
  });

  @override
  ConsumerState<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends ConsumerState<QuizScreen> {
  String? _selectedOption;
  DateTime? _questionStartTime;
  
  @override
  void initState() {
    super.initState();
    _questionStartTime = DateTime.now();
    // Load quiz questions
    Future.microtask(() {
      // TODO: Load quiz for topic
      // ref.read(quizProvider.notifier).loadQuiz(topicId: widget.topicId);
    });
  }
  
  void _submitAnswer() {
    if (_selectedOption == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('لطفاً یک گزینه را انتخاب کنید')),
      );
      return;
    }
    
    // Calculate response time
    final responseTime = DateTime.now().difference(_questionStartTime!).inSeconds.toDouble();
    
    // TODO: Submit answer
    // ref.read(quizProvider.notifier).submitAnswer(
    //   questionId: currentQuestion.questionId,
    //   chosenOption: _selectedOption!,
    //   responseTimeSec: responseTime,
    // );
  }
  
  @override
  Widget build(BuildContext context) {
    // TODO: Watch quiz provider state
    // final quizState = ref.watch(quizProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('تست'),
        actions: [
          // Question counter
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                '۱/۵',  // TODO: Use actual question count
                style: const TextStyle(fontSize: 16),
              ),
            ),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Question stem (clinical vignette)
            Expanded(
              child: SingleChildScrollView(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'سوال',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 12),
                        // TODO: Display actual question stem
                        const Text(
                          'کودک ۸ ساله با تشنگی شدید، تنفس عمیق و سریع (کوسماول)، و سطح هوشیاری کاهش یافته به اورژانس مراجعه می‌کند. قند خون ۴۵۰ mg/dL، کتون ادراری ++++، و pH خون ۷.۱۵ است. اولین اقدام درمانی کدام است؟',
                          style: TextStyle(fontSize: 16, height: 1.6),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            
            // Options
            // TODO: Map through actual options
            QuizOptionTile(
              label: 'الف',
              text: 'نرمال سالین سریع وریدی',
              isSelected: _selectedOption == 'A',
              onTap: () => setState(() => _selectedOption = 'A'),
            ),
            const SizedBox(height: 8),
            QuizOptionTile(
              label: 'ب',
              text: 'انسولین بولوس فوری',
              isSelected: _selectedOption == 'B',
              onTap: () => setState(() => _selectedOption = 'B'),
            ),
            const SizedBox(height: 8),
            QuizOptionTile(
              label: 'ج',
              text: 'بیکربنات سدیم وریدی',
              isSelected: _selectedOption == 'C',
              onTap: () => setState(() => _selectedOption = 'C'),
            ),
            const SizedBox(height: 8),
            QuizOptionTile(
              label: 'د',
              text: 'گلوکز هایپرتونیک',
              isSelected: _selectedOption == 'D',
              onTap: () => setState(() => _selectedOption = 'D'),
            ),
            const SizedBox(height: 24),
            
            // Submit button
            ElevatedButton(
              onPressed: _submitAnswer,
              child: const Text('ثبت پاسخ'),
            ),
          ],
        ),
      ),
    );
  }
}
