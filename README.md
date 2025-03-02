# Flask Application for Booking System and Inventory/Member upload

This Flask-based application manages member bookings for items from an inventory. Members can book and cancel items, 
and the app supports uploading member and inventory data from CSV files.

## Features

- **Book an item**: Members can book an available item from the inventory.
- **Cancel a booking**: Members can cancel their bookings.
- **Upload Members and Inventory**: Upload member and inventory data from CSV files.
- **Date Validation**: The app validates the date formats for both member join date and inventory expiration date.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.10+**: The app is built using Python 3.10 or later.
- **pip**: Python's package installer.

You can check your Python version with:

```bash
python --version
```

# 1. Clone the Repository
```
git clone https://github.com/utkarshSUV/TravelBooking.git
cd TravelBooking
```

# 2. Set Up a Virtual Environment (Recommended)
To keep the project dependencies isolated, it’s recommended to use a virtual environment.
On macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

On windows:
```
python -m venv venv
.\venv\Scripts\activate
```

# 3. Install Dependencies
```
pip install -r requirements.txt
```

# 4. Set Up the Database (Not needed)
I have created a free DB instance on a website(https://replit.com/) which is already running so you can skip this part.
Also If you want to connect/clone the DB instance on your system then here is the **database_uri = "postgresql://neondb_owner:npg_VKbztk8GN2Je@ep-super-mode-a4emkx94.us-east-1.aws.neon.tech:5432/neondb"**
NOTE:- If you face any issues with the DB connection then let me know

# 5.Run the Application
If all the requirements were installed properly then you can simply run the flask app with the below command
```
flask run
```

# NOTE:- The postgres instance is under a free tier subscription and it takes few seconds to hot reload after inactivity. You may experience delay in the first API response, subsequent API calls should work fine.
 
