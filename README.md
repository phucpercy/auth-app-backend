# Auth App Backend

This repository contains the backend implementation for an authentication application. It is built using Python and includes the necessary components to handle user authentication processes.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Application Locally](#running-the-application-locally)
- [Testing](#testing)
- [Design Decisions and Trade-offs](#design-decisions-and-trade-offs)
  - [Use of Python](#use-of-python)
  - [Project Structure](#project-structure)
  - [Dependency Management](#dependency-management)
  - [Testing Strategy](#testing-strategy)

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional but recommended)

## Setup Instructions

### Cloning the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/phucpercy/auth-app-backend.git
cd auth-app-backend
```

### Setting Up the Virtual Environment
It's advisable to use a virtual environment to manage dependencies. You can set it up using the following commands:

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Installing Dependencies
Once the virtual environment is activated, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### Set up the enviroment variables
Create a `.env` file in the root directory of the project and add the following environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost/db_name
SECRET_KEY=your_secret_key
ALGORITHM=your_algorithm # e.g., HS256
ACCESS_TOKEN_EXPIRE_MINUTES=your_access_token_expiration_time # e.g., 3
REFRESH_TOKEN_EXPIRE_MINUTES=your_refresh_token_expiration_time # e.g., 3000
BACKEND_CORS_ORIGINS=your_allowed_origin # e.g., ["http://localhost:3000","http://localhost:5173"]```
```

### Running the Application Locally
To run the application locally, use the following command to start the FastAPI server:

```bash
uvicorn src.main:app --reload --port 8080
```

## Testing
To run the tests, ensure you have pytest installed. It is recommended to have a spare database for testing.

You can run the tests using the following command:

```bash
pytest
```

## Design Decisions and Trade-offs
