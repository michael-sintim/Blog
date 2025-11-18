from django.shortcuts import render
from .models import Post
# Create your tests here.

posts = [
    {
        'id': 1,
        'title': 'Introduction to Python Programming',
        'content': 'Python is a versatile programming language used for web development, data analysis, AI, and more.',
        'author': 'Alice Johnson',
        'date': '2024-01-15'
    },
    {
        'id': 2,
        'title': 'Getting Started with Django Framework',
        'content': 'Django is a high-level Python web framework that enables rapid development of secure websites.',
        'author': 'Bob Smith',
        'date': '2024-01-20'
    },
    {
        'id': 3,
        'title': 'React Basics for Beginners',
        'content': 'React is a JavaScript library for building user interfaces, particularly web applications.',
        'author': 'Carol Davis',
        'date': '2024-01-25'
    },
    {
        'id': 4,
        'title': 'Database Design Fundamentals',
        'content': 'Learn the basics of database design, normalization, and SQL queries for efficient data storage.',
        'author': 'David Wilson',
        'date': '2024-02-01'
    }
]


def home(request):
    context = {

        'posts':Post.objects.all()
    }
    return render(request, "home.html", context)


def about(request):
    return render(request,'About.html',{'title':'title'})