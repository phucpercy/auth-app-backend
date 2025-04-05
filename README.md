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

In developing the Auth App Backend, several critical design decisions were made to balance functionality, maintainability, and performance. This part outlines these decisions and the inherent trade-offs involved.

### 1. Project Structure: Modular Organization

**Decision**: Organize the project with distinct directories for source code (`src`) and tests (`tests`). 

**Trade-offs**:

- **Pros**:
  - Enhances code maintainability and readability.
  - Facilitates independent development and testing.

- **Cons**:
  - May introduce complexity in navigation for new developers. 
  - Requires consistent enforcement of organizational standards.

**Rationale**: The clear separation of concerns was deemed essential for scalability and collaborative development, outweighing the initial learning curve for new contributors. 

### 2. Dependency Management: `requirements.txt`

**Decision**: Manage project dependencies using a `requirements.txt` file.

**Trade-offs**:

- **Pros**:
  - Simplifies the setup process for new environments.
  - Ensures consistency across different development and production environments.

- **Cons**:
  - Requires manual updates to track changes in dependencies.
  - Lacks advanced features like dependency resolution provided by tools such as Poetry. 

**Rationale**: The simplicity and widespread familiarity of `requirements.txt` were favored to streamline onboarding and deployment processes.

### 3. Testing Framework: `pytest`

**Decision**: Implement testing using the `pytest` framework.

**Trade-offs**:

- **Pros**:
  - Offers a simple syntax and powerful features for writing tests.
  - Supports fixtures and plugins, enhancing test capabilities.

- **Cons**:
  - Introduces an additional dependency.
  - May require learning for developers unfamiliar with the framework.

**Rationale**: The robustness and ease of use of `pytest` were considered beneficial for maintaining high code quality and facilitating test-driven development. 

## 4. Security Considerations: Token Handling

**Decision**: Implement token-based authentication for securing the application.

**Trade-offs**:

- **Pros**:
  - Enhances security by avoiding the need to store sensitive session data on the client side.
  - Facilitates scalability by allowing stateless authentication mechanisms.

- **Cons**:
  - Requires careful handling of tokens to prevent security vulnerabilities.
  - May introduce complexity in managing token expiration and refresh mechanisms.

**Rationale**: Adopting token-based authentication aligns with modern security best practices and supports the application's scalability requirements. 

### 5. Token Strategy: From Single Token to Dual Token System

**Initial Decision**: Use a single token (typically an access token) for fast MVP development.

**Pros of Initial Approach**:
- Simplifies authentication logic during early development.
- Reduces the number of moving parts and speeds up prototyping.
- Easier for developers to implement and debug.

**Cons**:
- The access token typically has a short lifespan; reusing it for refresh purposes can pose security risks.
- Lack of a separate refresh token makes maintaining long sessions more difficult and can lead to user frustration with frequent logouts.
- Vulnerable to token theft scenarios without a secure token refresh mechanism.

**Refactored Decision**: When time allowed, migrate to a dual-token system — short-lived access tokens and long-lived refresh tokens.

**Trade-offs**:
- **Pros**:
  - Enhances security by limiting the exposure window of the access token.
  - Allows seamless user experience with silent token refresh without re-authentication.
  - Follows industry best practices for scalable and secure session management.

- **Cons**:
  - Increases complexity in token lifecycle management and storage.
  - Requires careful design to securely store refresh tokens (especially on the client side).
  - Adds extra logic for refreshing tokens and handling token expiration.

**Rationale**: While the initial single-token setup accelerated development and testing, the move to a dual-token architecture was essential for production readiness. It balances security and user experience by ensuring sessions can persist securely without compromising access control.

## 6. Real-time Communication: Use of WebSockets

**Decision**: Implement WebSocket protocol for real-time communication between the client and server.

**Trade-offs**:

- **Pros**:
  - Enables bi-directional, low-latency communication, ideal for real-time features like notifications, session monitoring, or live updates.
  - Reduces the need for constant HTTP polling, improving efficiency and responsiveness.
  - Enhances user experience through instant feedback mechanisms.

- **Cons**:
  - Introduces added complexity in backend infrastructure and client handling.
  - Requires careful handling of authentication, connection lifecycle, and fallbacks for disconnected clients.
  - Can be more difficult to scale horizontally compared to stateless HTTP endpoints.

**Rationale**: The decision to use WebSockets reflects a need for responsive, interactive client-server communication that cannot be easily achieved with standard REST APIs. Despite the added complexity, the real-time capabilities it provides significantly enhance the user experience for authentication events or live updates.

---

*Note: These decisions are based on the current scope and requirements of the project. As the project evolves, continuous evaluation and adaptation of these choices may be necessary to address emerging challenges and opportunities.
