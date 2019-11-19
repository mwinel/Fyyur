#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from sqlalchemy import inspect
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import Venue, Artist, Show, app, db


# Helper functions
def format_venue_shows(shows):
    new_list = []
    for show in shows:
        artist = show.artist
        new_list.append({
            'id': artist.id,
            'name': artist.name,
            'image_link': artist.image_link,
            'start_time': artist.start_time
        })
    return new_list

def format_artist_shows(shows):
    new_list = []
    for show in shows:
        venue = show.venue
        new_list.append({
            "id": venue.id,
            "name": venue.name,
            "image_link": venue.image_link,
            "start_time": venue.start_time
        })
    return new_list


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    res_result = []
    query = Venue.query.all()
    for row in query:
        city = row.city
        state = row.state
        query = db.session.query(Venue).filter(
            Venue.state == state, Venue.city == city).all()
        venues = [i for i in query]
        for i in query:
            result = {
                'city': i.city,
                'state': i.state,
                'venues': venues
            }
        res_result.append(result)
    data = [i for n, i in enumerate(
        res_result) if i not in res_result[n + 1:]]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    venues = db.session.query(Venue).filter(Venue.name.contains(search_term)).all()
    data = []
    for venue in venues:
        print(venue.name)
        # Filter upcoming shows
        upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(
            Show.start_time > datetime.utcnow().isoformat()).all()
        res_result = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": upcoming_shows,
        }
        data.append(res_result)
    response = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, 
                            search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    data = []
    if venue:
        data = venue.__dict__

    # Filter past shows
    past_shows = Show.query.filter_by(venue_id=venue.id).filter(
        Show.start_time < datetime.utcnow().isoformat()).all()

    # Filter upcoming shows
    upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(
        Show.start_time > datetime.utcnow().isoformat()).all()

    # Format upcoming and past shows
    past_shows = format_venue_shows(past_shows)
    upcoming_shows = format_venue_shows(upcoming_shows)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        new_venue = Venue(name=form.name.data,
                          city=form.city.data,
                          state=form.state.data,
                          address=form.address.data,
                          phone=form.phone.data,
                          seeking_description=form.seeking_description.data,
                          image_link=form.image_link.data,
                          facebook_link=form.facebook_link.data,
                          website=form.website.data,
                          genres=form.genres.data
                          )
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed.')
    except:
        flash('Something went wrong. Venue ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')
    

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueEditForm()
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.seeking_description.data = venue.seeking_description
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.website.data = venue.website
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueEditForm()
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    if venue:
        try:
            venue.name=form.name.data,
            venue.city=form.city.data,
            venue.state=form.state.data,
            venue.address=form.address.data,
            venue.phone=form.phone.data,
            venue.seeking_description=form.seeking_description.data,
            venue.image_link=form.image_link.data,
            venue.facebook_link=form.facebook_link.data,
            venue.website=form.website.data,
            venue.genres=form.genres.data
            # add to database
            db.session.add(venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully updated.')
        except:
            flash('Something went wrong. Venue ' +
                request.form['name'] + ' could not be updated.')
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = db.session.query(Venue).filter_by(id=venue_id).first()
        name = venue.name
        db.session.delete(venue)
        db.session.commit()
        flash('Venue, ' + name + ' successfully deleted.')
    except:
        flash('Something went wrong. ' + name + ' could not be deleted.')
    return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = [i for i in artists]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    data = []
    artists = []
    search_term = request.form.get("search_term").lower()
    for artist in db.session.query(Artist).with_entities(Artist.id, Artist.name).all():
        if search_term in artist.name.lower():
            artists.append(artist)
    for artist in artists:
        # Filter artist upcoming shows
        upcoming_shows = Show.query.filter_by(artist_id=artist.id).filter(
            Show.start_time > datetime.utcnow().isoformat()).all()
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(upcoming_shows)
        })
    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    data = []
    if artist:
        data = artist.__dict__

    # Filter artist past shows
    past_shows = Show.query.filter_by(artist_id=artist.id).filter(
        Show.start_time < datetime.utcnow().isoformat()).all()

    # Filter artist upcoming shows
    upcoming_shows = Show.query.filter_by(artist_id=artist.id).filter(
        Show.start_time > datetime.utcnow().isoformat()).all()

    # Format upcoming and past shows
    past_shows = format_artist_shows(past_shows)
    upcoming_shows = format_artist_shows(upcoming_shows)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
    
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    try:
        new_artist = Artist(name=form.name.data,
                            city=form.city.data,
                            state=form.state.data,
                            phone=form.phone.data,
                            image_link=form.image_link.data,
                            seeking_description=form.seeking_description.data,
                            facebook_link=form.facebook_link.data,
                            website=form.website.data,
                            genres=form.genres.data
                            )
        db.session.add(new_artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed.')
    except:
        flash('Something went wrong. Artist ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
