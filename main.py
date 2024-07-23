from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')

@app.route('/SymptoScan')
def SymptScan():
    return render_template('SymptoScan.html')

@app.route('/symrelief')
def symrelief():
    return render_template('symrelief.html')




if __name__ == '__main__':
    app.run(debug=True)
