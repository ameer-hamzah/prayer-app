from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from hijri_converter import Gregorian
import os

app = Flask(__name__)
app.secret_key = "madina-marriage-hall-mosque"

# 🔐 CHANGE THIS PIN
ADMIN_PIN = "1188"

# Weekday names
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# 🕋 In-memory prayer times (serverless)
PRAYER_TIMES = {
    "Fajr": "06:20",
    "Zuhr": "13:30",
    "Asr": "16:00",
    "Maghrib": "غروب آفتاب",
    "Isha": "19:00"
}


class Prayer:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def formatted_time(self):
        try:
            return datetime.strptime(self.time, "%H:%M").strftime("%I:%M")
        except:
            return self.time


@app.route("/", methods=["GET", "POST"])
def index():
    global PRAYER_TIMES

    if request.method == "POST":
        pin = request.form.get("pin")

        if pin != ADMIN_PIN:
            flash("غلط پن کوڈ", "error")
            return redirect(url_for("index"))

        for name in PRAYER_TIMES:
            PRAYER_TIMES[name] = request.form.get(name)

        flash("اوقاتِ نماز اپڈیٹ ہو گئیں", "success")
        return redirect(url_for("index"))

    prayers = [Prayer(name, time) for name, time in PRAYER_TIMES.items()]

    today = datetime.now()
    weekday = WEEKDAYS[today.weekday()]
    english_date = f"{weekday}, {today.day:02d} {today.strftime('%B')} {today.year}"

    hijri = Gregorian(today.year, today.month, today.day).to_hijri()
    islamic_date = f"{weekday}, {hijri.day:02d} {hijri.month_name()} {hijri.year} AH"

    return render_template(
        "index.html",
        prayers=prayers,
        english_date=english_date,
        islamic_date=islamic_date
    )


if __name__ == "__main__":
    app.run()