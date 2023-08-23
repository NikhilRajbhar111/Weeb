from flask import Blueprint, render_template, flash, redirect, url_for, request
from my_site.access import load_home_data, load_trending_data
from scraper.detail import get_detail_data
from scraper.stream import get_stream_url
from scraper.search import get_search_data
from scraper.genre import get_genre_data

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home():
    data = load_home_data(20)
    carousel_data = load_trending_data(15)
    return render_template('home.html', data=data, carousel_data=carousel_data)

@routes.route('/category/<card_link>')
def category(card_link):
    title = request.args.get('title')
    anime_data = get_detail_data(card_link, title)
    
    if anime_data:
        genre = anime_data[0]["Genre"]
        genre_data = get_genre_data(genre)
        return render_template('detail.html', data=anime_data, genre=genre_data)
    else:
        flash("An error occurred while fetching data from the category page.")
        return redirect(url_for('routes.home'))

    
@routes.route('/stream/<title>')
def stream(title):
    stream_url = get_stream_url(title)
    total_ep = request.args.get('total_ep')
    
    if stream_url:
        return render_template('stream.html', stream_url=stream_url, total_ep=total_ep, title=title)
    else:
        flash("An error occurred while fetching the stream URL.")
        return redirect(url_for('routes.home'))
    
@routes.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        anime_name = request.form.get("myform")
        anime_data = get_search_data(anime_name)
        return render_template("search.html", data=anime_data)
    return redirect(url_for("routes.home"))


@routes.route("/trending")
def trending():
    data=load_trending_data(20)
    return render_template("trending.html",data=data)
