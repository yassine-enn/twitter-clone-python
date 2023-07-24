import json
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_tweet(tweet_id):
   with open("tweet.json", "r") as reader:
        data_json = json.loads(reader.read())
        msg=None
        for d_json in data_json:
              if d_json.get("id_tweet")==tweet_id:
                msg=d_json
                break

        if msg is None:
            abort(404)
   return msg

def get_tweet_rep(tweet_id):
   with open("tweet.json", "r") as reader:
        data_json = json.loads(reader.read())
        tweet_data=[]
        for d_json in data_json:
              if d_json.get("parent_id_tweet")==tweet_id:
                 tweet_data.append(d_json)

   return tweet_data

@app.route('/')
def index():
    with open("tweet.json", "r") as reader:
        tweet_json = json.loads(reader.read())
        data_json = []
        for d_json in tweet_json:
            if d_json.get("parent_id_tweet") == 0:
                data_json.append(d_json)

    return render_template('index.html',data_json=data_json)

@app.route('/<int:tweet_id>')
def twiter(tweet_id):
    tweet = get_tweet(tweet_id)
    return render_template('tweet.html',tweet=tweet)

@app.route('/ajout', methods=('GET', 'POST'))
def ajout():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        hashtag = request.form['hashtag']
        message = request.form['message']

        if not nom_utilisateur:
            flash('Nom utilisateur est obligatoire !')
        else:
            with open("tweet.json", "r") as reader:
                tweet_data = json.loads(reader.read())
            id_twt=int(len(tweet_data)+1)
            date_tweet=datetime.utcnow()
            date_tweet=date_tweet.strftime('%d/%m/%Y')
            tweet = {
                "id_tweet": id_twt,
                "nom_utilisateur": nom_utilisateur,
                "message": message,
                "parent_id_tweet": 0,
                "date_creation":  date_tweet,
                "hashtag": hashtag,
                "nbre_like": 0
            }
            tweet_data.append(tweet)
            objet_json=json.dumps(tweet_data, indent=2)

            with open("tweet.json","w") as json_data:
                json_data.write(objet_json)
            return redirect(url_for('index'))

    return render_template('ajout.html')

@app.route('/<int:tweet_id>/like')
def like(tweet_id):
  with open("tweet.json", "r") as reader:
        data_json = json.loads(reader.read())

        for d_json in data_json:
            if d_json.get("id_tweet") == tweet_id:
                indice=data_json.index(d_json)
                break

        v_like=data_json[indice]['nbre_like']+1
        data_json[indice]['nbre_like']=v_like
        objet_json = json.dumps(data_json, indent=2)

  with open("tweet.json", "w") as json_data:
        json_data.write(objet_json)
  tweet = get_tweet(tweet_id)
  return render_template('tweet.html', tweet=tweet)

@app.route('/<int:tweet_id>/repondre', methods=('GET', 'POST'))
def repondre(tweet_id):
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        hashtag = request.form['hashtag']
        message = request.form['message']
        if not nom_utilisateur:
            flash('Nom utilisateur est obligatoire !')
        else:
            with open("tweet.json", "r") as reader:
                tweet_data = json.loads(reader.read())
            id_twt = int(len(tweet_data) + 1)
            date_tweet = datetime.utcnow()
            date_tweet = date_tweet.strftime('%d/%m/%Y')
            tweet = {
                "id_tweet": id_twt,
                "nom_utilisateur": nom_utilisateur,
                "message": message,
                "parent_id_tweet": tweet_id,
                "date_creation": date_tweet,
                "hashtag": hashtag,
                "nbre_like": 0
            }
            tweet_data.append(tweet)
            objet_json = json.dumps(tweet_data, indent=2)

            with open("tweet.json", "w") as json_data:
                json_data.write(objet_json)
            return redirect(url_for('index'))


    return render_template('repondre.html')


@app.route('/<int:tweet_id>/affiche_rep')
def affiche_rep(tweet_id):
    tweet_rep = get_tweet_rep(tweet_id)
    tweet = get_tweet(tweet_id)
    return render_template('affiche_rep.html',tweet_rep=tweet_rep,tweet=tweet)

