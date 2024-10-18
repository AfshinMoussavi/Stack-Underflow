# Stack Underflow

Welcome to **Stack Underflow**, a Q&A platform similar to Stack Overflow, where users can ask questions, provide answers, upvote, downvote, and interact with the community.

## Features
- **User Authentication**: Sign up, log in, and manage your profile.
- **Ask Questions**: Post technical questions and get answers from the community.
- **Answer Questions**: Share your knowledge by answering existing questions.
- **Upvote/Downvote**: Engage with the community by upvoting or downvoting questions and answers.
- **Tagging System**: Organize and search questions by tags.
- **Recent Questions**: View questions that were asked within the last 5 minutes.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- Django
- Git
- A virtual environment tool (such as `virtualenv`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AfshinMoussavi/Stack-Underflow.git
   ```
2. **Navigate to the project directory:
  ```bash
  cd Stack-Underflow
```

3. **Create and activate a virtual environment:
  ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    
    # For MacOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
```
4. **Install the dependencies:
  ```bash
    pip install -r requirements.txt
  ```

5. **Run database migrations:
  ```bash
  python manage.py migrate
```

6. **Load sample data:
To get started with pre-populated data, load the initial.json file into your database:
  ```bash
  python manage.py loaddata initial_data.json
```

7. **Run the development server:
  ```bash
  python manage.py runserver
```

8. **Open your browser and navigate to http://127.0.0.1:8000 to start using Stack Underflow!



  











