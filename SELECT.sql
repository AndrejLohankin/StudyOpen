SELECT Music_track_name, duration FROM Music_tracks
WHERE duration = (SELECT MAX(duration) FROM Music_tracks);

SELECT Music_track_name FROM Music_tracks
WHERE duration > 210;

SELECT Collection_name FROM Collection
WHERE Collection_year_of_release between 2018 and 2020;

SELECT musical_performer_name FROM musical_performers
WHERE musical_performer_name not like '% %';

SELECT Music_track_name FROM Music_tracks
WHERE Music_track_name like '%my%' or Music_track_name like '%мой%';

SELECT COUNT(musical_performer_ID), musical_genre_name FROM musical_performers_musical_genres
JOIN musical_genres ON musical_performers_musical_genres.musical_genre_ID = musical_genres.musical_genre_id
GROUP BY musical_genre_name;

SELECT COUNT(Music_track_name) FROM Music_tracks
JOIN albums ON Music_tracks.album_ID = albums.album_ID
WHERE album_year_of_release between 2019 and 2020;

SELECT AVG(duration), album_name FROM Music_tracks
JOIN albums ON Music_tracks.album_ID = albums.album_ID
GROUP BY album_name;

SELECT musical_performer_name FROM musical_performers
JOIN musical_performers_albums ON musical_performers_albums.musical_performer_ID = musical_performers.musical_performer_ID
JOIN albums ON albums.album_ID = musical_performers_albums.album_ID
WHERE album_year_of_release != 2020;

SELECT Collection_name FROM Collection
JOIN Collection_Music_tracks ON Collection_Music_tracks.Collection_ID = Collection.Collection_ID
JOIN Music_tracks ON Collection_Music_tracks.Music_track_ID = Music_tracks.Music_track_ID
JOIN albums ON albums.album_ID = Music_tracks.album_ID
JOIN musical_performers_albums ON musical_performers_albums.album_ID = albums.album_ID
JOIN musical_performers ON musical_performers.musical_performer_ID = musical_performers_albums.musical_performer_ID
WHERE musical_performer_name like 'Matrang';

SELECT album_name FROM albums
JOIN musical_performers_albums ON musical_performers_albums.album_ID = albums.album_ID
JOIN musical_performers ON musical_performers.musical_performer_ID = musical_performers_albums.musical_performer_ID
JOIN musical_performers_musical_genres ON musical_performers_musical_genres.musical_performer_ID = musical_performers.musical_performer_ID
GROUP BY album_name
HAVING COUNT(musical_performers_musical_genres.musical_performer_ID) > 1;

SELECT Music_track_name FROM Music_tracks
full JOIN Collection_Music_tracks ON Collection_Music_tracks.Music_track_ID = Music_tracks.Music_track_ID
WHERE Collection_Music_tracks.Collection_ID is null;

SELECT musical_performer_name FROM musical_performers
JOIN musical_performers_albums ON musical_performers_albums.musical_performer_ID = musical_performers.musical_performer_ID
JOIN albums ON albums.album_ID = musical_performers_albums.album_ID
JOIN Music_tracks ON Music_tracks.album_ID = albums.album_ID
WHERE Music_tracks.duration = (SELECT MIN(duration) FROM Music_tracks);

SELECT album_name FROM albums
JOIN Music_tracks ON Music_tracks.album_ID = albums.album_ID
group by album_name
ORDER BY COUNT(Music_tracks.music_track_name)
limit 1;