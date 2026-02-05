from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt 
   
USERS_FILE = "Users.txt"
DOCTORS_FILE = "Doctors.txt"

st.set_page_config(page_title="Lifeline", page_icon="🏥", layout="centered")
st.title("🏥 LifeLine – Smart Hospital System")

st.sidebar.title("🔐 Secure Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")   
st.markdown("""
<style>
.stApp{
    background:linear-gradient(135deg, midnightblue, black, darkslateblue);
    font-family:"Segoe UI",sans-serif;
    color:white;
}
h1,h2,h3,h4,h5,h6,p,span,label,div{
    color:white !important;
}
input,textarea,select{
    background-color:black!important;
    color:white!important;
    border-radius:10px!important;
    border:1px solid slategray!important;
}
button{
        background-color:royalblue!important;
            border:2px solid white!important;
    }        
</style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <img src="https://cdn-icons-png.flaticon.com/512/4320/4320337.png"
         width="300"
         style="border-radius:20px;">
    """,
    unsafe_allow_html=True
)

class LoginError(Exception):
    pass

adminUsername = "admin"
adminPassword = "admin123"

def readFromFile(fileName):
    data = []
    try:
        with open(fileName, "r") as file:
            for line in file:
                data.append(line.strip().split(","))
    except:
        pass
    return data

def loginUser(username, password):
    if username == adminUsername and password == adminPassword:
        return "Admin"
    users = readFromFile("Users.txt")
    for user in users:
        if user[0] == username and user[1] == password:
            return "Patient"
    else:
        raise LoginError("❌ Wrong username or password. Try again 😐")

if st.sidebar.button("Login"):
    try:
        role = loginUser(username, password)
        st.session_state["logged"] = True
        st.session_state["role"] = role
        st.session_state["user"] = username
        st.success(f"🔥 Access granted! Welcome {role} 👋")
    except LoginError as e:
        st.error(e)

if "logged" not in st.session_state:
    st.warning("⚠️ Login first to enter the system 👆")
    st.stop()

if username == "admin" and password == adminPassword:
    menu = st.sidebar.selectbox(
        "Control Panel",
        [
            "Add Patient",
            "View Patients",
            "Search Patient",
            "Sort Patients by Age",
            "OPD Queue",
            "Bed Allocation",
            "Add Doctor",
            "Statistics",
        ],
    )
elif username.startswith("pat"):
    menu = st.sidebar.selectbox(
        "Patient Menu",
        [
            "View My Details",
            "Book Appointment",
            "View Prescriptions",
        ],
    )
elif username.startswith("doc"):
    menu = st.sidebar.selectbox(
        "Doctor Menu",
        [
            "View Appointments",
            "Add Prescription",
        ],
    )

if not st.session_state.logged:
    st.warning("⚠️ Login required 👆")
    st.stop()

diseaseList = [
    "Fever",
    "Cold",
    "Diabetes",
    "BP",
    "Heart Problem",
    "Asthma",
    "Infection",
    "Fracture"
]

doctorSpecializations = [
    "General Physician",
    "Cardiologist",
    "Dermatologist",
    "Neurologist",
    "Orthopedic",
    "Pediatrician",
    "Gynecologist",
    "ENT",
    "Psychiatrist"
] 

diseaseDoctorMap = {
    "Fever": "General Physician",
    "Cold": "General Physician",
    "Diabetes": "General Physician",
    "BP": "Cardiologist",
    "Heart Problem": "Cardiologist",
    "Asthma": "General Physician",
    "Infection": "General Physician",
    "Fracture": "Orthopedic"
}

def writeToFile(fileName, dataLine):
    with open(fileName, "a") as file:
        file.write(dataLine + "\n")

class ValidationError(Exception):
    pass

def validatePatient(patientId, name, age):
    if patientId == "" or name == "":
        raise ValidationError("❌ Name and ID cannot be empty 😐")
    if age <= 0:
        raise ValidationError("❌ Age must be greater than zero 😄")

def searchPatient(patientId, patients):
    for p in patients:
        if p[0] == patientId:
            return p
    return None 

def sortPatientsByAge(patients):
    n = len(patients)
    for i in range(n):
        for j in range(0, n - i - 1):
            if int(patients[j][2]) > int(patients[j + 1][2]):
                patients[j], patients[j + 1] = patients[j + 1], patients[j]
    return patients

if "opdQueue" not in st.session_state:
    st.session_state.opdQueue = []

def callNextOpd():
    if len(st.session_state.opdQueue) == 0:
        return "😴 OPD queue is empty. No patients waiting."
    else:
        return st.session_state.opdQueue.pop(0)

def getAllPatientIds():
    patients = readFromFile("Users.txt")
    return [p[0] for p in patients]

if "beds" not in st.session_state:
    st.session_state.beds = {
        "B1": "FREE",
        "B2": "FREE",
        "B3": "FREE",
        "B4": "FREE",
        "B5": "FREE"
    }

def allocateBed(patientId):
    beds = st.session_state.beds
    if patientId in beds.values():
        return "⚠️ Patient already has a bed allocated 😐"
    for bedNo, status in beds.items():
        if status == "FREE":
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log = (f"\n--- BED ALLOCATED ---\n"
                   f"Bed No: {bedNo}\n"
                   f"Date & Time: {time_now}\n")
            writeToFile(f"{patientId}.txt", log)
            beds[bedNo] = patientId
            return f"🛏️ Bed {bedNo} successfully allocated to {patientId} ✅"
    return "🚫 All beds are currently full 😴"

def dischargeBed(patientId):
    beds = st.session_state.beds
    for bedNo, status in beds.items():
        if status == patientId:
            beds[bedNo] = "FREE"
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log = (f"\n--- BED DISCHARGED ---\n"
                   f"Bed No: {bedNo}\n"
                   f"Date & Time: {time_now}\n")
            writeToFile(f"{patientId}.txt", log)
            return f"🛏️ {patientId} discharged from {bedNo} successfully"
    return "❌ Patient not found in any bed 😐"

if menu == "Add Patient":
    st.subheader("➕ Add New Patient 🧑‍⚕️")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=1)
    caseType = st.selectbox("Case Type", ["New", "Old"])

    patientId = "pat" + name[:3].lower() + str(age)

    if st.button("Save Patient"):
        try:
            # ✅ Basic validation
            validatePatient(patientId, name, age)

            # 🔍 Proper duplicate patient check
            try:
                with open("Users.txt", "r") as file:
                    for line in file:
                        data = line.strip().split(",")
                        if len(data) > 1 and data[1] == patientId:
                            raise ValidationError(
                                "⚠️ Patient already exists! Try a different name or age."
                            )
            except FileNotFoundError:
                pass

            # 💾 Save patient
            writeToFile(
                "Users.txt",
                f"{name.split()[0]+'@'+str(age)},{patientId},{age},{name}"
            )

            money = {"New": 5000, "Old": 2000}
            patientData = (
                f"Patient ID: {patientId}\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Case Type: {caseType}\n"
                f"Time: {datetime.now()}\n"
                f"------------------------------\n"
            )

            writeToFile(
                f"{patientId}.txt",
                patientData + f"Registration fees: {money[caseType]}\n"
            )

            st.info(f"🆔 Patient ID: {patientId} | Password = Patient ID 🔑")
            st.success("✅ Patient registered successfully 🎉")

        except ValidationError as e:
            st.error(e)

elif menu == "View Patients":
    st.subheader("📋 Registered Patients")
    patients = readFromFile("Users.txt")
    for p in patients:
        st.write(f"🧑 ID: {p[0]} | Name: {p[3]} | Age: {p[2]}   ")

elif menu == "Search Patient":
    pid = st.text_input("Enter Patient ID")
    if st.button("Search"):
        result = searchPatient(pid, readFromFile("Users.txt"))
        if result:
            st.success(result)
        else:
            st.error("❌ Patient not found 😐")

elif menu == "Sort Patients by Age":
    patients = sortPatientsByAge(readFromFile("Users.txt"))
    for p in patients:
        st.write(f"🧑 ID: {p[0]} | Name: {p[3]} | Age: {p[2]}   ")
        st.write("---")

elif menu == "OPD Queue":   
    st.subheader("🧾 OPD Waiting List")
    patientIds = getAllPatientIds()
    if not patientIds:
        st.warning("⚠️ No patients available right now 😐")
    else:
        pid = st.selectbox("Choose Patient ID", patientIds)
        if st.button("Add to OPD"):
            st.session_state.opdQueue.append(pid)
            st.success(f"🧾 {pid} added to OPD queue ✅")
        if st.button("Call Next"):
            st.info(callNextOpd())

elif menu == "Bed Allocation":
    st.subheader("🛏️ Bed Management")
    patientIds = getAllPatientIds()
    if not patientIds:
        st.warning("⚠️ No patients found 😐")
    else:
        pid = st.selectbox("Select Patient ID", patientIds)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Allocate Bed"):
                st.success(allocateBed(pid))
        with col2:
            if st.button("Discharge Patient"):
                st.info(dischargeBed(pid))

    st.subheader("📊 Live Bed Status")
    st.write(st.session_state.beds)

elif menu == "Add Doctor":
    st.subheader("👨‍⚕️ Add Doctor Profile")

    dname = st.text_input("Doctor Name")
    age = st.number_input("Age", min_value=25, max_value=80, step=1)
    spec = st.selectbox("Specialization", doctorSpecializations)

    did = ""
    if dname.strip():
        did = "doc" + dname.strip()[:3].lower() + str(age)

    if st.button("Add Doctor"):
        if not dname.strip():
            st.error("❌ Doctor name cannot be empty")
        elif not dname.replace(" ", "").isalpha():
            st.error("❌ Doctor name should contain only letters")
        else:
            doctors = readFromFile("Doctors.txt")
            existing_ids = [d[0] for d in doctors]
            if did in existing_ids:
                st.warning("⚠️ Doctor already exists in system")
            else:
                writeToFile("Doctors.txt", f"{did},{dname},{spec}")
                st.success("👨‍⚕️ Doctor added successfully! System updated ✅")

elif menu == "Statistics":
    st.subheader("📈 Hospital Insights")

    patients = readFromFile("Users.txt")
    if not patients:
        st.warning("⚠️ No patient data available 😐")
        st.stop()

    ages = [int(p[2]) for p in patients]
    st.info(f"👥 Total Patients Registered: {len(patients)}")
    st.success(f"📊 Average Patient Age: {sum(ages)//len(ages)} years")

    age_groups = {
        "0-10": 0, "11-20": 0, "21-30": 0,
        "31-40": 0, "41-50": 0, "51-60": 0, "61+": 0
    }

    for age in ages:
        if age <= 10: age_groups["0-10"] += 1
        elif age <= 20: age_groups["11-20"] += 1
        elif age <= 30: age_groups["21-30"] += 1
        elif age <= 40: age_groups["31-40"] += 1
        elif age <= 50: age_groups["41-50"] += 1
        elif age <= 60: age_groups["51-60"] += 1
        else: age_groups["61+"] += 1

    st.bar_chart(age_groups)

    diseaseCount = {}
    for p in patients:
        pid = p[0]
        try:
            with open(f"{pid}.txt", "r") as file:
                for line in file:
                    if line.startswith("Diseases:"):
                        diseases = line.replace("Diseases:", "").strip().split(",")
                        for d in diseases:
                            diseaseCount[d.strip()] = diseaseCount.get(d.strip(), 0) + 1
        except:
            pass

    if diseaseCount:
        st.info(f"🦠 Total Disease Types Recorded: {len(diseaseCount)}")
        st.bar_chart(diseaseCount)
    else:
        st.warning("⚠️ No disease data found 😐")
elif menu == "View My Details":
    st.subheader("👤 My Patient Details")
    patientData = ""
    try:
        with open(f"{username}.txt", "r") as file:
            patientData = file.read()
        st.text(patientData)
        st.download_button(
            label="📥 Download My Details",
            data=patientData,
            file_name=f"{username}_details.txt",
            mime="text/plain"
        )
    except FileNotFoundError:
        st.error("❌ No details found for your account 😐"  )

elif menu == "Book Appointment":
    st.subheader("📅 Book Appointment")
    disease = st.selectbox("Select Disease", diseaseList)
    if st.button("Book"):
        doctorSpec = diseaseDoctorMap[disease]
        st.success(f"✅ Appointment booked with {doctorSpec} for {disease} 🎉")
        log = f"\n--- APPOINTMENT BOOKED ---\nDisease: {disease}\nDoctor: {doctorSpec}\nDate & Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        writeToFile(f"{username}.txt", log)
        charges = {"Fever": 1000, "Cold": 800, "Diabetes": 3000, "BP": 2500, "Heart Problem": 5000, "Asthma": 2000, "Infection": 1500, "Fracture": 4000}
        total_amount = charges.get(disease, 0)
        writeToFile(f"{username}.txt", f"Total Amount: {total_amount}")
elif menu == "View Prescriptions":
    st.subheader("💊 My Prescriptions")
    prescriptions = ""
    try:
        with open(f"{username}.txt", "r") as file:
            for line in file:
                if line.startswith("Prescription:"):
                    prescriptions += line.replace("Prescription:", "").strip() + "\n"
        if prescriptions:
            st.text(prescriptions)
            st.download_button(
                label="📥 Download Prescriptions",
                data=prescriptions,
                file_name=f"{username}_prescriptions.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ No prescriptions found for your account 😐")
    except FileNotFoundError:
        st.error("❌ No details found for your account 😐" )
elif menu == "View Appointments":
    st.subheader("📅 My Appointments")
elif menu == "Add Prescription":
    st.subheader("💊 Add Prescription")
    patientId = st.text_input("Enter Patient ID")
    prescriptionText = st.text_area("Prescription Details")
    if st.button("Add Prescription"):
        try:
            with open(f"{patientId}.txt", "a") as file:
                log = f"\n--- PRESCRIPTION ADDED ---\nPrescription: {prescriptionText}\nDate & Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
                file.write(log)
            st.success("✅ Prescription added successfully 🎉")
        except FileNotFoundError:
            st.error("❌ Patient not found 😐")
                            