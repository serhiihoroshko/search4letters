from flask import Flask, render_template, request, session
from database import Database, ConnectionError
from checker import Checker
from vsearch import search4letters

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': '8isPo!@TWDuj9G8J',
                          'database': 'vsearchlogDB', }


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


def log_request(req: 'flask_request', res: str) -> None:
    with Database(app.config['dbconfig']) as cursor:
        _SQL = """INSERT INTO log 
                (phrase, letters, ip, browser_string, results)
                values 
                (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.headers.get('User-Agent'),
                              res, ))


@app.route('/', methods=['GET'])
@app.route('/entry', methods=['GET'])
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('***** Login failed with this error:', str(err))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)


@app.route('/viewlog', methods=['GET'])
@Checker
def view_the_log() -> 'html':
    try:
        with Database(app.config['dbconfig']) as cursor:
            _SQL = """SELECT phrase, letters, ip, browser_string, results 
                    FROM log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
