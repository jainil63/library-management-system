# LIBIFY - Library Management System

LIBIFY is a comprehensive library management system designed to assist library administrators in efficiently managing their libraries. The system ensures ease of use, secure data handling, and a robust platform for both users and administrators.

---

## Features

### Core Features:
- [ ] **Homepage**: A welcoming interface showcasing the library's information and offerings.
- [ ] **User Dashboard**: Personalized dashboard for library users to:
  - Browse and search books.
  - View borrowed books.
  - Manage their account details.
- [ ] **Admin Dashboard**: An intuitive dashboard for administrators to:
  - Manage book inventory (add, remove, or edit books).
  - Handle user accounts.
  - Monitor borrowing and return activities.
- [ ] **REST API**: Developed using **FastAPI** to enable seamless communication between the frontend and backend systems.
- [ ] **Secure Authorization & Authentication**: Implementation of:
  - Role-based access control (RBAC).
  - Password encryption and session management.
- [ ] **Data Persistence**: Local database to ensure reliable and efficient storage of library data.

---

## Technologies Used

### Frontend:
- **HTML**: Structuring the web pages.
- **CSS**: Styling and enhancing the visual appeal.
- **JavaScript**: Enabling interactivity and dynamic content.

### Backend:
- **FastAPI**: A modern web framework for building APIs with Python.

### Database:
- **Local Database**: Lightweight and efficient storage solution for development and production needs.

---

## How to Run the Project

### Prerequisites:
1. Install [Python 3.11+](https://www.python.org/downloads/).
2. Install the required libraries.
   

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/jainil63/library-management-system.git
   ```

2. Navigate to the project directory:
   ```bash
   cd library-management-system
   ```

3. Install the required libraries
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   uvicorn backend:app --host 127.0.0.1 --port 8080
   ```
   OR
   ```bash
   uvicorn backend.app:app --host 127.0.0.1 --port 8080
   ```

5. Open the `http://127.0.0.1:8080` in your preferred browser.
 
---

## Contributors

This project is made possible by the following contributors:

- [Jainil](https://github.com/jainil63)  
  _Frontend Developer_

- [Jeel](https://github.com/JeelDobariya38)  
  _Backend Developer_

We welcome contributions from the community! Feel free to submit issues or create pull requests to improve LIBIFY.

---

## License

This project is licensed under the [MIT License](LICENSE.txt). You are free to use, modify, and distribute this software in compliance with the license.

---

## Contact Us

For any queries or suggestions, feel free to reach out:
- **GitHub Issues**: [LIBIFY Issues](https://github.com/jainil63/library-management-system/issues)

---

Thank you for using LIBIFY! Let’s revolutionize library management together.

