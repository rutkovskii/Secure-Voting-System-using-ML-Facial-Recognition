from flask import *
import base64
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

users_data = []  #Initialize users_data as an empty list

@app.route("/")
def start():
    session['visited_start'] = True  #Set the flag that the user has visited the start page
    return render_template("start.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    if (not session.get('visited_start', False)):
        return redirect(url_for("start"))
    

    global users_data

    form_identifier = request.form.get("form_identifier")

    if form_identifier == "details_form":
        #Retrieve input data
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        street = request.form.get("street")
        city = request.form.get("city")
        zipcode = request.form.get("zipcode")
        state = request.form.get("state")
        phone = request.form.get("phone")
        voter_id = request.form.get("voter_id")

        #Input validation
        errors = []

        def check_input_length(value, max_len, field_name):
            if value is None or len(value) == 0:
                errors.append(f"{field_name} requires a value")
            elif len(value) > max_len:
                errors.append(f"{field_name} is too long")


        check_input_length(first_name, 50, "First name")
        check_input_length(last_name, 50, "Last name")
        check_input_length(street, 100, "Street")
        check_input_length(city, 50, "City")
        check_input_length(zipcode, 10, "Zip Code")
        check_input_length(state, 50, "State")
        check_input_length(phone, 20, "Phone Number")
        check_input_length(voter_id, 20, "Voter ID")

        #Check for errors
        if not errors:
            data = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "street": street,
                "city": city,
                "zipcode": zipcode,
                "state": state,
                "phone": phone,
                "voter_id": voter_id,
                "image": None
            }

            users_data = data

            session['submitted_details'] = True

            return redirect(url_for("capture"))  # Redirect to the capture page
        else:
            for error in errors:
                flash(error)
            return redirect(url_for("details"))

    return render_template("details.html")

@app.route('/capture')
def capture():
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False)
    ):
        return redirect(url_for("start"))
    
    session['visited_capture'] = True
    
    return render_template("capture.html")

@app.route('/save_image', methods=["POST"])
def save_image():
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False) or
        not session.get('visited_capture', False)
    ):
        return redirect(url_for("start"))

    global users_data

    image_data = request.form.get("image_data")
    img_data = base64.b64decode(image_data.split(',')[1])

    user_id = users_data['voter_id']
    image_filename = f"photo_{user_id}.png"

    with open(image_filename, 'wb') as f:
        f.write(img_data)

    users_data['image'] = image_filename

    return redirect(url_for("vote"))

@app.route('/vote')
def vote():
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False) or
        not session.get('visited_capture', False)
    ):
        return redirect(url_for("start"))
    
    return render_template('vote.html')

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    president = request.form.get('president')
    project_coolness = request.form.get('project_coolness')
    class_like = request.form.get('class_like')

    # Store the votes in a database or another storage method
    # ...

    # Redirect to a success or confirmation page (create one if necessary)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
