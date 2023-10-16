from flask import Flask, render_template
from data import certificats
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', certificats=certificats)


@app.route('/certificates')
def certificates():
    return render_template('certificates.html', certificats=certificats)

if __name__ == '__main__':  
    app.run(debug=True)