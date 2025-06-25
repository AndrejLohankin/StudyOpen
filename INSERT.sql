INSERT INTO musical_performers (musical_performer_name) 
VALUES('ATL');

INSERT INTO musical_performers (musical_performer_name) 
VALUES('Benny Benassi');

INSERT INTO musical_performers (musical_performer_name) 
VALUES('Silent Planet');

INSERT INTO musical_performers (musical_performer_name) 
VALUES('Matrang');

INSERT INTO musical_genres (musical_genre_name) 
VALUES('Pop');

INSERT INTO musical_genres (musical_genre_name) 
VALUES('Ambient');

INSERT INTO musical_genres (musical_genre_name) 
VALUES('Dance');

INSERT INTO albums (album_name, album_year_of_release)
VALUES('Fckswg x Trillogy', 2015);

INSERT INTO albums (album_name, album_year_of_release)
VALUES('Love is Gonna Save Us', 2003);

INSERT INTO albums (album_name, album_year_of_release)
VALUES('When The End Began', 2018);

INSERT INTO albums (album_name, album_year_of_release)
VALUES('С самим собой', 2019);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Божественный флоу', 138, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Король Мандрагоры', 164, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Доспехи', 184, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Love is Gonna Save Us', 205, 2);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Love is', 215, 2);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Thus spoke', 134, 3);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('The my Eternity', 205, 2);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('Afterdusk', 134, 3);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('С самим собой', 188, 4);

INSERT INTO Collection (Collection_name, Collection_year_of_release)
VALUES('Бодрое', 2020);

INSERT INTO Collection (Collection_name, Collection_year_of_release)
VALUES('Спокойное', 2024);

INSERT INTO Collection (Collection_name, Collection_year_of_release)
VALUES('Грустное', 2025);

INSERT INTO Collection (Collection_name, Collection_year_of_release)
VALUES('Веселое', 2025);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(1, 2);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(2, 4);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(3, 1);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(4, 1);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(5, 3);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(6, 3);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(7, 3);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(8, 4);

INSERT INTO Collection_Music_tracks (Music_track_ID, Collection_ID)
VALUES(9, 3);

INSERT INTO musical_performers_albums (musical_performer_ID, album_ID)
VALUES(1, 1);

INSERT INTO musical_performers_albums (musical_performer_ID, album_ID)
VALUES(2, 2);

INSERT INTO musical_performers_albums (musical_performer_ID, album_ID)
VALUES(3, 3);

INSERT INTO musical_performers_albums (musical_performer_ID, album_ID)
VALUES(4, 4);

INSERT INTO musical_performers_musical_genres (musical_genre_ID, musical_performer_ID)
VALUES(1, 1);

INSERT INTO musical_performers_musical_genres (musical_genre_ID, musical_performer_ID)
VALUES(3, 2);

INSERT INTO musical_performers_musical_genres (musical_genre_ID, musical_performer_ID)
VALUES(2, 3);

INSERT INTO musical_performers_musical_genres (musical_genre_ID, musical_performer_ID)
VALUES(2, 4);

INSERT INTO musical_performers_musical_genres (musical_genre_ID, musical_performer_ID)
VALUES(1, 3);

/* Дополнительные данные для проверки работоспособности запросов */

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('myself', 164, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('by myself', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('bemy self', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('myself by', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('by myself by', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('beemy', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('premyne', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('my own', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('own my', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('my', 100, 1);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('oh my god', 100, 1);

INSERT INTO albums (album_name, album_year_of_release)
VALUES('example album', 2010);

INSERT INTO Music_tracks (Music_track_name, duration, album_ID)
VALUES('example track', 100, 5);
