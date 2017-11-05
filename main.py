import requests
from flask import Flask, render_template, request, url_for, redirect
import lxml.html
import urllib.request ##get_page
from bs4 import BeautifulSoup
import re
import os
import ranking
import look
    


app = Flask(__name__)
@ app.route('/')
def index():
    return render_template("send.html")

@ app.route('/search', methods=['GET', 'POST'])
def send_request():
    key_show = ""
    if request.method == "POST":
        keyword = request.form['key']
        order = look.order_search(keyword)
        try:
            order[0]
            try:
                order[1]
                try:
                    order[2]
                    return render_template("result.html", key_show=order[0], key_show2=order[1], key_show3=order[2])
                except:
                    return render_template("result.html", key_show=order[0], key_show2=order[1])
            except:
                return render_template("result.html", key_show=order[0])
        except:
            return render_template("result.html", error="So sorry, I can't find")
       


if __name__ == '__main__':
    app.debug = True
    app.run()
