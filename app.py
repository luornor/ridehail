from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_data = {}
user_states = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_id = request.values.get("From")
    incoming_msg = request.values.get("Body", "").strip()

    response = MessagingResponse()

    # URL for the greeting image
    greeting_image_url = "https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80"  # Replace with your image URL

    # Initialize user's state if they are new
    if user_id not in user_states:
        user_states[user_id] = "send_greeting"
    
    # State-based response handling
    if user_states[user_id] == "send_greeting":
        # Send the greeting image and welcome message
        msg = response.message("Hello! Welcome to our service. Let's get started with a few questions. What is your name?")
        msg.media(greeting_image_url)  # Fixed line
        user_states[user_id] = "ask_name"

    elif user_states[user_id] == "ask_name":
        # Save the user's name and move to next question
        user_data[user_id] = {"name": incoming_msg}
        user_states[user_id] = "ask_date_of_birth"
        response.message(f"Nice to meet you, {incoming_msg.capitalize()}! What is your date of birth (e.g., YYYY-MM-DD)?")

    elif user_states[user_id] == "ask_date_of_birth":
        # Save the user's date of birth and move to next question
        user_data[user_id]["date_of_birth"] = incoming_msg
        user_states[user_id] = "ask_email"
        response.message("Got it! What is your email address?")

    elif user_states[user_id] == "ask_email":
        # Save the user's email and move to the next question
        user_data[user_id]["email"] = incoming_msg
        user_states[user_id] = "ask_phone_number"
        response.message("Thank you! What is your phone number?")

    elif user_states[user_id] == "ask_phone_number":
        # Save the user's phone number and move to the next question
        user_data[user_id]["phone_number"] = incoming_msg
        user_states[user_id] = "ask_occupation"
        response.message("Got it! Lastly, what is your occupation?")

    elif user_states[user_id] == "ask_occupation":
        # Save the user's occupation and confirm the details
        user_data[user_id]["occupation"] = incoming_msg
        response.message(
            f"Thanks! Here’s the info you provided:\n"
            f"Name: {user_data[user_id]['name']}\n"
            f"Date of Birth: {user_data[user_id]['date_of_birth']}\n"
            f"Email: {user_data[user_id]['email']}\n"
            f"Phone Number: {user_data[user_id]['phone_number']}\n"
            f"Occupation: {user_data[user_id]['occupation']}\n"
            "If everything looks good, you’re all set!"
        )
        # Optionally, reset the user's state
        user_states[user_id] = "completed"

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)