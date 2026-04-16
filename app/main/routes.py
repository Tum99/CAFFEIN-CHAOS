from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template(
        'main/index.html', 
        active_page='home', 
        body_class='page-home')

@main.route('/about')
def about():
    return render_template(
        'main/about.html',
        active_page='about', 
        body_class='page-about')

@main.route('/events')
def events():
    return render_template(
        'main/events.html', 
        active_page='events', 
        body_class='page-events')
