create table musical_genres (
	musical_genre_ID SERIAL primary key,
	musical_genre_name VARCHAR(60) not null
);

create table musical_performers (
	musical_performer_ID SERIAL primary key,
	musical_performer_name VARCHAR(60) not null
);

create table musical_performers_musical_genres (
	primary key (musical_genre_ID, musical_performer_ID),
	musical_genre_ID integer REFERENCES musical_genres (musical_genre_ID),
	musical_performer_ID integer REFERENCES musical_performers (musical_performer_ID)
);

create table albums (
	album_ID SERIAL primary key,
	album_name VARCHAR(60) not null,
	album_year_of_release integer not null
);

create table musical_performers_albums (
	primary key (album_ID, musical_performer_ID),
	musical_performer_ID integer REFERENCES musical_performers (musical_performer_ID),
	album_ID integer REFERENCES albums (album_ID)
);

create table Music_tracks (
	Music_track_ID SERIAL primary key,
	Music_track_name VARCHAR(60) not null,
	duration integer check (duration > 0 and duration <300),
	album_ID integer REFERENCES albums (album_ID)
);

create table Collection (
	Collection_ID SERIAL primary key,
	Collection_name VARCHAR(60) not null,
	Collection_year_of_release integer not null
);

create table Collection_Music_tracks (
	primary key (Music_track_ID, Collection_ID),
	Music_track_ID integer REFERENCES Music_tracks (Music_track_ID),
	Collection_ID integer REFERENCES Collection (Collection_ID)
);