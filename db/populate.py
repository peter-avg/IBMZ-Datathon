import psycopg2
from faker import Faker
import random
import bcrypt

# Initialize Faker
fake = Faker()

# Database connection
conn = psycopg2.connect(
    host="ep-tiny-moon-absraxda-pooler.eu-west-2.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="JaMorant180203"
)
cur = conn.cursor()

def populate_doctor(n=5):
    for _ in range(n):
        name = fake.name()
        email = fake.unique.email()
        # hashed_pw = hash_password(fake.password(length=10))
        cur.execute(
            "INSERT INTO doctor (full_name, email) VALUES (%s, %s)",
            (name, email)
        )


def populate_patient(n=20):
    for _ in range(n):
        name = fake.name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        cur.execute(
            "INSERT INTO patient (full_name, dob) VALUES (%s, %s)",
            (name, dob)
        )

def populate_doctor_patient():
    #* get all doctor ids
    cur.execute("SELECT doctor_id FROM doctor;")
    doctor_ids = [row[0] for row in cur.fetchall()]

    #* get all patient IDs
    cur.execute("SELECT patient_id FROM patient;")
    patient_ids = [row[0] for row in cur.fetchall()]

    for doctor_id in doctor_ids:
        patient_id = random.choice(patient_ids)
        cur.execute(
            "INSERT INTO doctor_patient (doctor_id, patient_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (doctor_id, patient_id)
        )


def populate_form(n=30):
    cur.execute("SELECT patient_id FROM patient")
    patient_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT doctor_id FROM doctor")
    doctor_ids = [row[0] for row in cur.fetchall()]

    for _ in range(n):
        patient_id = random.choice(patient_ids)
        doctor_id = random.choice(doctor_ids)
        cur.execute(
            "INSERT INTO form (patient_id, doctor_id) VALUES (%s, %s)",
            (patient_id, doctor_id)
        )


def populate_medications(n=30):
    for _ in range(n):
        name = fake.word()
        strength = fake.random_int(10, 10000)
        frequency = fake.random_int(1, 10)
        duration = fake.random_int(1, 100)

        cur.execute(
            "INSERT INTO medication (name, strength, frequency, duration) VALUES (%s, %s, %s, %s)",
            (name, strength, frequency, duration)
        )

def populate_form_medication():
    cur.execute("SELECT form_id FROM form;")
    form_ids = [row[0] for row in cur.fetchall()]

    #* get all patient IDs
    cur.execute("SELECT medication_id FROM medication;")
    medication_ids = [row[0] for row in cur.fetchall()]

    for form_id in form_ids:
        medication_id = random.choice(medication_ids)
        cur.execute(
            "INSERT INTO form_medication (form_id, medication_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (form_id, medication_id)
    )


def populate_symptom(n=10):
    for _ in range(n):
        name = fake.sentence(nb_words=2)
        duration = fake.random_int(1, 100)
        intensity = fake.random_int(1, 10)
        recurrence = fake.boolean()

        cur.execute(
            "INSERT INTO symptom (name, duration, intensity, recurrence) VALUES (%s, %s, %s, %s)",
            (name, duration, intensity, recurrence)
        )


def populate_form_symptom():
    cur.execute("SELECT form_id FROM form;")
    form_ids = [row[0] for row in cur.fetchall()]

    #* get all patient IDs
    cur.execute("SELECT symptom_id FROM symptom;")
    symptom_ids = [row[0] for row in cur.fetchall()]

    for form_id in form_ids:
        symptom_id = random.choice(symptom_ids)
        cur.execute(
            "INSERT INTO form_symptom (form_id, symptom_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (form_id, symptom_id)
    )


def clear_all_tables():
    """
    Remove all entries from all tables in the correct order,
    respecting foreign key constraints.
    """
    try:
        # Disable foreign key checks temporarily (optional)
        # cur.execute("SET session_replication_role = 'replica';")

        # Truncate tables in dependency order
        cur.execute("TRUNCATE TABLE form_medication CASCADE;")
        cur.execute("TRUNCATE TABLE form_symptom CASCADE;")
        cur.execute("TRUNCATE TABLE form CASCADE;")
        cur.execute("TRUNCATE TABLE doctor_patient CASCADE;")
        cur.execute("TRUNCATE TABLE medication CASCADE;")
        cur.execute("TRUNCATE TABLE symptom CASCADE;")
        cur.execute("TRUNCATE TABLE patient CASCADE;")
        cur.execute("TRUNCATE TABLE doctor CASCADE;")

        # Commit changes
        conn.commit()
        print("✅ All tables cleared successfully!")
        
        # Re-enable foreign key checks if disabled
        # cur.execute("SET session_replication_role = 'origin';")

    except Exception as e:
        conn.rollback()
        print("❌ Error clearing tables:", e)


# --- Run Population ---
populate_doctor(5)
populate_patient(20)
populate_doctor_patient()
populate_form(30)
populate_medications(30)
populate_form_medication
populate_symptom(30)
populate_form_symptom()

# clear_all_tables()


# Commit and close
conn.commit()
cur.close()
conn.close()