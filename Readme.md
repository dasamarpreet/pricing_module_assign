Please read this Build Instructions to run this project:

1. Open Terminal or Git Bash & Clone the Repository
$ git clone https://github.com/dasamarpreet/pricing_module.git
$ cd pricing_module

2. Set up Virtual Environment
$ python -m venv venv
$ source venv/Scripts/activate    # On Linux: venv\bin\activate

3. Install Dependencies
$ pip install -r requirements.txt

4. Set Up the Database (SQLite by default)
Run the migrations to set up the database schema:
$ python manage.py migrate

5. Create a Superuser for Admin Access
$ python manage.py createsuperuser

NOTE: For the ease, I�ve put my db.sqlite3 on this repository which also has pricing setup (as given in assignment) and superuser. Use the following Django-admin credentials: 
username: amarpdas		Email: dasamarp@gmail.com		pass: Admin@123#

6. Run the Development Server
$ python manage.py runserver
Visit the admin interface at http://127.0.0.1:8000/admin.


-------------------------------------------------------------------------------------------------------------------------------------

API Documentation:

To Calculate Price

* Endpoint: /api/calc-price/

* Method: POST

* Request Body (JSON):
{
  "distance": 4.5,
  "ride_time": 61,
  "waiting_time": 3,
  "day_str": "Sat"
}

* Response:
{
  "price": 196.25
}

Request Parameters:
* distance: Total distance of the ride in kilometers (float).
* ride_time: Total ride time in minutes (float).
* waiting_time: Total waiting time in minutes (float).
* day_str: Day of the week (3-character string, e.g., "Mon", "Tue", etc.).

Admin Interface

Once you run the project, you can log in to Django Admin at:
* URL: http://127.0.0.1:8000/admin
* Manage PricingConfig, DistanceBasePrice, DistanceAdditionalPrice, TimeMultiplier, and WaitingCharge.
* Track changes in PricingConfigLog.

-------------------------------------------------------------------------------------------------------------------------------------
