from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str):
    with open('vsearch.log', 'a') as logfile:
        print(req.form, req.remote_addr, req.user_agent, res, file=logfile, sep='|')


@app.route('/search4', methods=['POST'])
def search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are you results!'
    results = str((search4letters(phrase, letters)))
    log_request(request, results)
    return render_template('result.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog', methods=['POST'])
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=contents, )


if __name__ == '__main__':
    app.run(debug=True)
