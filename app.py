import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash,Response
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'
import pyodbc

sql_server_config = {
    'server': 'localhost',  # Replace with your server name or instance
    'database': 'music',          # Replace with your database name
}

def get_sql_server_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_server_config['server']};"
        f"DATABASE={sql_server_config['database']};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


@app.route('/api/record_play', methods=['POST'])
def record_play():
    data = request.json
    user_id = data.get('user_id')
    song_id = data.get('song_id')
    print(f"Received data - user_id: {user_id}, song_id: {song_id}")
    if not user_id or not song_id:
        print ("nothing happening")
        return "Missing user_id or song_id", 400
        

    conn = get_sql_server_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO User_history (user_id, song_id)
            VALUES (?, ?)
        """, (user_id, song_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e), 500
    finally:
        conn.close()

    return "", 200
@app.route('/api/songs/<userId>',methods=['GET','POST'])
def get_songs(userId):
    # Connect to the database
    print (" in this function")
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM [user] WHERE id = ?", (userId,))
    user = cursor.fetchone()
    username = user[0]
    # Fetch song data
    print ("user name is",username)
    cursor.execute("EXEC generate_recommendations @username = ?", (username,))
    songs = [
        {
            "song_id": row[0],
            "title": row[1],
            "year": row[2],
            "path": url_for('serve_audio', filename=row[3]),  # Point to /audio/<filename>,
            "picture": url_for('static', filename=f'pictures/{row[4]}')
        }
        for row in cursor.fetchall()
    ]       
    conn.close()

    # Return the JSON response
    return jsonify({
        'songs': songs,
    })
@app.route('/audio/<filename>')
def serve_audio(filename):
    # Full path to the audio file
    audio_path = f'static/songs/{filename}'
    
    try:
        # Open the audio file in binary mode
        file = open(audio_path, 'rb')
        file_size = os.path.getsize(audio_path)

        # Handle Range header for partial content
        range_header = request.headers.get('Range', None)
        if not range_header:
            # No range header; serve the entire file
            return Response(file.read(), status=200, content_type="audio/mpeg")

        # Parse Range header for partial content
        byte_start, byte_end = range_header.replace("bytes=", "").split("-")
        byte_start = int(byte_start)
        byte_end = int(byte_end) if byte_end else file_size - 1

        file.seek(byte_start)
        chunk = file.read(byte_end - byte_start + 1)

        # Return partial content with appropriate headers
        response = Response(chunk, status=206, content_type="audio/mpeg")
        response.headers["Content-Range"] = f"bytes {byte_start}-{byte_end}/{file_size}"
        response.headers["Accept-Ranges"] = "bytes"
        return response

    except FileNotFoundError:
        return "File not found", 404
@app.route('/get_most_viewed/<category>/<username>', methods=['GET'])
def get_most_viewed(category, username):
    
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    if category == 'songs':
        query = """
            SELECT TOP 5 
                s.song_id, 
                s.title, 
                COUNT(uh.song_id) AS views
            FROM User_history uh
            JOIN [user] u ON u.id = uh.user_id
            JOIN song s ON uh.song_id = s.song_id
            WHERE u.Name = ?
            GROUP BY s.song_id, s.title
            ORDER BY views DESC
        """
    elif category == 'genres':
        query = """
            SELECT TOP 5 
                g.id, 
                g.name, 
                COUNT(uh.song_id) AS views
            FROM User_history uh
            JOIN [user] u ON u.id = uh.user_id
            JOIN song s ON uh.song_id = s.song_id
            JOIN Song_Genre sg ON s.song_id = sg.Song_ID
            JOIN genre g ON sg.Genre_ID = g.id
            WHERE u.Name = ?
            GROUP BY g.id, g.name
            ORDER BY views DESC
        """
    elif category == 'artists':
        query = """
            SELECT TOP 5 
                a.id, 
                a.name, 
                COUNT(uh.song_id) AS views
            FROM User_history uh
            JOIN [user] u ON u.id = uh.user_id
            JOIN song s ON uh.song_id = s.song_id
            JOIN Song_Artist sa ON s.song_id = sa.Song_ID
            JOIN artist a ON sa.Artist_ID = a.id
            WHERE u.Name = ?
            GROUP BY a.id, a.name
            ORDER BY views DESC
        """
    else:
        return {"error": "Invalid category"}, 400

    
    cursor.execute(query, (username,))
    results = [{"id": row[0], "name": row[1], "views": row[2]} for row in cursor.fetchall()]
    conn.close()

    return jsonify({'data': results}), 200


@app.route('/welcome/<username>', methods=['GET', 'POST'])
def welcome(username):
    # Connect to the database
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    # Fetch song data
    cursor.execute("EXEC generate_recommendations @username = ?", (username,))
    songs = [
        {
            "song_id": row[0],
            "title": row[1],
            "year": row[2],
            "path": url_for('static', filename=f'songs/{row[3]}'),
            "picture": url_for('static', filename=f'pictures/{row[4]}')
        }
        for row in cursor.fetchall()
    ]
    # Fetch user_id based on the username
    cursor.execute("SELECT id FROM [user] WHERE Name = ?", (username,))
    user = cursor.fetchone()
    user_id = user[0]

    # Fetch genres
    cursor.execute("SELECT ID, name FROM genre")
    genres = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

    # Fetch artists
    cursor.execute("SELECT ID, name FROM artist")
    artists = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

    cursor.execute("Select id,title from playlist where user_id = ?;", (user_id,))
    playlists = [{"id": row[0], "title": row[1]} for row in cursor.fetchall()]




    conn.close()
    

    # Pass the song, genre, and artist data to the template
    return render_template('songs.html', songs=songs, genres=genres, artists=artists,user_id=user_id,username=username , playlists = playlists)



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn =  get_sql_server_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM [user] WHERE name = ?", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user[0] == password:
            return redirect(url_for('welcome',username=username))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        dob = request.form.get('dob')
        password = request.form.get('password')

        if not password:
            password = None
        conn = get_sql_server_connection()
        cursor = conn.cursor()

        try:
            # Attempt to insert the new user
            cursor.execute("""
                INSERT INTO [user] (Name, Gender, Email, DOB, password) 
                VALUES (?, ?, ?, ?, ?)
            """, (name, gender, email, dob, password))
            conn.commit()
            cursor.execute("SELECT ID FROM [user] WHERE Email = ?", (email,))
            user = cursor.fetchone()
            user_id = user[0]
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('choose_genres', user_id=user_id))
        except pyodbc.IntegrityError as e:
            # Handle the T-SQL error for NOT NULL constraint or CHECK constraint
            if "Cannot insert the value NULL" in str(e):
                flash('All fields are required. Please fill out all fields.', 'danger')
            elif "Age must be at least 18 years." in str(e):
                flash('Age must be greater than or equal to 18.', 'danger')
            else:
                flash(f"Database error: {e}", 'danger')
        except Exception as e:
            if "a valid email address" in str(e):
                flash('Invalid email format. Please provide a valid email address.', 'danger')
            elif "Password must be" in str(e):
                flash('Password must be at least 8 characters long and include at least one letter and one number.', 'danger')
            elif "username already exists" in str(e):
                flash('This username already exists.','danger')
            else:
                flash(f"Unexpected error: {e}", 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')
@app.route('/choose_genres/<int:user_id>', methods=['GET', 'POST'])
def choose_genres(user_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, name, picture FROM Genre")
    genres = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        selected_genres = request.form.getlist('genres')
        conn = get_sql_server_connection()
        cursor = conn.cursor()

        for genre_id in selected_genres:
            cursor.execute("INSERT INTO user_genres (user_id, genre_id) VALUES (?, ?)", (user_id, genre_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('choose_artists', user_id=user_id))

    return render_template('genre.html', genres=genres, user_id=user_id)


@app.route('/choose_artists/<int:user_id>', methods=['GET', 'POST'])
def choose_artists(user_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, name, picture FROM Artist")
    artists = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        selected_artists = request.form.getlist('artists')
        conn = get_sql_server_connection()
        cursor = conn.cursor()

        for artist_id in selected_artists:
            cursor.execute("INSERT INTO user_artist (user_id, artist_id) VALUES (?, ?)", (user_id, artist_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Preferences saved! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('artist.html', artists=artists, user_id=user_id)
@app.route('/search', methods=['POST'])
def search():
    input_text = request.json.get('input', '')
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC search_options ?", input_text)
    
    # Fetch results
    artists = [row[0] for row in cursor.fetchall()]
    cursor.nextset()
    genres = [row[0] for row in cursor.fetchall()]
    cursor.nextset()
    songs = [row[0] for row in cursor.fetchall()]
    
    conn.close()

    return jsonify({'artists': artists, 'genres': genres, 'songs': songs})

@app.route('/fetch_songs', methods=['POST'])
def fetch_songs():
    data = request.json
    print("Received data:", data)  # Debug: Log received data

    input_value = data.get('inputValue')  # Value from dropdown
    search_type = data.get('type')       # Type (artist, genre, song)
    print("Input value:", input_value, "Type:", search_type)  # Debug: Log parsed input

    if not input_value or not search_type:
        print("Invalid input received.")  # Debug: Invalid input
        return jsonify({'error': 'Invalid input'}), 400

    try:
        conn = get_sql_server_connection()
        
        cursor = conn.cursor()

        # Call the stored procedure
        cursor.execute("EXEC sp_GetSongsByType ?, ?", (input_value, search_type))
        rows = cursor.fetchall()
        print("Fetched rows:", rows)  # Debug: Log fetched rows

        # Convert results to JSON
        songs = [
            {
                'song_id': row.song_id,
                'title': row.title,
                'year': row.yr_of_release,
                "path": url_for('static', filename=f'songs/{row[3]}'),
                "picture": url_for('static', filename=f'pictures/{row[4]}')
            }
            for row in rows
        ]
        

        return jsonify({'songs': songs})
    except Exception as e:
       
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
@app.route('/filter/songs', methods=['GET'])
def filter_songs():
    genre_id = request.args.get('genre_id', type=int)
    artist_id = request.args.get('artist_id', type=int)

    conn = get_sql_server_connection()
    cursor = conn.cursor()

    try:
        # Call the stored procedure with appropriate parameters
        cursor.execute("EXEC sp_FilterSongs @Genre_ID = ?, @Artist_ID = ?", (genre_id, artist_id))
        
        songs = [
            {
                "song_id": row[0],
                "title": row[1],
                "year": row[2],
                "path": url_for('static', filename=f'songs/{row[3]}'),
                "picture": url_for('static', filename=f'pictures/{row[4]}')
            }
            for row in cursor.fetchall()
        ]

        return jsonify({"songs": songs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/create_playlist/<int:user_id>', methods=['GET', 'POST']) 
def create_playlist(user_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    print("user id: "+ str(user_id))
    # Fetch all songs with their ID, title, and picture
    cursor.execute("SELECT Song_ID, title, picture FROM Song")
    songs = [{"id": row[0], "title": row[1], "picture": row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        selected_songs = request.form.getlist('songs')  # Get selected song IDs as a list

        if not playlist_name:
            flash('Please provide a name for the playlist.', 'danger')
            return render_template('create_playlist.html', songs=songs, user_id=user_id)

        if not selected_songs:
            flash('Please select at least one song for the playlist.', 'danger')
            return render_template('create_playlist.html', songs=songs, user_id=user_id)

        try:
            conn = get_sql_server_connection()
            cursor = conn.cursor()

            # Insert the playlist
            cursor.execute("INSERT INTO Playlist (Title, User_id) VALUES (?, ?)", (playlist_name, user_id))
            conn.commit()

            # Get the ID of the newly created playlist
            cursor.execute("SELECT id from Playlist where title = ? and User_id = ?;", (playlist_name, user_id))
            playlist_id = cursor.fetchone()[0]  # Fetch the generated ID

            # Insert songs into the playlist
            for song_id in selected_songs:
                cursor.execute("INSERT INTO Playlist_songs (playlist_id, Song_id) VALUES (?, ?)", (playlist_id, song_id))
            conn.commit()

            flash('Playlist created successfully!', 'success')
            cursor.execute("select name from [user] where id = ?", (user_id,))
            username = cursor.fetchone()[0]
            return redirect(url_for('welcome', username=username))

        except Exception as e:
            conn.rollback()
            if("A user cannot have duplicate playlist names." in str(e)):
                flash(f'Error creating playlist: A user cannot have duplicate playlist names.', 'danger')
                return redirect(url_for('create_playlist', user_id=user_id))
            flash(f'Error creating playlist: {e}', 'danger')
            return redirect(url_for('create_playlist', user_id=user_id))

        finally:
            cursor.close()
            conn.close()

    return render_template('create_playlist.html', songs=songs, user_id=user_id)

@app.route('/playlists/<int:user_id>', methods=['GET'])
def get_playlists(user_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    # Fetch playlists for the user
    cursor.execute("SELECT ID, Title FROM Playlist WHERE User_id = ?", (user_id,))
    playlists = [{"id": row[0], "title": row[1]} for row in cursor.fetchall()]

    conn.close()
    return jsonify({'playlists': playlists})

@app.route('/playlist_songs/<int:playlist_id>', methods=['GET'])
def get_playlist_songs(playlist_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    # Fetch songs in the playlist
    cursor.execute("""
        SELECT s.Song_ID, s.title, s.picture, s.yr_of_release, s.path
        FROM Playlist_songs ps
        JOIN Song s ON ps.Song_id = s.Song_ID
        WHERE ps.playlist_id = ?""", (playlist_id,))
    songs = [
        {
            "song_id": row[0],
            "title": row[1],
            "picture": url_for('static', filename=f'pictures/{row[2]}'),
            "year": row[3],
            "path": url_for('static', filename=f'songs/{row[4]}')
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify({'songs': songs})

# Example Flask route
@app.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    try:
        # Delete the playlist from the database
        conn = get_sql_server_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Playlist WHERE ID = ?"
        cursor.execute(query, (playlist_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Playlist deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_playlist/<int:user_id>/<int:playlist_id>', methods=['GET', 'POST'])
def update_playlist(user_id,playlist_id):
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Fetch playlist details
        cursor.execute("SELECT Title FROM Playlist WHERE ID = ?", (playlist_id,))
        playlist = cursor.fetchone()

        # Fetch songs in the playlist
        cursor.execute("""
            SELECT s.Song_ID, s.title, s.picture
            FROM Playlist_songs ps
            JOIN Song s ON ps.Song_id = s.Song_ID
            WHERE ps.playlist_id = ?
        """, (playlist_id,))
        playlist_songs = [{"id": row[0], "title": row[1], "picture": row[2]} for row in cursor.fetchall()]

        # Fetch all songs
        cursor.execute("SELECT Song_ID, title, picture FROM Song")
        all_songs = [{"id": row[0], "title": row[1], "picture": row[2]} for row in cursor.fetchall()]

        conn.close()
        return render_template('update_playlist.html', playlist=playlist, playlist_songs=playlist_songs, all_songs=all_songs)

    elif request.method == 'POST':
        new_title = request.form.get('playlist_name')
        selected_songs = request.form.getlist('songs')

        if not new_title:
            flash('Playlist name cannot be empty.', 'danger')
            return redirect(url_for('update_playlist', playlist_id=playlist_id))

        try:
            # Update playlist title
            conn = get_sql_server_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Playlist SET Title = ? WHERE ID = ?", (new_title, playlist_id))

            # Remove existing songs
            cursor.execute("DELETE FROM Playlist_songs WHERE Playlist_ID = ?", (playlist_id,))

            # Add new songs
            for song_id in selected_songs:
                cursor.execute("INSERT INTO Playlist_songs (Playlist_ID, Song_ID) VALUES (?, ?)", (playlist_id, song_id))

            conn.commit()


            # Fetch the username for redirection
            cursor.execute("SELECT name FROM [user] WHERE id = ?", (user_id,))
            username = cursor.fetchone()[0]
            return redirect(url_for('welcome', username=username))

        except Exception as e:
            conn.rollback()
            if "A user cannot have duplicate playlist names" in str(e):
                flash(f'Error updating playlist: A user cannot have duplicate playlist names.', 'danger')
                return redirect(url_for('update_playlist', playlist_id=playlist_id, user_id = user_id))

            flash(f'Error updating playlist: {e}', 'danger')
            return redirect(url_for('update_playlist', playlist_id=playlist_id, user_id = user_id))

        finally:
            conn.close()


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True,port=1000)
