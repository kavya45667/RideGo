from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------------------
# DATABASE CONNECTION FUNCTION
# ----------------------------
def get_db():
    conn = sqlite3.connect("RideGo.db")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# REGISTER USER PAGE
# ----------------------------
@app.route("/register_user")
def register_user():
    return render_template("register_user.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_db()
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    return redirect("/")


# ----------------------------
# REGISTER DRIVER PAGE
# ----------------------------
@app.route("/register_driver")
def register_driver():
    return render_template("register_driver.html")  # correct name


@app.route("/add_driver", methods=["POST"])
def add_driver():
    name = request.form["name"]
    vehicle = request.form["vehicle"]
    license_no = request.form["license_no"]

    conn = get_db()
    conn.execute("""
        INSERT INTO drivers (name, vehicle, license_no)
        VALUES (?, ?, ?)
    """, (name, vehicle, license_no))
    conn.commit()
    conn.close()

    return redirect("/")


# ----------------------------
# BOOK RIDE PAGE
# ----------------------------
@app.route("/book_ride")
def book_ride():
    return render_template("book_ride.html")


@app.route("/add_ride", methods=["POST"])
def add_ride():
    user_id = request.form["user_id"]
    driver_id = request.form["driver_id"]
    pickup = request.form["pickup"]
    drop_location = request.form["drop"]

    conn = get_db()
    conn.execute("""
        INSERT INTO rides (user_id, driver_id, pickup, drop_location)
        VALUES (?, ?, ?, ?)
    """, (user_id, driver_id, pickup, drop_location))
    conn.commit()
    conn.close()

    return redirect("/")


# ----------------------------
# ADMIN QUERIES PAGE
# ----------------------------
@app.route("/admin_queries")
def admin_queries():
    conn = get_db()

    users = conn.execute("SELECT * FROM users").fetchall()
    drivers = conn.execute("SELECT * FROM drivers").fetchall()
    rides = conn.execute("SELECT * FROM rides").fetchall()

    conn.close()

    return render_template("admin_queries.html", users=users, drivers=drivers, rides=rides)
@app.route("/map")
def map():
    return render_template("map.html")


# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)