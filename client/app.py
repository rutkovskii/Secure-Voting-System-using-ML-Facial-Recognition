from flask import *
import requests
import json
from client_encryption import encrypt_data

app = Flask(__name__)
app.secret_key = "super_secret_key"

#Initialize users_data as an empty list
users_data = []  

@app.route("/")
def start():
    session.clear()
    #Set the flag that the user has visited the start page, then render page
    session['visited_start'] = True  
    return render_template("start.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    #Check if the individual user already visited start
    if (not session.get('visited_start', False)):
        return redirect(url_for("start"))
    
    global users_data

    #Create form identifier to determine if user is coming from "Start" or "Details"
    form_identifier = request.form.get("form_identifier")

    #If user is being redirected from details due to errors
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

        #Data structure to hold errors
        errors = []

        #Input validation function
        def check_input_length(value, max_len, field_name):
            if value is None or len(value) == 0:
                errors.append(f"{field_name} requires a value")
            elif len(value) > max_len:
                errors.append(f"{field_name} is too long")

        #Perform input validation
        check_input_length(first_name, 50, "First name")
        check_input_length(last_name, 50, "Last name")
        check_input_length(street, 100, "Street")
        check_input_length(city, 50, "City")
        check_input_length(zipcode, 10, "Zip Code")
        check_input_length(state, 50, "State")
        check_input_length(phone, 20, "Phone Number")
        check_input_length(voter_id, 20, "Voter ID")

        #IF not errors, store data for future use
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
            }

            #Store in global data variable
            users_data = data

            #Set details flag, then redirect for picture
            session['submitted_details'] = True
            return redirect(url_for("capture"))  # Redirect to the capture page
        else:
            #Display errors and redirect to details to try again
            for error in errors:
                flash(error)
            return redirect(url_for("details"))

    return render_template("details.html")

@app.route('/capture')
def capture():
    #Check prerequisites are met
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False)
    ):
        return redirect(url_for("start"))
    
    #Set session flag, then render page
    session['visited_capture'] = True
    
    return render_template("capture.html")

@app.route('/save_image', methods=["POST"])
def save_image():
    #Check prerequisites are met
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False) or
        not session.get('visited_capture', False)
    ):
        return redirect(url_for("start"))

    global users_data

    #Get image data from form and save it
    users_data["image_data"] = request.form.get("image_data")
<<<<<<< HEAD
=======

    users_data["image_data"] = "Image data goes here"
    print("\n")
    print("[+] START UNENCRYPTED DATA \n")
    print(users_data)
    print("[+] END UNENCRYPTED DATA \n")
    print("\n")
    #Send data to exteranal server for validataion
    status = send_to_external_server(users_data)
>>>>>>> 494e26b60d9e54557bbf16cf34a85a9fbb1b6e8f

    #Send data to exteranal server for validataion
    status, token = send_to_external_server(users_data)
    
    if status == 'valid':
        session['server_response_status'] = 'valid'
        session['token'] = token  # store the received token in session
        return redirect(url_for("vote"))
    else:
        flash('Invalid data, please check your details and try again.')
        return redirect(url_for("details"))

#Functions to handle server communication
def send_to_external_server(data):

    encrypted_data = encrypt_data(data)
<<<<<<< HEAD
=======
    print("\n")
    print("[+] START ENCRYPTED DATA \n")
    print(encrypted_data)
    print("[+] END UNENCRYPTED DATA \n")
    print("\n")
    
>>>>>>> 494e26b60d9e54557bbf16cf34a85a9fbb1b6e8f
    #Set parameters for request then send
    url = "http://localhost:8000/api/endpoint"  #Dummy address
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(encrypted_data))

    #IF data is received by server correctly, return response
    if response.status_code != 200:
        print("Failed to send data to the external server.")
        return 'invalid'
    else:
        #Notify user that data is invalid
        print("Data successfully sent to the external server.")
        response_data = response.json()
        return response_data.get('status', 'invalid')

@app.route('/vote')
def vote():
    #If prerequistes aren't met
    if (
        not session.get('visited_start', False) or
        not session.get('submitted_details', False) or
        not session.get('visited_capture', False) or
        not session.get('server_response_status', False) != 'valid'
    ):
        return redirect(url_for("start"))
    
    return render_template('vote.html')

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    president = request.form.get('president')
    project_coolness = request.form.get('project_coolness')
    class_like = request.form.get('class_like')

    # package the vote choices into a dictionary
    vote_data = {
        'president': president,
        'project_coolness': project_coolness,
        'class_like': class_like,
    }

    # encrypt the vote data
    encrypted_vote_data = encrypt_data(vote_data)

    # send the encrypted vote data and token to the server
    url = "http://localhost:8000/api/vote_endpoint"  # dummy address
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'vote_data': encrypted_vote_data, 'token': session['token']})
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        flash("Failed to submit vote.")
        return redirect(url_for('vote'))


if __name__ == "__main__":
    app.run(debug=True)
