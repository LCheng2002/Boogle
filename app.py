from flask import Flask, redirect, render_template, request, url_for
from SearchFiles import Page_search

import sqlite3

app = Flask(__name__)

@app.route("/")
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/results', methods=['GET'])
def results():
    search_content = request.args.get('search_content')
    Matching_num, Searching_result = Page_search(search_content)
    print(Searching_result)
    return render_template("results.html", search_content = search_content, Matching_num = Matching_num, Searching_result = Searching_result)

@app.route('/history')
def history():
    connect = sqlite3.connect('./history.db')
    cursor = connect.cursor()

    sql = "select Time, content from history"
    cursor.execute(sql)
    records = cursor.fetchall()
    return render_template("history.html",records = records)


if __name__ == '__main__':
    app.run(debug=True, port=4572)
