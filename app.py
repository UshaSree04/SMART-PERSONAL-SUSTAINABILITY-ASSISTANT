from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



app = Flask(__name__)
# Load trained model

model_path = "carbon_footprint_model.pkl"
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    model = None
    print("❌ Model file not found! Please train the model first.")


# Serve Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Serve Additional Pages
@app.route("/calculator")
def calculator():
    return render_template("calci.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/cfp")
def cfp():
    return render_template("cfp.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/donation")
def donation():
    return render_template("donation.html")
# Carbon Footprint Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("📥 Received Data:", data)  # Debugging

        # Convert input into DataFrame
        df = pd.DataFrame([data])

        # Rename JSON keys to match training data
        df.rename(columns={
            "electricity": "Electricity Usage (kWh)",
            "water": "Water Usage (Liters)",
            "foodWaste": "Food Waste (kg)"
        }, inplace=True)

        print("📊 DataFrame before checking for NaN:\n", df)  # Debugging

        # Check for missing values
        if df.isnull().values.any():
            print("⚠️ Missing values found in DataFrame!")
            return jsonify({"error": "❌ Missing values detected. Please enter all fields."})

        # Ensure model is loaded
        if model is None:
            return jsonify({"error": "❌ Model is not loaded. Train the model first."})

        # Make prediction
        prediction = model.predict(df)[0]
        return jsonify({"carbon_footprint": round(prediction, 2)})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)})

# Error Handling for 404 Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/recycle")
def recycle():
    """Render the chatbot interface."""
    return render_template("recycle.html")

recycling_tips = {
    "plastic": [
        "Rinse plastic containers before recycling to remove food residue.",
        "Avoid single-use plastics—opt for reusable alternatives instead.",
        "Check the recycling number on plastic items to ensure they are accepted in your area.",
        "Plastic bags cannot be recycled in regular bins—take them to a supermarket drop-off."
    ],
    "glass": [
        "Glass bottles and jars should be rinsed before recycling.",
        "Do not mix different colors of glass—separate clear, green, and brown glass.",
        "Avoid recycling broken glass—it can contaminate the batch and cause safety hazards."
    ],
    "electronics": [
        "Take old electronics to an e-waste recycling center to prevent toxic landfill waste.",
        "Many retailers offer trade-in programs for old devices—check before disposing.",
        "Batteries and chargers should be recycled separately to avoid hazards."
    ],
    "paper": [
        "Remove staples, plastic covers, or laminated surfaces before recycling paper.",
        "Shredded paper should be placed in a paper bag before recycling to prevent mess.",
        "Avoid recycling greasy or wet paper—it can ruin the entire batch."
    ],
    "metal": [
        "Rinse metal cans before recycling and remove any paper labels if possible.",
        "Scrap metal can often be taken to a local scrapyard for proper recycling.",
        "Aluminum foil can be recycled, but only if it’s clean—avoid food contamination."
    ],
    "clothes": [
        "Donate old clothes in good condition instead of throwing them away.",
        "Recycle torn or unwearable clothes at textile recycling centers.",
        "Upcycle old clothes into cleaning rags or creative crafts to reduce waste."
    ],
    "default": [
        "I'm not sure about that. Try asking about plastic, glass, electronics, paper, metal, or clothes recycling."
    ]
}
@app.route("/chat", methods=["POST"])
def chat():
    """Handle user messages and return recycling tips."""
    user_message = request.json.get("message", "").lower().strip()

    # Find relevant response
    for key in recycling_tips.keys():
        if key in user_message:
            response = recycling_tips[key]
            break
    else:
        response = recycling_tips["default"]

    return jsonify({"response": response})
# SMTP Server Configuration
SMTP_SERVER = "smtp.gmail.com"  # You can change this to your SMTP provider
SMTP_PORT = 587
SENDER_EMAIL = "greentrack19@gmail.com"  # Replace with your email
SENDER_PASSWORD = "eqae vztv lbxn xmsg"  # Use an app-specific password for Gmail

def send_confirmation_email(recipient_email, name, amount):
    subject = "Thank You for Your Donation!"
    body = f"Dear {name},\n\nThank you for your generous donation of ₹{amount}.\n\nWe appreciate your support!"

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
@app.route("/submit", methods=["POST"])
def submit_donation():
    name = request.form["name"]
    email = request.form["email"]
    amount = request.form["amount"]

    # Call the function to send the confirmation email
    send_confirmation_email(email, name, amount)

    return redirect(url_for("thank_you"))

@app.route("/thank_you")
def thank_you():
    return "Thank you for your donation! A confirmation email has been sent."
if __name__ == "__main__":
    app.run(
     host='127.0.0.1',
     port=5008,
     debug=True)
