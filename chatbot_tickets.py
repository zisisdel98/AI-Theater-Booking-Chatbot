from openai import OpenAI
import speech_recognition as sr
import uuid
from datetime import datetime
from twilio.rest import Client
from openai import OpenAI
import speech_recognition as sr
import uuid
from datetime import datetime
from flask import Flask, request, redirect
from twilio.rest import Client
from flask import Flask, request
from twilio. twiml.messaging_response import MessagingResponse
from twilio.rest import Client


account_sid = '****'
auth_token = '*****'
clients = Client(account_sid, auth_token)



# Your WhatsApp-enabled Twilio phone number
from_whatsapp_number = '+13146674797'

client = OpenAI(api_key="*****************")
first_msg= True
app = Flask(__name__)
@app.route("/", methods=["GET",'POST'])

def whatsapp_reply():
    response = MessagingResponse()
    reply=handler(request.values.get("Body",None))
    response.message(reply)
    return str(response)

reply_AI=None
info_ok = False
reboot=None
cancel_ok=False

"""
# Λειτουργία αναγνώρισης φωνής
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio, language="el-GR")
        print("You said: {}".format(response))
    except sr.RequestError:
        response = "API unavailable"
    except sr.UnknownValueError:
        response = "Unable to recognize speech"

    return response
"""
#read the jsonl file to fine tune my model
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

#prompt and completion from API
def chat_with_gpt(customer_query, initial_info, model="gpt-3.5-turbo", max_tokens=800, temperature=0.7, top_p=1.0):
    try:
        response = client.chat.completions.create(model=model,
        messages=[
            {"role": "system", "content": initial_info},
            {"role": "user", "content": customer_query}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Παρουσιάστηκε σφάλμα: {e}"


performances = {
    "Η μηχανή του Turing": {
        "dates": "10-10-2024 έως 31-03-2025",
        "times": ["18:00", "21:00"],
        "duration": "2 ώρες",
        "cost": {
            "Διακεκριμένη ζώνη": 50,
            "Α΄ ζώνη": 30,
            "Β΄ ζώνη": 20
        },
        "info": "Η θρυλική, πλέον, παράσταση με τον Ορφέα Αυγουστίδη στον ρόλο του Άλαν Τούρινγκ..."
    },
    "Οι βρυκόλακες": {
        "dates": "10-10-2024 έως 31-03-2025",
        "times": ["18:00", "21:00"],
        "duration": "2 ώρες",
         "cost": {
            "Διακεκριμένη ζώνη": 50,
            "Α΄ ζώνη": 30,
            "Β΄ ζώνη": 20
        },
        "info": "Η κυρία Άλβινγκ ετοιμάζεται για τα εγκαίνια του Ιδρύματος..."
    }
}

def is_date_in_range(date_str):
    # Ορισμός της μορφής ημερομηνίας
    date_format = "%d-%m-%Y"
    
    # Ορισμός των ορίων ημερομηνιών
    start_date = datetime.strptime("10-10-2024", date_format)
    end_date = datetime.strptime("31-03-2025", date_format)
    
    # Μετατροπή της εισαγόμενης ημερομηνίας σε αντικείμενο datetime
    date_to_check = datetime.strptime(date_str, date_format)
    
    # Έλεγχος αν η ημερομηνία είναι εντός του εύρους
    return start_date <= date_to_check <= end_date

book_ok= False
book_state="anamoni"
title, date, hour, tickets, zone, surname, name, email, reservation_number = None, None, None, None, None, None, None, None, None
bookings=[]
complete_booking=False
def book_ticket(msg):
    global book_state
    global complete_booking
    global title,date,hour,tickets,zone,surname,name,email,reservation_number
    global bookings
    if book_state=="anamoni" :
        book_state="performance"
        return ("Διαθέσιμες παραστάσεις: Η μηχανή του Turing, Οι βρυκόλακες " + "Επιλέξτε παράσταση: ")
    elif book_state=="performance":
        if msg not in performances:
            return ("H παράσταση δεν βρέθηκε " + "επιλέξτε παράσταση")
        else:
            title=msg
            book_state="date"
            return ("Επιλέξτε ημερομηνία (π.χ. 15-10-2024): ")
    elif book_state=="date":
        if is_date_in_range(msg) == False :
            return ("Η παράσταση είναι διαθέσιμη από 10-10-2024 έως 31-03-2025. Επιλέξτε ημερομηνία: ")
        else:
            date=msg
            book_state="hour"
            return("Επιλέξτε ώρα (18:00 ή 21:00): ")
    elif book_state=="hour":
        if msg not in ["18:00","21:00"]:
            return ("Επιλέξτε ώρα (18:00 ή 21:00): ")
        else:
            hour=msg
            book_state="tickets" 
            return ("Πόσα εισιτήρια θέλετε;")
    elif book_state=="tickets":
        tickets
        book_state="zone"
        return("Επιλέξτε ζώνη (Διακεκριμένη ζώνη, Α΄ ζώνη, Β΄ ζώνη): ")
    elif book_state=="zone":
        if msg not in performances[title]['cost']:
            return ("Μη έγκυρη επιλογή ζώνης. "+ "Επιλέξτε ζώνη (Διακεκριμένη ζώνη, Α΄ ζώνη, Β΄ ζώνη): ")
        else:
            book_state="surname" 
            return ("Επώνυμο: ")
    elif book_state=="surname":
        book_state="name"
        return("Όνομα: ")
    elif book_state=="name":
        book_state="Email"
        return("Εισάγετε το email σας :")
    elif book_state=="Email":
        book_state="final"
        reservation_number = str(uuid.uuid4())
        bookings.append(reservation_number)
        complete_booking=True
        return ("Η κράτησή σας ολοκληρώθηκε. Ο αριθμός κράτησης είναι: "+reservation_number+"\nΕυχαριστώ για τη συνομιλία!")

found_complain=False
complain_ok=False
def complain(msg):
    global found_complain
    global complain_ok
    if (complain_ok==False):
        complain_ok=True
        return("Παρακαλώ πείτε το παράπονό σας.")
    else:
        found_complain=True
        return ("Το παράπανο σας καταγράφηκε" + "\nΕυχαριστώ για τη συνομιλία! ")



found=False
def info(msg):
    global found
    global info_ok
    if (not info_ok):
        info_ok = True
        return ("Διαθέσιμες παραστάσεις: Η μηχανή του Turing, Οι βρυκόλακες " + "Επιλέξτε παράσταση για πληροφορίες: ")
    else:
        if msg not in performances and found == False:
            return ("H παράσταση δεν βρέθηκε " + "επιλέξτε παράσταση για πληροφορίες")
        else:
            found=True
            return (get_performance_info(msg) + "\nΕυχαριστώ για τη συνομιλία! ")

found_cancel=False
def cancel(msg):
        global found_cancel
        global cancel_ok

        if (not cancel_ok):
            cancel_ok=True
            return("Για να ακυρώσετε την κράτησή σας, παρακαλώ εισάγετε τον αριθμό κράτησης.")
        else:
            if msg in bookings and found_cancel==False:
                found_cancel=True
                return ("H κράτηση με αριθμό "+ msg+" ακυρώθηκε"+ "\nΕυχαριστώ για τη συνομιλία! ")
            else:
                return ("Παρακαλώ δώσε έναν σωστό αριθμό κράτησης")


def get_performance_info(title):
    info = performances.get(title, None)
    if info:
        return f"Παράσταση: {title}\nΗμερομηνίες: {info['dates']}\nΏρες: {', '.join(info['times'])}\nΔιάρκεια: {info['duration']}\nΠληροφορίες: {info['info']}"
    else:
        return "Δεν βρέθηκαν πληροφορίες για την επιλεγμένη παράσταση."

def initial_state():
    global found_complain
    global complain_ok
    global first_msg
    global found_cancel
    global reply_AI
    global info_ok
    global bookings
    global complete_booking
    global cancel_ok
    global book_state
    global found
    global reboot
    global title,date,hour,tickets,zone,surname,name,email,reservation_number
    first_msg= True
    reply_AI=None
    found=False
    info_ok = False
    found_complain=False
    complain_ok=False
    reboot=None
    found_cancel=False
    book_state="anamoni"
    complete_booking=False
    cancel_ok=False
    title, date, hour, tickets, zone, surname, name, email, reservation_number = None, None, None, None, None, None, None, None, None


def handler(msg):
    global first_msg
    global cancel_state
    global reply_AI
    global found_complain
    global complain_ok
    global info_ok
    global bookings
    global found_cancel
    global found
    global book_state
    global complete_booking
    global reboot
    global title,date,hour,tickets,zone,surname,name,email,reservation_number
    reply=""
    file_path= "1.jsonl"
    initial_info= read_file(file_path)
    reboot= chat_with_gpt(msg, initial_info)

    if "Change"in reboot:
        initial_state()

    if first_msg:
        reply = "Καλώς ήρθατε στο σύστημα κρατήσεων θεατρικών παραστάσεων.\n"+"\nΣε τι θα μπορούσα να βοηθήσω; "
        first_msg=False
    else:
        if (msg !="έξοδος" and msg!="Έξοδος" and "εξοδος"):
            reboot= chat_with_gpt(msg, initial_info) if reboot is None else reboot
            reply_AI = chat_with_gpt(msg, initial_info) if reply_AI is None else reply_AI
            if "Info" in reply_AI :
                if found==False:
                    return info(msg)
                else:
                    initial_state()
                    return ("Χρειάζεστε κάτι άλλο;")
            elif "Book ticket" in reply_AI:
                if complete_booking==False:
                    return book_ticket(msg) 
                else:
                    initial_state()
                    return ("Χρειάζεστε κάτι άλλο;")
            elif "Cancel" in reply_AI:
                if found_cancel==False:
                    return cancel(msg) 
                else:
                    initial_state()
                    return ("Χρειάζεστε κάτι άλλο;")
            elif "Complain" in reply_AI:
                if found_complain==False:
                    return complain(msg)
                else:
                    initial_state()
                    return ("Χρειάζεστε κάτι άλλο;")
        else:
            initial_state()
            return("Ευχαριστώ για τη συνομίλια!")
            

    return (reply)
    

if __name__ == "__main__":
    app.run(port=8080)
    #main_menu()
