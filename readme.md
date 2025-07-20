# ✈️ Airport Booking API System 

A backend flight booking system designed for airport travel, built using **FastAPI**, **Python**, and **MySQL** with SQLAlchemy ORM. This system simulates a real-life ticket booking experience, including user account management, flight classes, booking flow, and flight status handling.



---

## 📊 Features

- 🔐 **JWT-based Login Authentication**
- 🔒 **Secure password storage** using `bcrypt`
- 📆 **Flight booking with return trip support**
- 🛋️ **4 flight classes** (Economy, Premium, Business, First)
- ⏳ **Flight status tracking** (Pending, Boarding, On-time, Delayed, Cancelled)
- 📂 **6 MySQL Tables** with proper relationships and nested responses
- ✅ **CRUD operations** for each resource
- ✏️ **Input validation** via Pydantic
- ✅ **Full RESTful API** using FastAPI
- 📊 **Tested via Postman and Swagger UI**

---

## 📄 API Routers

### 🔑 Login

`/login`

- Handles user authentication (email + password)
- Returns JWT token with user role

### 💼 Accounts

`/accounts`

- **POST**: Register new account
- **GET**: Get all accounts (admin)
- **GET/PUT/PATCH/DELETE** `/accounts/{account_id}`: Manage individual accounts

### 👤 Account Info

`/accounts/{account_id}/info`

- **GET/POST/PUT/PATCH/DELETE**: Manage user profile information
- Tightly coupled with account table via foreign key

### 🏧 Airports

`/airports`

- **GET/POST/PUT/DELETE**: Manage airport entries
- Required for booking departure and arrival info

### 🛋️ Classes

`/classes`

- **GET/POST/PUT/DELETE**: Manage flight class types (economy, business, etc.)

### 💳 Bookings

`/accounts/{account_id}/bookings`

- **POST**: Book a flight (one-way or return)
- **GET**: View all bookings by account
- **PUT/PATCH/DELETE**: Manage bookings

### ✈️ Flights

`/accounts/{account_id}/bookings/{booking_id}/flights`

- **GET/POST/PUT/PATCH/DELETE**: Manage individual flights inside bookings

---

## 🤝 Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Security**: bcrypt
- **Auth**: JWT
- **Testing**: Postman, FastAPI Swagger Docs

---

## 🔍 Sample Enums (SQLAlchemy)

```python
class ClassEnum(enum.Enum):
    economy = "economy"
    premium = "premium"
    business = "business"
    first = "first"

class FlightStatus(enum.Enum):
    pending = "pending"
    boarding = "boarding"
    on_time = "on_time"
    delayed = "delayed"
    cancelled = "cancelled"
```

---

## 📅 Future Additions

- 📅 Real-time flight updates
- 🌐 Frontend UI (React or Vue)
- 💵 Payment gateway integration
- ✅ Admin dashboard for flight and airport management

---

## 🌐 Swagger UI

Once running, access interactive API docs via:

```
http://localhost:8000/docs
```

---

## 🔢 Sample Folder Structure

```bash
app/
├── diagram/
├── routers/
├── body.py
├── config.py
├── database.py
├── main.py
├── models.py
├── oauth2.py
├── queries.py
├── response.py
├── status_codes.py
├── updates.py
└── utils.py
```

---

## 🤔 Why I Built This

This project was inspired by a real-life travel event involving my girlfriend's family vacation to Japan. I used this opportunity to explore SQLAlchemy ORM, proper relationship modeling, and simulate a real-world airport booking system.

---

## 🔗 Authentication

- **JWT Bearer Token** stored in headers for protected routes
- Login returns token + user role

---

## 🌍 How to Run

```bash
python -m venv venv
source venv/bin/activate.bat  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📖 feel free to fork, clone, modify, and contribute!

