# Django Web Application

This is a web application built with Django, providing functionality for user authentication, product management, and orders. The app includes a fully functional customer interface, product listings, and an admin panel for managing users and products.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating a Virtual Environment](#creating-a-virtual-environment)
3. [Installing Dependencies](#installing-dependencies)
4. [Applying Migrations](#applying-migrations)
5. [Seeding the Database](#seeding-the-database)
6. [Creating a Superuser](#creating-a-superuser)
7. [Running the Application](#running-the-application)
8. [Accessing the App](#accessing-the-app)

---

## Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

- Python 3.8+

---

## Creating a Virtual Environment

It’s highly recommended to run this app inside a virtual environment. Here’s how to create and activate a virtual environment cross-platform:

### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Installing Dependencies

After activating the virtual environment, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries and packages listed in the `requirements.txt` file.

---

## Applying Migrations

Once the dependencies are installed, you need to apply the migrations to set up your database schema.

Run the following commands in your terminal:

```bash
python manage.py makemigrations
python manage.py makemigrations core
python manage.py migrate
```

These commands will create and apply the necessary migrations to your database.

---

## Seeding the Database (Optional)

If you want to seed your database with some dummy data (e.g., users, products), you can run the seed command:

```bash
python manage.py seed
```

This will fill the database with pre-configured dummy data to get you started.

---

## Creating a Superuser

To access the Django admin panel, you’ll need to create an admin account. Run the following command and follow the prompts:

```bash
python manage.py createsuperuser
```

Provide the required information (username, email, password), and the admin account will be created.

---

## Running the Application

After completing all the previous steps, you can run the development server using:

```bash
python manage.py runserver
```

This will start the app, and you can now access it in your browser.

---

## Accessing the App

Once the server is running, you can access the app and the admin panel at the following URLs:

- **Customer Interface:** [http://localhost:8000/](http://localhost:8000/)
- **Admin Panel:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Use the superuser credentials you created earlier to log in to the admin panel.

---

### Notes:

- Ensure your virtual environment is activated before running any commands.
- The seeding process will add the following users, each of them with the password `pass`

user1@gmail.com
user2@gmail.com
user3@gmail.com
user4@gmail.com
user5@gmail.com
user6@gmail.com
user7@gmail.com
user8@gmail.com
user9@gmail.com
user10@gmail.com
