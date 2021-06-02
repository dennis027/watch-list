from flask import render_template,request,redirect,url_for
from app import app
from .request import get_movies,get_movie,search_movie
from .models import review
from .forms import ReviewForm
Review = review.Review

# Views
# @app.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''
#     message = "where are you"
#     return render_template('index.html',message=message)

@app.route('/movie/<int:id>')
def movie(id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'

    return render_template('movie.html',title = title,movie = movie)

@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    popular_movies = get_movies('popular')
    upcoming_movie = get_movies('upcoming')
    now_showing_movie = get_movies('now_playing')
    title = 'Home - Welcome to The best Movie Review Website Online'
    search_movie = request.args.get('movie_querry')
    if search_movie:
        return redirect(url_for('search',movie_name=search_movie))
    return render_template('index.html', title = title, popular = popular_movies, upcoming = upcoming_movie, now_showing = now_showing_movie )

# @app.route('/search/<movie_name>')
# def search(movie_name):
#     '''
#     View function to display search results
#     '''
#     movie_name_list = movie_name.split('')
#     movie_name_format = "+".join (movie_name)
#     searched_movie = searched_movie(movie_name_format)
#     title = f'search result for {{movie_name}}'
#     return render_template ('search.html',movies = searched_movie)

@app.route('/search/<movie_name>')
def search_movie(movie_name):
    """
    view function to display search result
    """
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movie = search_movie(movie_name_format)
    title = f'search result for {{movie_name}}'
    return render_template ('search.html',movies = searched_movie)


@app.route('/movie/review/new/<int:id>' ,methods = ['GET','POST'])
def new_review(id):
    form = ReviewForm()
    movie= get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review= form.review.data
        new_review= Review (movie.id,title,movie.poster,review)
        new_review.save_review()
        return redirect(url_for('movie',id=movie.id))
        title = f'{movie.title}review'
        return render_template('new_review.html',title=title,form_review = form,movie=movie)




