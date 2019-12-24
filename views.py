from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import cgi
import pyrebase
from django.shortcuts import render
from django.contrib import auth


config = {

    'apiKey': "AIzaSyAZA4gUvaOJf817zs3pHPE38ZcJp8lTn3A",
    'authDomain': "iimt-hostel-dc91e.firebaseapp.com",
    'databaseURL': "https://iimt-hostel-dc91e.firebaseio.com",
    'projectId': "iimt-hostel-dc91e",
    'storageBucket': "iimt-hostel-dc91e.appspot.com",
    'messagingSenderId': "344340173967"

}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

def admno(request):
    return render(request, 'login/admno.html')


def display(request):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='iimt_hostel',
    )

    try:
        #return HttpResponse("here")
        with connection.cursor() as cursor:
            formdata = cgi.FieldStorage()
            sql = "SELECT `Admission_no`, `Student_name`,`Course`,`Branch`,`Block`,`Room_Number`,`Contact_Number`,`Parent_Contact`,`Year`,`Std_photo` FROM student WHERE `Admission_no` = %s"
            #return HttpResponse("here")
            # return HttpResponse(pyid)
            try:
                #return HttpResponse("here")
                global pyid
                pyid = request.POST['admno']
                #return HttpResponse(pyid)
                cursor.execute(sql, (pyid))
                result = cursor.fetchall()

                # print("Id\t\t Title\t\t\t\t\tDescription")
                # print("---------------------------------------------------------------------------")
                for row in result:
                    admn = str(row[0])
                    name = str(row[1])
                    course = str(row[2])
                    branch = str(row[3])
                    block = str(row[4])
                    room_no = str(row[5])
                    contact = str(row[6])
                    p_no = str(row[7])
                    year = str(row[8])
                    image = str(row[9])

                    # message = pyid
                    return render(request, 'login/display.html', {"admn": admn,  "name": name, "course": course, "branch": branch, "block": block, "room_no": room_no, "contact": contact, "p_no": p_no, "year": year,"image":image})
                msg = "not found in the database"
                return render(request, 'login/admno.html',{"msg":msg})
            except:
                message = "Oops! Something wrong"
                return HttpResponse(message)

        connection.commit()
    finally:
        connection.close()
    #return render(request, 'login/display.html', {"here": pyid})


def login_form(request):
    return render(request, 'login/index.html')

def login(request):
    email = request.POST['User_id']
    pasw = request.POST['Password']
    try:
        user = authe.sign_in_with_email_and_password(email, pasw)
    except:
        message = "invalid credentials, enter again"
        return render(request, 'login/index.html', {"msg":message})
    print("\n\n\n\nHERE YOU SEE\n\n\n\n", user['idToken'], "\n\n\n")
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "login/login.html", {"e": email})

def refuse(request):
    message = "Candidate not allowed"
    return render(request, 'login/login.html', {"msg":message})

def send_data(request):
    return render(request, 'login/data.html')


def allow(request):    #on the basis of post_send_data function
#new
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='iimt_hostel',
    )

    try:
        # return HttpResponse("here")
        with connection.cursor() as cursor:
            formdata = cgi.FieldStorage()
            sql = "SELECT `Admission_no`, `Student_name`,`Course`,`Branch`,`Block`,`Room_Number`,`Contact_Number`,`Parent_Contact`,`Year`,`Std_photo` FROM student WHERE `Admission_no` = %s"
            # return HttpResponse("here")
            # return HttpResponse(pyid)
            try:
                # return HttpResponse("here")
                #pyid = request.POST['admno']
                # return HttpResponse(pyid)
                cursor.execute(sql, (pyid))
                result = cursor.fetchall()

                # print("Id\t\t Title\t\t\t\t\tDescription")
                # print("---------------------------------------------------------------------------")
                for row in result:
                    admn = str(row[0])
                    name = str(row[1])
                    course = str(row[2])
                    branch = str(row[3])
                    block = str(row[4])
                    room_no = str(row[5])
                    contact = str(row[6])
                    p_no = str(row[7])
                    year = str(row[8])
                    Std_photo = str(row[9])

            except:
                return HttpResponse("something wrong")
    finally:
        connection.close()

    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili" + str(millis))
    #Std_name = request.POST.get('Std_name')
   # admno = request.POST.get('admno')
    time_out = request.POST.get('time-out')
    date_in = request.POST.get('date-in')
    time_in = request.POST.get('time-in')
    print("\nhere\n", time_out, "\n\n", time_in, "\nhere\n")
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info" + str(a))
    data = {
        "Student name": name,
        'Admission Number': admn,
        "Time Out": time_out,
        "Date In": date_in,
        "Time In": time_in,
        "Std_photo": Std_photo
    }
    database.child('users').child(a).child('student').child(millis).set(data)
    message = "Candidate allowed"
    return render(request, 'login/login.html', {"mssg": message})



def post_send_data(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili" + str(millis))
    Std_name = request.POST.get('Std_name')
    admno = request.POST.get('admno')
    time_out = request.POST.get('time-out')
    time_in = request.POST.get('time-in')
    print("\nhere\n",time_out,"\n\n",time_in,"\nhere\n")
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info" + str(a))
    data = {
        "Student name": Std_name,
        'Admission Number': admno,
        "Time Out": time_out,
        "Time In": time_in
    }
    database.child('users').child(a).child('student').child(millis).set(data)
    name = database.child('users').child(a).child('student').child('Student Name').get().val()
    return render(request, 'login/login.html', {'e': name})
    #return HttpResponse("not working")



def fetch_data(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('users').child(a).child('student').shallow().get().val()
    lis_time = []
    for i in timestamps:
        lis_time.append(i)

    lis_time.sort(reverse=True)
    print("\n\nfirst\n\n",lis_time)
    name = []

    for i in lis_time:
        wor = database.child('users').child(a).child('student').child(i).child('Student name').get().val()
        name.append(wor)
    print("\n\nsecond\n\n",name)

    admno = []
    for i in lis_time:
        adm = database.child('users').child(a).child('student').child(i).child('Admission Number').get().val()
        admno.append(adm)
    print("\n\nthird\n\n",admno)

    date = []
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)


    time_out = []
    for i in lis_time:
        to = database.child('users').child(a).child('student').child(i).child('Time Out').get().val()
        time_out.append(to)

    time_in = []
    for i in lis_time:
        ti = database.child('users').child(a).child('student').child(i).child('Time In').get().val()
        time_in.append(ti)

    date_in = []
    for i in lis_time:
        di = database.child('users').child(a).child('student').child(i).child('Date In').get().val()
        date_in.append(di)

    Std_photo = []
    for i in lis_time:
        sp = database.child('users').child(a).child('student').child(i).child('Std_photo').get().val()
        Std_photo.append(sp)


    print("\n\nfourth\n\n",date)

    comb_lis = zip(lis_time, date, name, admno, time_out, time_in, date_in, Std_photo)
    #name1 = database.child('users').child(a).child('student').child('Student name').get().val()

    return render(request, 'login/getdata.html', {'comb_lis': comb_lis})

    #return render(request, 'login/login.html', {'time': lis_time, 'dat': date, 'name':name, 'admno':admno})
    #return render(request, 'login/getdata.html')

def logout(request):
    auth.logout(request)
    return render(request,'login/index.html')
