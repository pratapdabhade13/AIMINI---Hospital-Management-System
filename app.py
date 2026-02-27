from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import mysql.connector
import os
import random
import string
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------- DATABASE CONNECTION -------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1305",
    database="aimini"
)
cursor = db.cursor()

# ------------------- PATIENT DATA -------------------
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
patients = []

# ------------------- LOGIN REQUIRED DECORATOR -------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ------------------- HOME -------------------
@app.route('/')
@login_required
def home():
    return render_template('home.html')

# ------------------- LOGIN -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Get user from DB by email
        cursor.execute("SELECT id, fullname, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            db_password = user[2].strip()  # remove spaces
            if db_password == password:
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                flash(f"Welcome {user[1]}!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid email or password", "danger")
                return redirect(url_for('login'))
        else:
            # Unknown user → show pop-up and redirect to register page
            flash("Email not registered! Please register first.", "warning")
            return redirect(url_for('register'))

    if 'user_id' in session:
        return redirect(url_for('home'))

    return render_template('login.html')


# ------------------- REGISTER -------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        # Already logged in → home page
        return redirect(url_for('home'))

    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Email already registered! Please login.", "warning")
            return redirect(url_for('login'))

        # Insert new user
        cursor.execute("INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)",
                       (fullname, email, password))
        db.commit()

        # Registration successful → show pop-up and redirect to login page
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ------------------- LOGOUT -------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# ------------------- TRUSTS -------------------
@app.route('/trusts')
@login_required
def trusts():
    trusts = [
        {
            "name": "Apollo Hospitals Foundation",
            "image": "https://pbs.twimg.com/profile_images/1463409510505086976/KBuXQmED_400x400.jpg",
            "details": "Supports patient care and hospital infrastructure."
        },
        {
            "name": "Fortis Cares",
            "image": "https://logos-world.net/wp-content/uploads/2022/07/Fortis-Emblem.png",
            "details": "Funds medical research and education programs."
        },
        {
            "name": "Max Foundation",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Max_India_Foundation_logo.svg/2560px-Max_India_Foundation_logo.svg.png",
            "details": "Provides equipment and technology for hospitals."
        },
        {
            "name": "Care Hospitals Trust",
            "image": "https://cdn.brandfetch.io/id0SbvZ3dk/w/400/h/400/theme/dark/icon.jpeg?c=1bxid64Mup7aczewSAYMX&t=1754045199981",
            "details": "Supports rural healthcare initiatives."
        },
        {
            "name": "Manipal Foundation",
            "image": "https://www.manipalhospitals.com/assets/images/about/About_US.jpg",
            "details": "Medical scholarships and research funding."
        },
        {
            "name": "Wockhardt Foundation",
            "image": "https://static.wixstatic.com/media/56e136_871d4bb2acc54cba90afd48469dad83c~mv2.jpg/v1/fit/w_2500%2Ch_1330%2Cal_c/56e136_871d4bb2acc54cba90afd48469dad83c~mv2.jpg",
            "details": "Health camps and community outreach programs."
        },
        {
            "name": "Medanta Heart Foundation",
            "image": "https://medanta.s3.ap-south-1.amazonaws.com/posts/May2025/V5SvPuKwH68LdQaNn6yVWr4arEQ0tl-metaTWVkYW50YS1Mb2dvLUNUQy1wbmcucG5n-.png",
            "details": "Supports cardiac care and emergency services."
        },
        {
            "name": "Sir HN Reliance Foundation",
            "image": "https://cdn.brandfetch.io/idv7k5hZjQ/w/400/h/400/theme/dark/icon.jpeg?c=1bxid64Mup7aczewSAYMX&t=1753479375428",
            "details": "Funds research, training, and patient support programs."
        },
        {
            "name": "Shalby Foundation",
            "image": "https://www.shelbystore.com/v/vspfiles/photos/Z26-CSF-DECAL-2.jpg?v-cache=1657622770",
            "details": "Provides orthopedic and rehabilitation support."
        },
        {
            "name": "HCG Foundation",
            "image": "https://tukuz.com/wp-content/uploads/2020/04/healthcare-global-enterprises-ltd-hcg-logo-vector.png",
            "details": "Cancer care, patient aid, and community awareness."
        }
    ]
    return render_template('trust.html', trusts=trusts)

# ------------------- DOCTORS -------------------
@app.route('/doctors')
@login_required
def doctors():
    doctors = [
        # Dr. J Nair (Unchanged)
        {"name": "Dr. J Nair", "degree": "MS", "specialization": "Neurosurgeon",
         "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=500&q=80"}, 

        # Updated Doctors
        {"name": "Dr. B Patel", "degree": "DM", "specialization": "Neurologist",
         "image": "https://images.openai.com/thumbnails/url/Gk8PWXicu5mVUVJSUGylr5-al1xUWVCSmqJbkpRnoJdeXJJYkpmsl5yfq5-Zm5ieWmxfaAuUsXL0S7F0Tw70dzUtDkxydinwSnUp9opwDkzM8XEpcQ_Iicp38jHxD07J9Uv0sswMdw8K1nXKNPNNUysGAHTwJcs"},  # 2nd image

        {"name": "Dr. I Desai", "degree": "MD", "specialization": "ENT Specialist",
         "image": "https://images.openai.com/thumbnails/url/RCL9lnicu5mZUVJSUGylr5-al1xUWVCSmqJbkpRnoJdeXJJYkpmsl5yfq5-Zm5ieWmxfaAuUsXL0S7F0Tw5JSSqrqKyINMvzM7UoLHdxNPcwSUry9AoMyvJ0Dysvjww2sfA1dU0uc3bVjTI3zSxWKwYAXqklng"},  # 3rd image

        # Unchanged Doctors
        {"name": "Dr. G Kapoor", "degree": "MD", "specialization": "Gynecologist",
         "image": "https://images.unsplash.com/photo-1607746882042-944635dfe10e?auto=format&fit=crop&w=500&q=80"}, 
        {"name": "Dr. D Rao", "degree": "DM", "specialization": "Dermatologist",
         "image": "https://images.unsplash.com/photo-1595152772835-219674b2a8a6?auto=format&fit=crop&w=500&q=80"}, 
        {"name": "Dr. A Sharma", "degree": "MD", "specialization": "Cardiologist",
         "image": "https://images.unsplash.com/photo-1581090700227-1e37b190418e?auto=format&fit=crop&w=500&q=80"},
        {"name": "Dr. E Joshi", "degree": "MD", "specialization": "Pediatrician",
         "image": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=500&q=80"},
        {"name": "Dr. F Mehta", "degree": "MS", "specialization": "General Surgeon",
         "image": "https://images.unsplash.com/photo-1550831107-1553da8c8464?auto=format&fit=crop&w=500&q=80"},
        {"name": "Dr. H Reddy", "degree": "DM", "specialization": "Cardiologist",
         "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=500&q=80"},
        {"name": "Dr. C Singh", "degree": "MS", "specialization": "Orthopedic Surgeon",
         "image": "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=500&q=80"}
    ]
    return render_template('doctors.html', doctors=doctors)

# ------------------- HOSPITAL STAFF -------------------
@app.route('/hospital_staff')
@login_required
def hospital_staff():
    names = [
        "Ramesh Pawar", "Sneha Patil", "Amit Jadhav", "Kiran Shinde", "Pooja Deshmukh",
        "Suresh Kadam", "Meena Kale", "Vikas Rane", "Anjali Gokhale", "Rahul Patankar",
        "Nilesh Thorat", "Priya Bhagat", "Santosh Dumbre", "Komal Bhosale", "Ashok More",
        "Sheetal Pawar", "Mahesh Kale", "Rekha Kharat", "Vivek Chavan", "Sunita Mane",
        "Ganesh Bhise", "Rutuja Jagtap", "Arjun Shelar", "Snehal Ingle", "Vivek Suryavanshi",
        "Madhuri Lohar", "Rohit Ghadge", "Asha Khedekar", "Vijay Dhotre", "Neha Pawar",
        "Manoj Jadhav", "Smita Naik", "Sanjay Gaikwad", "Priti Dhumal", "Sachin Nikam",
        "Anita Phad", "Nitin Bhosale", "Jyoti Kharat", "Avinash Shinde", "Reena Patil",
        "Vishal Kadam", "Kavita Gole", "Anand Bhise", "Tejaswini More", "Dilip Kharade",
        "Sneha Rane", "Rajesh Kale", "Pallavi Jadhav", "Omkar Shinde", "Aarti Patankar"
    ]
    roles = ["Clerk", "Nurse", "Technician", "Ambulance Driver", "Sanitation Worker", "Ward Boy"]
    staff = [{"name": names[i], "role": roles[i % len(roles)]} for i in range(50)]
    return render_template('hospital_staff.html', staff=staff)

# ------------------- APPOINTMENT SYSTEM -------------------
@app.route('/appointment')
@login_required
def appointment():
    doctors = [
        {"name": "Dr. A Sharma", "profession": "Cardiologist", "disease": "Heart Disease"},
        {"name": "Dr. B Patel", "profession": "Neurologist", "disease": "Migraine"},
        {"name": "Dr. C Singh", "profession": "Orthopedic Surgeon", "disease": "Fractures"},
        {"name": "Dr. D Rao", "profession": "Dermatologist", "disease": "Skin Infection"},
        {"name": "Dr. E Joshi", "profession": "Pediatrician", "disease": "Child Illness"},
        {"name": "Dr. F Mehta", "profession": "General Surgeon", "disease": "Surgery Needs"},
        {"name": "Dr. G Kapoor", "profession": "Gynecologist", "disease": "Women's Health"},
        {"name": "Dr. H Reddy", "profession": "Cardiologist", "disease": "Heart Disease"},
        {"name": "Dr. I Desai", "profession": "ENT Specialist", "disease": "Ear/Nose/Throat Issues"},
        {"name": "Dr. J Nair", "profession": "Neurosurgeon", "disease": "Brain/Spine Issues"}
    ]
    return render_template('appointment.html', doctors=doctors)

@app.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment():
    patient_name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    doctor_name = request.form['doctor']
    doctor_profession = request.form['doctor_profession']
    disease = request.form['disease']
    date = request.form['date']
    time = request.form['time']

    cursor.execute("""
        INSERT INTO appointments (patient_name, age, contact, doctor_name, doctor_profession, disease, date, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (patient_name, age, contact, doctor_name, doctor_profession, disease, date, time))
    db.commit()
    return jsonify({"status": "success"})

@app.route('/get_appointments')
@login_required
def get_appointments():
    cursor.execute("SELECT * FROM appointments ORDER BY id ASC")
    data = cursor.fetchall()
    appointments = []

    for row in data:
        appointments.append({
            "id": row[0],
            "patient_name": row[1],
            "age": str(row[2]) if row[2] else "",
            "contact": row[3],                 # ✅ correct
            "doctor_name": row[4],             # ✅ correct
            "doctor_profession": row[5],       # ✅ correct
            "disease": row[6],                 # ✅ correct
            "date": str(row[7]),               # ✅ correct
            "time": str(row[8])                # ✅ correct
        })

    return jsonify(appointments)

@app.route('/view_appointments')
@login_required
def view_appointments_page():
    return render_template('view_appointments.html')

# ------------------- ADD PATIENT -------------------
@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    name = request.form.get('patientName')
    age = request.form.get('age')
    gender = request.form.get('gender')
    contact = request.form.get('contact')
    address = request.form.get('address')
    disease = request.form.get('disease')
    photo = request.files.get('photo')

    photo_filename = None
    if photo and photo.filename != '':
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        filename = f"{random_str}_{photo.filename}"
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)
        photo_filename = os.path.join('uploads', filename)

    patients.append({
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'address': address,
        'disease': disease,
        'photo': photo_filename
    })

    return jsonify({"status": "success"})

@app.route('/get_patients')
@login_required
def get_patients():
    return jsonify(patients)

@app.route('/patient_form')
@login_required
def patient_form_page():
    return render_template('patient_form.html')

@app.route('/view_patients')
@login_required
def view_patients_page():
    return render_template('view_patients.html')

@app.route('/facilities')
@login_required
def facilities():
    return render_template('facilities.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ------------------- RUN APP -------------------
if __name__ == '__main__':
    app.run(debug=True)
