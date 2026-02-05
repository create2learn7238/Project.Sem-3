from datetime import datetime

# ===============================
# USERS.txt
# Format:
# username@age,patientId,age,name
# ===============================
users = [
    "ram@25,patram25,25,Ram Sharma",
    "sita@30,patsit30,30,Sita Verma",
    "amit@40,patami40,40,Amit Patel",
    "neha@22,patneh22,22,Neha Singh",
    "rohan@35,patroh35,35,Rohan Mehta"
]

with open("Users.txt", "w") as f:
    for u in users:
        f.write(u + "\n")

# ===============================
# Doctors.txt
# Format:
# doctorId,name,specialization
# ===============================
doctors = [
    "docraj45,Raj Mehta,Cardiologist",
    "docsun38,Sunita Rao,General Physician",
    "docvik50,Vikram Singh,Orthopedic",
    "docanu42,Anuradha Iyer,Neurologist",
    "docrav36,Ravi Kumar,Pediatrician"
]

with open("Doctors.txt", "w") as f:
    for d in doctors:
        f.write(d + "\n")

# ===============================
# Individual Patient Files
# ===============================
patients = {
    "patram25": "Ram Sharma",
    "patsit30": "Sita Verma",
    "patami40": "Amit Patel",
    "patneh22": "Neha Singh",
    "patroh35": "Rohan Mehta"
}

for pid, name in patients.items():
    with open(f"{pid}.txt", "w") as f:
        f.write(
            f"Patient ID: {pid}\n"
            f"Name: {name}\n"
            f"Age: {pid[-2:]}\n"
            f"Case Type: New\n"
            f"Time: {datetime.now()}\n"
            f"------------------------------\n"
            f"Registration fees: 5000\n"
            f"\n--- APPOINTMENT BOOKED ---\n"
            f"Disease: Fever\n"
            f"Doctor: General Physician\n"
            f"Date & Time: {datetime.now()}\n"
        )

print("✅ 5 Patients and 5 Doctors sample data created successfully!")
