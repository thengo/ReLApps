from flask import Flask, render_template, redirect, request
# import pymongo

app = Flask(__name__, static_url_path = "")
# connection_string = "mongodb://127.0.0.1"
# connection = pymongo.MongoClient(connection_string)
# database = connection.taxi
# rides = database.rides
conn = connectTo 'jdbc:oracle:thin:@128.83.138.158:1521:orcl' 'C##cs347_prof' 'orcl_prof' 'rdf_mode' 'F2014'

#Homepage
@app.route('/')
def splash():
    return app.send_static_file('splash.html')

#Individual information page for each book
@app.route('/detail/<name>/<time>/', methods=['GET', 'POST'])
def detail(name, time):
    if request.method == 'GET':
        cursor = SQL on conn """select name, phone, pickup, destination, time, driver from rides where name = '"""name"""' and time = '"""time"""'"""

        #print "Cursor tuple is: %s" % (cursor,)
        result_dict = {}
        num = 0
        for j in cursor:
            result_dict.update({'name' : j[0], 'phone' : j[1], 'pickup' : j[2], 'destination' : j[3], 'time' : j[4], 'driver' : j[5]})
            num += 1
            #results = {field:value for field, value in cursor.items()}
    return render_template('detail.html', result=result_dict)

#serves image in image file for a particular book
@app.route('/static/images/<image>/')
def image(image):
    return app.send_static_file('images/'+image)

#Claims a ride given name
@app.route('/claim/<name>/<time>/', methods=['GET', 'POST'])
def claim(name, time):
    cursor = SQL on conn """select name, phone, pickup, destination, time, driver from rides where name = '"""name"""' and time = '"""time"""'"""
    already_claimed = True
    if request.method == 'GET' :
        pass
        # SQL on conn """update rides set driver = 'driver_1' where name ='"""name"""' and time = '"""time"""'""" 
        #result_dict = {}
        #num = 0
        #for j in cursor:
        #    result_dict.update({'name' : j[0], 'phone' : j[1], 'pickup' : j[2], 'destination' : j[3], 'time' : j[4], 'driver' : j[5]})
        #    num += 1

    #print(cursor)
    elif request.method == 'POST':
        SQL on conn """update rides set driver = 'driver_1' where name ='"""name"""' and time = '"""time"""'"""    
        cursor = SQL on conn """select name, phone, pickup, destination, time, driver from rides where name = '"""name"""' and time = '"""time"""'"""
        print("cursor:", cursor)

    cursor_2 = SQL on conn """select * from rides where name = '"""name"""' and time = '"""time"""' and driver = 'driver_1'"""
    if len(cursor_2) == 1:
        already_claimed = False

    result_dict = {}
    num = 0
    for j in cursor:
        result_dict.update({'name' : j[0], 'phone' : j[1], 'pickup' : j[2], 'destination' : j[3], 'time' : j[4], 'driver' : j[5]})
        num += 1
    return render_template('claim.html', result = result_dict, already_claimed=already_claimed)

@app.route('/unclaimed_rides/', methods=['GET', 'POST'])
def unclaimed_rides():
    if request.method == 'GET':
        cursor = SQL on conn """select name, phone, pickup, destination, time, driver from rides where driver = 'N/A'"""
        print(cursor)
        result_dict = {}
        num = 0
        for j in cursor:
            if j[0] != 'name':
                result_dict.update({'Key' + str(num): {'name' : j[0], 'phone' : j[1], 'pickup' : j[2], 'destination' : j[3], 'time' : j[4]}})
                num += 1
        return render_template('unclaimed_rides.html', posting=False, result=result_dict)


#The search page
@app.route('/search/', methods=['GET', 'POST'])
def search():
    #Return results for titles, authors and genres that match the search query
    if request.method == 'POST':
        query = request.form['query']
        # title_cursor = books.find({'title':query})
        # author_cursor = books.find({'author':query})
        # genre_cursor = books.find({'genre':query})
        
        cursor = SQL on conn """select name, time from rides where name = '"""query"""' or phone = '"""query"""' or pickup = '"""query"""' or destination = '"""query"""' or time = '"""query"""'"""  
        #phones = SQL on conn """select name, phone, time from rides where phone = '"""query"""'"""
        #pickups = SQL on conn """select name, pickup, time from rides where pickup = '"""query"""'"""
        #destinations = SQL on conn """select name, destination, time from rides where destination = '"""query"""'"""
        #times = SQL on conn """select name, time from rides where time = '"""query"""'"""
        #print(cursor)
        name_dict = {}
        num = 0
        for j in cursor :
            if j[0] != 'name':
                # name_dict['Key' + str(num)].update({j[0]: j[1]})
                # num += 1
                name_dict.update({'Key' + str(num) : {'name' : j[0], 'time': j[1]}})
                num += 1

        #for key in name_dict :
        #    print(key, name_dict[key])

        #phone_dict = {}
        #num = 0
        #for j in phones :
        #    phone_dict.update({'Key' + str(num) : {'name' : j[0], 'time' : j[1]}})
        #     num += 1
        # pickup_dict = {}
        # num = 0
        # for j in pickups :
        #     pickup_dict.update({'Key' + str(num) : {'name' : j[0], 'time' : j[1]}})
        #     num += 1
        # destination_dict = {}
        # num = 0
        # for j in destinations :
        #     destination_dict.update({'Key' + str(num) : {'name' : j[0], 'time' : j[1]}})
        #     num += 1
        # time_dict = {}
        # num = 0
        # for j in times :
        #     time_dict.update({'Key' + str(num) : {'name' : j[0], 'time' : j[1]}})
        #     num += 1

        # title_dict = {}
        # author_dict = {}
        # genre_dict = {}"""

        no_results = name_dict == 0# and phone_dict == 0 and pickup_dict == 0 and destination_dict == 0 and time_dict == 0
        return render_template('search.html', posting=True, query=query, no_results=no_results, name_results=name_dict)#, phone_results=phone_dict, pickup_results=pickup_dict, destination_results=destination_dict, time_results=time_dict""")  

    else:
        return render_template('search.html', posting=False)

#The page to add a book to the database
@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_data = {k : v for k, v in request.form.items()}
        #If the user leaves a field blank
        if new_data['name'] == '' or new_data['phone'] == '' or new_data['pickup'] == '' or new_data['destination'] == '' or new_data['time'] == '':
            return render_template('add.html', alert="required")
        #If the user tries to add a Ride Request that's already in the database
        #elif rides.find({'name':new_data['name'], 'phone':new_data['phone'], 'time':new_data['time']}).count() > 0: 
        #    return render_template('add.html', alert="exists")
        else:
            # books.insert(new_data)
            values = (str(new_data['name']), str(new_data['phone']), str(new_data['pickup']), str(new_data['destination']), str(new_data['time']), str('N/A'))
            SQL on conn """insert into rides(name, phone, pickup, destination, time, driver) values"""values
            return render_template('add.html', alert = "success")
    else:
        return render_template('add.html', alert="")


#The page to add a book to the database
@app.route('/reset/', methods=['GET', 'POST'])
def reset():
    SQL on conn """DROP TABLE rides"""
    return app.send_static_file('splash.html')

if __name__ == '__main__':
    app.debug = True
    app.run()



