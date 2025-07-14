create database music;
use music;
drop database music;

CREATE TABLE [user] (
    id INT IDENTITY(1,1) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    password VARCHAR(225) NOT NULL,
    DOB DATE NOT NULL,
    Gender VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    CONSTRAINT pkid PRIMARY KEY (id)
);
drop table [user];
drop table user_artist;
drop table user_genres;
drop table playlist_songs;
drop table playlist;

select * from playlist;

create table song (
song_id int primary key,
Title varchar(100),
yr_of_release int,
path varchar(200),
picture varchar(200));

CREATE TABLE Artist
(
    ID int,
    name VARCHAR(90),
    picture VARCHAR(250),
    constraint PK_Artist_ID Primary key(ID)
    
);

CREATE TABLE Genre
(
    ID int,
    name VARCHAR(90),
    picture VARCHAR(250),
    constraint PK_Genre_ID Primary key(ID)
);
alter table genre
add picture varchar(250);

Create table Playlist
(
ID int IDENTITY(1,1),
Title varchar(20),
User_id int,
Constraint Pk_playlist primary key (ID),
Constraint fk_playlist foreign key(User_id) references [user](ID) on delete cascade on update cascade

); 
alter table Playlist
drop constraint PK_playlist;
select * from playlist; drop table playlist;
delete from Playlist;

Create table Playlist_songs
(
playlist_id int,
Song_id int,
Constraint Pk_songplaylist primary key(playlist_id,Song_id),
Constraint Fk_songplay1 foreign key(playlist_id) references Playlist(ID) On Update cascade on delete cascade,
Constraint Fk_songplay2 foreign key(Song_id) references Song(song_ID) on update cascade on delete cascade
);
select * from Playlist_songs;
drop table Playlist_songs;
create table user_genres(
user_id int,
genre_id int,
constraint pk_user_genres primary key (user_id,genre_id),
constraint fk_user_id foreign key (user_id) references [user](id) on update cascade on delete cascade,
constraint fk_genre_id foreign key (genre_id) references genre(ID)on update cascade on delete cascade);

create table user_artist(
user_id int,
artist_id int,
constraint pk_user_artist primary key (user_id,artist_id),
constraint fk_usser_id foreign key (user_id) references [user](id) on update cascade on delete cascade,
constraint fk_artist_id foreign key (artist_id) references artist(ID) on update cascade on delete cascade);

CREATE TABLE Song_Artist
(
    Song_ID int,
    Artist_ID int,
    Constraint FK_Song_ID_2 Foreign Key(Song_ID) References song(song_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Constraint FK_Artist_ID1 Foreign Key(Artist_ID) References Artist(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    Primary Key(Song_ID, Artist_ID)
);
CREATE TABLE Song_Genre
(
    Song_ID int,
    Genre_ID int,
    Constraint FK_Song_ID1 Foreign Key(Song_ID) References song(song_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Constraint FK_Genre_ID22 Foreign Key(Genre_ID) References Genre(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    Primary key (Song_ID,Genre_ID)
);
go
CREATE TRIGGER trg_CheckSignupConditions
ON [user]
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Validate Password: Minimum 8 characters, at least one letter and one number
    IF EXISTS (
        SELECT 1
        FROM inserted
        WHERE NOT (
            LEN(password) >= 8 AND
            password LIKE '%[a-zA-Z]%' AND
            password LIKE '%[0-9]%'
        )
    )
    BEGIN
        RAISERROR ('Password must be at least 8 characters long and include at least one letter and one number.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Validate Email: Must have @ and a domain (basic format check)
    IF EXISTS (
        SELECT 1
        FROM inserted
        WHERE NOT (email LIKE '%@%.%')
    )
    BEGIN
        RAISERROR ('Invalid email format. Please provide a valid email address.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Validate DOB: Ensure age is at least 18 years
    IF EXISTS (
        SELECT 1
        FROM inserted
        WHERE DATEDIFF(YEAR, dob, GETDATE()) < 18
    )
    BEGIN
        RAISERROR ('Age must be at least 18 years.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;
GO

delete from [user];

Select * from [user];

INSERT INTO Artist (ID, name, picture) 
VALUES 
    (1, 'Taylor Swift', 'taylor.jpeg'),
    (2, 'Ed Sheeran', 'edsheeran.jpeg'),
    (3, 'Beyonce', 'beyonce.jpeg');

	delete from Artist;

Select * from Artist;
Select * from Genre;
INSERT INTO Genre (ID, name, picture) 
VALUES 
    (1, 'Pop', 'pop.jpeg'),
    (2, 'Rock', 'ROck.jpeg'),
    (3, 'Jazz', 'jazz.jpeg');

select * from genre;
delete from genre;

INSERT INTO Genre (ID, name, picture) 
VALUES
   (4,'Blues','Blues.jpeg'),
   (5,'Classical','Classical.jpeg'),
   (6,'Country','country.jpeg'),
   (7,'Electronic','Electronic.jpeg'),
   (8,'Folk','Folk.jpeg'),
   (9,'Indie','Indie.jpeg'),
   (10,'Hiphop','Hiphop.jpeg'),
   (11,'Metal','Metal.jpeg'),
   (12,'Opera','opera.jpeg'),
   (13,'Punk','Punk.png'),
   (14,'R&B','R&B.jpeg'),
   (15,'Rap','Rap.png'),
   (16,'Reggae','Reggae.jpeg'),
   (17,'Ska','ska.jpeg'),
   (18,'Techno','Techno.jpeg'),
   (19,'World','World.jpeg'),
   (20,'Disco','disco.jpeg');

INSERT INTO Artist (ID, Name, Picture)
VALUES 
    
    (4, 'Justin Bieber', 'Justin Bieber.jpeg'),
    (5, 'Dua Lipa', 'Dua Lipa.jpeg'),
    (6, 'Alan Walker', 'Alan Walker.jpeg'),
    (7, 'Talha Anjum', 'Talha Anjum.jpeg'),
    (8, 'Adele', 'Adele.jpeg'),
    (9, 'Beatles', 'Beatles.jpeg'),
    
    (10, 'Billie Eilish', 'Billie Eilish.jpeg'),
    (11, 'Duncan Laurence', 'Duncan Lawrence.jpeg'),
    (12, 'Momina Mustehsan', 'Momina.jpeg'),
    (13, 'Avicii', 'Avicii.jpeg'),
    (14, 'Anuv Jain', 'Anuv.jpeg'),
    (15, 'Imagine Dragons', 'Imagine.jpeg'),
    (16, 'Alec Benjamin', 'Alec.jpg'),
    (17, 'Stephan Sanchez', 'Stefan.jpeg'),
    (18, 'Karun Aujla', 'Karun.jpeg'),
    (19, 'Bad Bunny', 'Bad.jpeg'),
    (20, 'Arijit Singh', 'Argit.jpeg'), 
    (21, 'Diljit Dosanjh', 'Diljit.jpeg'), 
    (22, 'Shubh', 'Shubh.jpg'), 
    (23, 'Atif Aslam', 'Atif Aslam.jpeg'), 
    (24, 'Aur', 'Aur.jpeg'), 
    (25, 'Pritam', 'Pritam.jpeg'),
    (26, 'Quratulain Baloch', 'qurat.jpg'),
    (27,'Nusrat Fateh Ali Khan','Nusrat.png');

	select * from artist;

	INSERT INTO Song (song_id, Title, yr_of_release, path, picture)
VALUES
	(37, 'Metamorphosis', 2023, 'Metamorphosis-Interworld.mp3', 'Metamorphosis.jpg'),
    (38, 'MyEyes', 2012, 'MyEyes-TravisScott.mp3', 'MyEyes.jpg'),
	(39, 'NahinMilta', 2023, 'NahinMilta-Bayaan.mp3', 'NahinMilta.jpg'),
    (40, 'OMaahi', 2012, 'OMaahi-Arijit.mp3', 'OMaahi.jpg'),
	(41, 'OneAndOnly', 2023, 'OneAndOnly-Adele.mp3', 'OneAndOnly.jpg'),
    (42, 'SacrificeTomorrow', 2012, 'SacrificeTomorrow-Alec.mp3', 'SacrificeTomorrow.jpg'),
	(43, 'SeeYouAgain', 2023, 'SeeYouAgain-CharliePuth.mp3', 'SeeYouAgain.jpg'),
    (44, 'ShapeOfYou', 2012, 'ShapeOfYou-EdSheeran.mp3', 'ShapeOfYou.jpg'),
	(45, 'Softcore', 2023, 'Softcore-Neighbourhood.mp3', 'Softcore.jpg'),
    (46, 'Spectre', 2012, 'Spectre-AlanWalker.mp3', 'Spectre.jpg'),
	(47, 'SummerHigh', 2023, 'SummerHigh-ApDhillon.mp3', 'SummerHigh.jpg'),
    (48, 'SweaterWeather', 2012, 'SweaterWeather-Neighbourhood.mp3', 'SweaterWeather.jpg'),
	(49, 'TheNights', 2023, 'TheNights-Avicii.mp3', 'TheNights.jpg'),
    (50, 'WithoutMe', 2012, 'WithoutMe-Eminem.mp3', 'WithoutMe.jpg');

	select * from song;
	insert into Song_Genre VALUES
    (6,1),(7,15),(7,10),(8,6),(8,1),(8,8),(9,9),(9,1),(9,8),(11,7),(12,1),(13,1),(14,2),(15,10),(16,9),(16,1),
    (17,1),(18,9),(18,1),(19,1),(20,10),(21,2),(22,7),(23,10),(23,2),(24,15),(24,10),(25,1),(26,9),(26,1),
    (27,1),(27,6),(28,10),(29,10),(30,10),(31,1),(31,14),(32,9),(32,1),(32,8),(33,6),(33,8),(34,1),(35,1),
    (36,1),(37,7),(38,10),(38,2),(39,2),(39,9),(40,6),(41,1),(42,1),(43,1),(44,1),(45,9),(46,7),(47,10),(48,9),
    (49,7),(50,15),(50,10);

	select * from Song_Genre;

    insert into Song_Artist VALUES
    (6,2),(7,7),(8,20),(9,14),(10,8),(12,11),(14,15),(16,24),(19,16),(20,22),(22,6),(24,7),(27,20),(31,3),(32,14),
    (33,20),(34,21),(35,16),(36,1),(40,20),(41,8),(42,16),(44,2),(46,6),(49,13);

	select * from Song_Artist;
	CREATE TABLE User_history
(
  user_id int,
  song_id int,
  CONSTRAINT FKUser_history1 Foreign key(user_id) REFERENCES [user](id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FKUser_history2 Foreign key(song_id) REFERENCES song(song_id) ON DELETE CASCADE ON UPDATE CASCADE,
  Primary key(user_id,song_id),
);
go
CREATE PROCEDURE search_options 
	@input nvarchar(100)
	AS
	BEGIN 
		Select name from Artist  where name like '%' + @input + '%'; 
		Select name from Genre where name like '%' + @input + '%';
		Select title from song where title like '%' + @input + '%';
	end	;	
	GO

	GO
	CREATE PROCEDURE sp_GetSongsByType
    @inputValue NVARCHAR(255), -- The value selected by the user
    @type NVARCHAR(50)         -- The type (can be 'artist', 'genre', or 'song')
AS
BEGIN

    IF @type = 'artist'
    BEGIN
        
        SELECT 
            s.song_id, s.title, s.yr_of_release, s.path, s.picture
        FROM 
            song s
        INNER JOIN 
            song_artist sa ON s.song_id = sa.song_id
        INNER JOIN 
            artist a ON sa.artist_id = a.id
        WHERE 
            a.name = @inputValue;
    END
    ELSE IF @type = 'genre'
    BEGIN
       
        SELECT 
            s.song_id, s.title, s.yr_of_release, s.path, s.picture
        FROM 
            song s
        INNER JOIN 
            song_genre sg ON s.song_id = sg.song_id
        INNER JOIN 
            genre g ON sg.genre_id = g.id
        WHERE 
            g.name = @inputValue;
    END
    ELSE IF @type = 'song'
    BEGIN
       
        SELECT 
            song_id, title, yr_of_release, path, picture
        FROM 
            song
        WHERE 
            title = @inputValue;
 ���END

����
END
	select * from [user];

	GO

	CREATE PROCEDURE sp_FilterSongs
    @Genre_ID INT = NULL,
    @Artist_ID INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT DISTINCT 
        s.song_id,
        s.Title,
        s.yr_of_release,
        s.path,
        s.picture
    FROM 
        song AS s
    LEFT JOIN 
        song_genre AS sg ON s.song_id = sg.Song_ID
    LEFT JOIN 
        song_artist AS sa ON s.song_id = sa.Song_ID
    WHERE
        (@Genre_ID IS NULL OR sg.Genre_ID = @Genre_ID)
        AND (@Artist_ID IS NULL OR sa.Artist_ID = @Artist_ID)
    ORDER BY
        s.Title; -- Optional: Adjust ordering�if�needed
END

GO

CREATE PROCEDURE generate_recommendations (@username VARCHAR(50))
AS
BEGIN
    -- Declare necessary variables
    DECLARE @user_id INT;

    -- Retrieve user_id based on the provided username
    SELECT @user_id = id FROM [user] WHERE Name = @username;

    -- Check if the user exists
    IF @user_id IS NULL
    BEGIN
        PRINT 'User not found';
        RETURN;
    END

    -- Retrieve songs with similar artist and genre based on User_history if records exist
    IF EXISTS (SELECT 1 FROM User_history WHERE user_id = @user_id)
    BEGIN
        SELECT DISTINCT s.*
        From song s
        JOIN Song_Artist sa ON s.song_id = sa.Song_ID
        WHERE sa.Artist_ID IN (
            SELECT sa2.Artist_ID FROM User_history uh2
            JOIN Song_Artist sa2 ON uh2.song_id = sa2.Song_ID
            WHERE uh2.user_id = @user_id
        )
        UNION
        SELECT DISTINCT s.*
        From song s
        JOIN Song_Genre sg ON s.song_id = sg.Song_ID
         where sg.Genre_ID IN (
            SELECT sg2.Genre_ID FROM User_history uh3
            JOIN Song_Genre sg2 ON uh3.song_id = sg2.Song_ID
            WHERE uh3.user_id = @user_id
        );
    END
    ELSE
    BEGIN
        -- Retrieve songs based on both genres and artists if records exist in both
        IF EXISTS (SELECT 1 FROM user_genres WHERE user_id = @user_id) AND EXISTS (SELECT 1 FROM user_artist WHERE user_id = @user_id)
        BEGIN
            SELECT DISTINCT s.*
            FROM song as s
            Join Song_genre as sg on sg.Song_ID=s.song_id
            where sg.Genre_ID IN (select ug.Genre_ID from user_genres as ug join [user] as u on ug.user_id=u.id where u.id=@user_id)
            UNION
            SELECT DISTINCT s.*
            FROM song as s
            Join Song_Artist as sg on sg.Song_ID=s.song_id
            where sg.Artist_ID IN (select ug.artist_id from user_artist as ug join [user] as u on ug.user_id=u.id where u.id=@user_id)
        END
        -- Retrieve songs based on genres only if records exist
        ELSE IF EXISTS (SELECT 1 FROM user_genres WHERE user_id = @user_id)
        BEGIN
        SELECT DISTINCT s.*
            FROM song as s
            Join Song_genre as sg on sg.Song_ID=s.song_id
            where sg.Genre_ID IN (select ug.Genre_ID from user_genres as ug join [user] as u on ug.user_id=u.id where u.id=@user_id)
            
        END
        -- Retrieve songs based on artists only if records exist
        ELSE IF EXISTS (SELECT 1 FROM user_artist WHERE user_id = @user_id)
        BEGIN
        SELECT DISTINCT s.*
            FROM song as s
            Join Song_Artist as sg on sg.Song_ID=s.song_id
            where sg.Artist_ID IN (select ug.artist_id from user_artist as ug join [user] as u on ug.user_id=u.id where u.id=@user_id)
            
        END
        -- Retrieve all songs if no preferences are found
        ELSE
        BEGIN
            SELECT * FROM song;
       �END
����END
END
GO


select * from [user];

EXEC generate_recommendations @username = 37;

go
CREATE TRIGGER trg_PreventDuplicateUserName
ON [user]
INSTEAD OF INSERT
AS
BEGIN
    -- Check for duplicate usernames
    IF EXISTS (
        SELECT 1
        FROM [user] u
        INNER JOIN inserted i
        ON u.Name = i.Name
    )
    BEGIN
        -- If duplicate found, raise an error and rollback
        RAISERROR ('A user with this username already exists.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
    
    -- If no duplicates, proceed with the insertion
    INSERT INTO [user] (Name, password, DOB, Gender, Email)
    SELECT Name, password, DOB, Gender, Email
    FROM inserted;
END;
GO
select * from playlist;
alter table playlist
add constraint unique_title Unique(Title);

select * from user_genres;
delete from user_genres where user_id = 38;
