# 📚 Studyer – Study Group Web App

**Studyer** is a Django-based web application that allows users to create and join study rooms based on shared interests and topics. It's designed to help students and developers collaborate, communicate, and learn together in real time.

---

## 🧠 Key Features

- **👤 User Authentication**  
  Custom user model with email-based login, bios, and avatars.

- **🧵 Topic Categorization**  
  Users can browse or filter study rooms by subject (e.g., Web Development, Python, Django, etc.).

- **📌 Room Creation & Participation**  
  Users can create, join, or leave study rooms and engage in group discussions.

- **💬 Messaging System**  
  Real-time room-based chat functionality to share ideas and resources.

- **📊 Activity Feed**  
  Shows recent replies, room posts, and discussions for better engagement.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Authentication:** Django’s AbstractUser with custom fields  
- **Database:** SQLite (Dev), can be extended to PostgreSQL or MySQL  
- **Upcoming:** Django REST Framework (for API access)

---

## 📂 Project Structure

```

Studyer/
├── static/              # CSS, JS, images
├── templates/           # HTML templates (Jinja-based)
├── studyer/             # Core Django app with models, views, urls
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation

````

---

## 📦 Installation

1. Clone the repository


2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🌐 Planned Enhancements

* ✅ REST API support using Django REST Framework (DRF)
* ✅ Mobile-friendly user interface
* ⏳ Enhanced user dashboard with profile editing and activity summaries
* ⏳ Notifications and tagging features in chat

---

## 👨‍💻 Developed By

**Abdullah**
[GitHub](https://github.com/abd027) | [LinkedIn](https://www.linkedin.com/in/abdullah-3940471b9)

---

## 📃 License

This project is open-source and free to use for educational purposes.


