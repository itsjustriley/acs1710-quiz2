from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')
    

@app.route('/character', methods=['GET'])
def character_details():
    character_number = request.args.get('character_number')
    result = requests.get('https://swapi.py4e.com/api/people/' + character_number)
    if result.status_code == 404 or character_number == '':
        return render_template('error.html')
    character = result.json()
    movies = character['films']
    movie_names = []
    for movie in movies:
        movie_names.append(movie_name(movie))
    home = homeworld(character['homeworld'])
    return render_template('character.html', character=character, character_number=character_number, movie_names=movie_names, home=home)


def movie_name(movie):
    movie_result = requests.get(movie)
    movie = movie_result.json()
    return movie['title']

def homeworld(homeworld):
    homeworld_result = requests.get(homeworld)
    homeworld = homeworld_result.json()
    return homeworld['name']

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)