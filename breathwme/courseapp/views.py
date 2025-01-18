from django.shortcuts import render , get_object_or_404
from .models import Course
from .models import Quiz
import csv


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    # Get the course with its materials
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all().order_by('order')
    
    # Fetch the quizzes for this course
    quizzes = course.quizzes.all()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'materials': materials,
        'quizzes': quizzes
    })

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Quiz
import csv

from django.shortcuts import render, get_object_or_404
import csv

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import Quiz

from django.shortcuts import render, get_object_or_404
from .models import Quiz

from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz

# views.py
from django.shortcuts import render, redirect, get_object_or_404
import csv
from .models import Quiz

from django.shortcuts import render, get_object_or_404
from .models import Quiz
import csv

from django.shortcuts import render, get_object_or_404
from .models import Quiz
import csv

from django.shortcuts import render, get_object_or_404
from .models import Quiz
import csv

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []

    # Read quiz file if exists
    if quiz.quiz_file:
        with open(quiz.quiz_file.path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for idx, row in enumerate(reader, start=1):
                question_text, option1, option2, option3, option4, correct_answer = row
                options = [option1, option2, option3, option4]
                questions.append({
                    'question_number': idx,
                    'question_text': question_text,
                    'options': options,
                    'correct_answer': correct_answer  # Store the correct answer text
                })

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)

        # Process the form data
        for index, question in enumerate(questions):
            selected_answer = request.POST.get(f'question_{index + 1}')  # Get selected answer

            # Debugging: print the selected and correct answers
            print(f"Selected answer for question {index + 1}: {selected_answer}")
            print(f"Correct answer for question {index + 1}: {question['correct_answer']}")

            if selected_answer:
                # Compare selected answer with the correct one (text match)
                if selected_answer == question['correct_answer']:
                    score += 1

        # Calculate percentage
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Debugging: print the final score
        print(f"Final score: {score}")
        print(f"Percentage: {percentage}%")

        # Redirect to results page or render results directly
        return render(request, 'courses/quiz_results.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage': round(percentage, 2),
        })

    return render(request, 'courses/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Retrieve results from session
    score = request.session.get('score', 0)
    total_questions = request.session.get('total_questions', 0)
    percentage = request.session.get('percentage', 0.0)

    return render(request, 'courses/quiz_result.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage
    })
