from flask import Flask,render_template,request,redirect,url_for
import sqlite3
import requests
import os
from dotenv import load_dotenv
import time


app = Flask(__name__) #When Flask starts up, it needs to find your templates folder
#creating an instance of flask, __name__ holds the name of the current module
#Flask uses this to know where to look for the templates folder
#when running app.py directly Python sets __name__ to the string "__main__"
#If app.py were imported by another file instead, __name__ would be "app".
load_dotenv()
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")


def init_db():
    with sqlite3.connect("video_game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Game_Tracker"
                       "(ID INTEGER PRIMARY KEY,Name TEXT NOT NULL, "
                       "Genre TEXT NOT NULL, Status TEXT NOT NULL, Rating REAL)")
        conn.commit()

def get_access_token():
    response = requests.post("https://id.twitch.tv/oauth2/token", #function that accepts (url)-where to send request,(params), query string parameter added to url after ? char.
    #(headers) are extra information that is sent to the server like authorization details, client_id,(data) what information are you requesting
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials" # grant type is what type of authentication is being performed in this case client credentials
        # which the application/program  ie:this program authenticates itself, no user involved
        #grant type : authorization_code requires login through browsers, user input required and is granted permission - login,password
        }
    )
    return response.json()["access_token"] # access_token is a key from the json() conversion of request.post()


@app.route('/',methods = ["GET","POST"])#decorator, when someone visits / run the function below, each route maps to a different function
#and direct to a different url/that does something different like /add would add a new game
#By default flask only accepts GET so you need to add POST to that list
#GET — fetching/retrieving data from the server. browser asks flask for something
#POST — browser sends data to flask
def home():
    with sqlite3.connect("video_game.db") as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            name = request.form["game"]# in the html file <input>
            genre = request.form["genre"]
            status = request.form["status"]
            rating = (request.form["rating"])
            rating = float(rating) if rating else None # rating is converted to a float if rating exist else rating is NONE
            # type( defines what kind of input it is usually in the form of a text box) text(accepts text as approved input)
            #name=( is what connects the html file to the python file) game(in this instance is the general label you placed )
            #for example in a gamestop, you give a disk to the clerk and it is understood as a game
            #request.form["game"] retrieves what that disk is, basically the title of that game
            cursor.execute("INSERT INTO Game_Tracker (name, genre, status, rating) VALUES (?, ?, ?, ?)",
                           (name, genre, status, rating))
            conn.commit()
        cursor.execute("SELECT * FROM Game_Tracker")
        game_list = cursor.fetchall()
        return render_template('index.html', game_list=game_list)#loads the html file,
        # game_list=game_list makes game_list visible in the html file

@app.route('/search',methods = ["GET"]) # only request data not submitting data
def search():
    query = request.args.get("query") # instead of moving to a
    #differnt route to get the information you stay on the same route and the information is brought to you
    #unlike post where you are routed to different .html files
    access_token = get_access_token()
    retry = 0
    while retry < 3:
        headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
        try:
            response = requests.post(
                "https://api.igdb.com/v4/games",
                headers=headers,
                data=f'search "{query}"; fields name,genres.name; limit 5;',# syntax is custom query language used by this api
                timeout= 2 # in the api doc this syntax is required to operate the api
                #timeout is an arg of the function request.post() that handles if a request is taking a long time

        )
            if response.status_code in [408, 429, 500, 502, 503, 504]:
                time.sleep(2 ** retry)#function of time that pauses the program for 2^of retry attempts, exponential backoff
                retry += 1
                continue
            if response.status_code == 200:
                results = response.json()
                return render_template('index.html', results=results) #pass the json
                #as a python dictionary to index.html
        except requests.exceptions.Timeout:
            print("Program timed out")
            retry +=1
            continue
    return render_template('index.html', results=[],error='Search failed, please try again.')
    #If all 3 retries fail we still need to return something — Flask always requires a return value.
    #We send back an empty results list and an error message that index.html can display


@app.route('/delete',methods = ["POST"])
def delete():
    with sqlite3.connect("video_game.db") as conn:
        cursor = conn.cursor()
        game_id = request.form["game_id"]
        cursor.execute("DELETE FROM Game_Tracker WHERE ID = ?", (game_id,))
        conn.commit()
        return redirect(url_for('home'))

@app.route('/edit/<id>',methods = ["GET"]) # gets id and routes user to edit.html database
def edit(id):# takes id as parameter
    with sqlite3.connect("video_game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Game_Tracker WHERE id = ?",(id,)) #fetches exactly one row
        game = cursor.fetchone() # stores that row in python variable
        return render_template("edit.html", game=game) #lefside game is what is
        #made visble to edit.html, right side game is game=cursor.fetchone()


@app.route('/update',methods = ["POST"])
def update():
    with sqlite3.connect("video_game.db") as conn:
        cursor = conn.cursor()
        game_id = request.form["game_id"]
        name = request.form["game"]
        genre = request.form["genre"]
        status = request.form["status"]
        rating = (request.form["rating"])
        rating = float(rating) if rating else None
        cursor.execute("UPDATE Game_Tracker SET Name = ?, Genre = ?, Status = ?, rating = ? WHERE ID = ?",
                       (name,genre,status,rating,game_id))
        conn.commit()
        return redirect(url_for('home')) # url_for is referencing the function name

if __name__ == '__main__':# if the python file is run directly execute this block of code else skip
    init_db()
    app.run(debug=True)#run this prog am in debug mode

