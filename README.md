# Library Management Flask Web Application with SQLAlchemy

## SUMMARY
This readme provides an overview of a Flask web application that utilizes SQLAlchemy to manage books, users, and loans. Currently, the application allows you to list all books, users and loans, but it is a work in progress and lacks the ability to display, add, edit, or delete individual items through an html-based webpage, but can all be done through Thunder Client with a request.json file in VSCode or any similar tool.

## How to Install and Run the Project from GitHub

1. **Clone the Project Repository:**

   Open your terminal or command prompt and navigate to the directory where you want to store the project. Then, use the `git clone` command to clone the project repository from GitHub. Here's the command:

   ```bash
   git clone https://github.com/TotalWreck/Lib_proj.git
   ```

2. **Navigate to the Project Directory:**

   Change your current directory to the newly cloned project directory:

   ```bash
   cd Lib_proj
   ```

3. **Create a Virtual Environment (Optional but Recommended):**

   While not mandatory, it's a good practice to create a virtual environment to isolate your project's dependencies. This ensures that your project doesn't interfere with other Python installations on your system.

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Project Dependencies:**

   With your virtual environment activated, you can install the project's dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the necessary packages for your project.

5. **Run the Application:**

   You can now run the Flask application using the following command:

   ```bash
   python app.py
   ```

   The application will start, and you can access it in your web browser at `http://127.0.0.1:5000/`.

By following these steps, you'll successfully install and run the project from the GitHub repository on your local machine.

## Implemented Features

1. **List of Books:**

   - You can view a list of all books by navigating to `/books/list`.
   - The application successfully displays a list of books in HTML format.

2. **List of Users:**

   - You can view a list of all users by navigating to `/users/list`.
   - The application successfully displays a list of users in HTML format.

3. **List of Loans:**

   - You can view a list of all loans by navigating to `/loans/list`.
   - The application successfully displays a list of loans in HTML format.

## Not Yet Implemented

The following features have not been fully implemented in the current version of the application:

1. **Display a Single Book:**

   - The application lacks a feature to display a single book's details.

2. **Add a Book:**

   - There is no functionality to add a new book to the database.

3. **Edit a Book:**

   - The application does not allow you to edit or update information for existing books.

4. **Delete a Book:**

   - There is no functionality to delete books from the database.

5. **User Management:**

   - User-specific functionality, such as displaying a single user, adding, editing, or deleting users, is not yet implemented.

6. **Loan Management:**

   - Similar to users, there is no functionality to display, add, edit, or delete individual loans.