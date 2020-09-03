from flask import Flask, render_template, request, make_response, jsonify, redirect
from services.google_ads_service import GoogleAdsService
import random

app = Flask(__name__)
google_ads_service = GoogleAdsService()

@app.route('/')
def home():
    homepage_name = random.choice(["home - bootstrap 2020m05.html", "home - original pre-2020m05.html"])
    google_ads_data = google_ads_service.get_google_ads_data_from_url()
    return render_template(homepage_name)

if __name__ == "__main__":
    app.run()

@app.route("/get")
def first_function_after_app_route():