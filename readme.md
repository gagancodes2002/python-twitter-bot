# Django Todo App

This is a simple Todo app built using Django. The app allows users to create, edit, complete and delete tasks. The app also allows the user to filter tasks by status. The app uses Django's built-in message framework to display success, error and info messages to the user. This version of the app does not include any session-based or authentication features, so all tasks will appear in one place and may be accessible to all users. 

The app's front-end template is a modified version of the "todo-list" project created by - [Abdellatif Laghjaj](https://github.com/abdellatif-laghjaj) and available on Github [here](https://github.com/abdellatif-laghjaj/todo-list).

## Screenshots
![App Screenshot](/screenshot/todo-photo-1.png)
![App Screenshot](/screenshot/completed-task-filter-2.png)
![App Screenshot](/screenshot/pending-task-filter-3.png)


## Features
- Create a new task
- Mark a task as completed or uncompleted
- Edit an existing task
- Delete a task
- Delete all tasks
- Filter tasks by status
- Display success, error and info messages to the user

## Requirements
- Python 3.x
- Django 3.x

## Setup
1. Clone the repository

    `https://github.com/jethliya-balaji/Django-Todo-App.git`

2. Install the requirements

    `pip install -r requirements.txt`

3. Run migrations

    `python manage.py makemigrations`

    `python manage.py migrate`

4. Run the development server

    `python manage.py runserver`
    
5. Visit http://127.0.0.1:8000/ in your browser to access the app

## Code Structure
The code is structured as follows:
- The `models.py` file contains the Todo models
- The `forms.py` file contains the TodoForm and TodoFilterForm
- The `views.py` file contains the views for the app
- The `urls.py` file contains the URL patterns for the app
- The `templates` directory contains the HTML templates for the app
- The `static` directory contains the static files for the app (CSS, JS, etc)

## Customization
You can customize the app to suit your needs by editing the templates and styles in the `templates` and `static` directories respectively.

## Contribution
If you want to contribute to this project, please fork the repository and create a pull request with your changes. You can add new features like session-based or authentication based task storage, adding task priority, adding notes to task, etc.

## Support
If you need any help or have any questions, please feel free to contact me.

## Note
As this version of the app does not include any session-based or authentication features, it's recommended to use it in a development environment only and not in production.

## Conclusion
The app is a great starting point for anyone looking to build a simple Todo app using Django. It demonstrates the use of Django's built-in message framework and the use of forms to handle user input. The app is easy to customize and extend to suit your needs.

## Fun Section
The web site is up and running [here]() but it may be temporarily down because the developer needs a coffee break. If you find the app helpful, feel free to buy the developer a coffee!

## Authors
Balaji Jethliya - Initial work - [GitHub](https://github.com/jethliya-balaji), [Twitter](https://twitter.com/jethliyabalaji)
