from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt 
   
st.set_page_config(page_title="Lifeline", page_icon="🏥", layout="centered")
st.title("🏥 LifeLine – Smart Hospital System")

st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")   

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
    else :
            raise LoginError("Invalid credentials 😐")



if st.sidebar.button("Login"):
    try:
        role = loginUser(username, password)
        st.session_state["logged"] = True
        st.session_state["role"] = role
        st.session_state["user"] = username
        st.success(f"Welcome {role} 😄")
    except LoginError as e:
        st.error(e)

if "logged" not in st.session_state:
    st.warning("Login karo pehla 👆")
    st.stop()

if username == "admin" and password == adminPassword:
    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Add Patient",
            "View Patients",
            "Search Patient",
            "Sort Patients by Age",
            "OPD Queue",
            "Bed Allocation",
            "Doctor Management",
            "Statistics",
        ],
    )
elif username.startswith("pat"):
    menu = st.sidebar.selectbox(
        "Menu",
        [
            "View My Details",
            "Book Appointment",
            "View Prescriptions",
        ],
    )
elif username.startswith("doc"):
    menu = st.sidebar.selectbox(
        "Menu",
        [
            "View Appointments",
            "Add Prescription",
        ],
    )

if not st.session_state.logged:
    st.warning("Login karo pehla 👆")
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


def writeToFile(fileName, dataLine):
    with open(fileName, "a") as file:
        file.write(dataLine + "\n")

class ValidationError(Exception):
    pass

def validatePatient(patientId, name, age, diseases):
    if patientId == "" or name == "":
        raise ValidationError("ID ane Name khali na hova joie 😐")
    if age <= 0:
        raise ValidationError("Age zero thi moto hovo joie 😄")
    if len(diseases) == 0:
        raise ValidationError("At least ek disease select karo 🤒")

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

## if i am using opdQueue=[] here then it will reset on every rerun
if "opdQueue" not in st.session_state:
    st.session_state.opdQueue = []
def callNextOpd():
    if len(st.session_state.opdQueue) == 0:
        return "OPD khali che 😴"
    else : 
     return st.session_state.opdQueue.pop(0)
    
def getAllPatientIds():
    patients = readFromFile("Users.txt")
    return [p[0] for p in patients]

## if i am using beds={} here then it will reset on every rerun
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
        return "Patient already has a bed 😐"
    for bedNo, status in beds.items():
        if status == "FREE":
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log = (f"\n--- BED ALLOCATED ---\n"
                f"Bed No: {bedNo}\n"
                f"Date & Time: {time_now}\n")
            writeToFile(f"{patientId}.txt", log)    
            beds[bedNo] = patientId
            return f"Bed {bedNo} allocated to {patientId} ✅"
    return "No beds available 😴"


def dischargeBed(patientId):
    beds = st.session_state.beds
    for bedNo, status in beds.items():
        if status == patientId:
            beds[bedNo] = "FREE"
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log = ( f"\n--- BED DISCHARGED ---\n"
                f"Bed No: {bedNo}\n"
                f"Date & Time: {time_now}\n" )
            writeToFile(f"{patientId}.txt", log)
            return f"{patientId} discharged from {bedNo} 🛏️"
    return "Patient not found in any bed 😐"

def showBeds(beds):
    for bedNo, status in beds.items():
        print(bedNo, "→", status)


if menu == "Add Patient":
    st.subheader("➕ Add Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    diseases = st.multiselect("Diseases", diseaseList)
    caseType = st.selectbox("Case Type", ["New", "Old"])
    patientId = "pat"+name[:3]+str(age) 

    if st.button("Save Patient"):
        try:
            validatePatient(patientId, name, age, diseases)
            diseaseString = ",".join(diseases)

            writeToFile("Users.txt",f"{patientId},{name+"@"+str(age)},{age}")

            patientData = (f"PatientId: {patientId}\n"
                           f"Name: {name}\n"
                           f"Age: {age}\n"
                           f"Diseases: {diseaseString}\n"
                           f"CaseType: {caseType}\n"
                           f"------------------------------")
            
            writeToFile(f"{patientId}.txt", patientData)
            st.info(f"Generated Patient ID: {patientId} ,  (Password)" )
            st.success("Patient Added successfully 🎉")
        except ValidationError as e:
            st.error(e)  

elif menu == "View Patients":
    st.subheader("📋 All Patients")
    patients = readFromFile("Users.txt")

    for p in patients:
        st.write(f"ID: {p[0]} | Name: {p[1].split("@")[0]} ")

elif menu == "Search Patient":
    pid = st.text_input("Enter Patient ID")
    if st.button("Search"):
        result = searchPatient(pid, readFromFile("Users.txt"))
        if result:
            st.success(result)
        else:
            st.error("Patient not found 😐")

elif menu == "Sort Patients by Age":
    patients = sortPatientsByAge(readFromFile("Users.txt"))
    for p in patients:
        st.write(str(p))
        st.write("---")

elif menu == "OPD Queue":
    st.subheader("🧾 OPD Queue")
    patientIds = getAllPatientIds()
    if not patientIds:
        st.warning("No patients available 😐")
    else:
        opdQueue=[]
        pid = st.selectbox("Select Patient ID", patientIds)
        if st.button("Add to OPD"):
            st.session_state.opdQueue.append(pid)
            st.success(f"{pid} OPD ma add thayu ✅")
        if st.button("Call Next"):
            st.info(callNextOpd())

elif menu == "Bed Allocation":
    st.subheader("🛏️ Bed Allocation")
    patientIds = getAllPatientIds()
    if not patientIds:
        st.warning("No patients available 😐")
    else:
        pid = st.selectbox("Select Patient", patientIds)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Allocate Bed"):
                st.success(allocateBed(pid))

        with col2:
            if st.button("Discharge Patient"):
                st.info(dischargeBed(pid))

    st.subheader("📊 Current Bed Status")
    st.write(st.session_state.beds)

elif menu == "Doctor Management":
    st.subheader("👨‍⚕️ Doctor Management")
    dname = st.text_input("Doctor Name")
    age = st.number_input("Age", min_value=25)  
    spec = st.selectbox("Specialization", doctorSpecializations)
    did = "doc" + dname[:3] + str(age)

    if st.button("Add Doctor"):
        writeToFile("Doctors.txt", f"{did},{dname},{spec}")
        st.success("Doctor added successfully 👨‍⚕️")
elif menu == "Statistics":
    st.subheader("📈 Hospital Statistics")

    patients = readFromFile("Users.txt")

    if not patients:
        st.warning("⚠️ No patient data available 😐")
        st.stop()

    ages = [int(p[2]) for p in patients]

    st.info(f"👥 Total Patients: {len(patients)}")
    st.success(f"📊 Average Age: {sum(ages)//len(ages)} years")

    age_groups = {
        "0-10": 0,
        "11-20": 0,
        "21-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0,
        "61+": 0
    }

    for age in ages:
        if age <= 10:
            age_groups["0-10"] += 1
        elif age <= 20:
            age_groups["11-20"] += 1
        elif age <= 30:
            age_groups["21-30"] += 1
        elif age <= 40:
            age_groups["31-40"] += 1
        elif age <= 50:
            age_groups["41-50"] += 1
        elif age <= 60:
            age_groups["51-60"] += 1
        else:
            age_groups["61+"] += 1

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
                            d = d.strip()
                            diseaseCount[d] = diseaseCount.get(d, 0) + 1
        except:
            pass

    if diseaseCount:
        st.info(f"🦠 Total Disease Types: {len(diseaseCount)}")
        st.bar_chart(diseaseCount)
    else:
        st.warning("No disease data found 😐")