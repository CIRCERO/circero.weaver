# -*- coding: utf-8 -*-
class VideoDatabase():
    def __init__(self, cursor):
        self.cursor = cursor

    def update_movie(self, *args):
        self.cursor.execute("UPDATE movie SET c00 = ?, c01 = ?, c02 = ?, c03 = ?, c04 = ?, c05 = ?, c06 = ?, c07 = ?, c09 = ?, c10 = ?, c11 = ?, c12 = ?, c14 = ?, c15 = ?, c16 = ?, c18 = ?, c19 = ?, c21 = ?, userrating = ?, premiered = ? WHERE idMovie = ?", args)

    def update_movie_nouserrating(self, *args):
        self.cursor.execute("UPDATE movie SET c00 = ?, c01 = ?, c02 = ?, c03 = ?, c04 = ?, c05 = ?, c06 = ?, c07 = ?, c09 = ?, c10 = ?, c11 = ?, c12 = ?, c14 = ?, c15 = ?, c16 = ?, c18 = ?, c19 = ?, c21 = ?, premiered = ? WHERE idMovie = ?", args)

    def add_movie(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO movie (idMovie, idFile, c00, c01, c02, c03, c04, c05, c06, c07, c09, c10, c11, c12, c14, c15, c16, c18, c19, c21, userrating, premiered) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

    def add_movie_nouserrating(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO movie (idMovie, idFile, c00, c01, c02, c03, c04, c05, c06, c07, c09, c10, c11, c12, c14, c15, c16, c18, c19, c21, premiered) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

    def create_movie_entry(self):
        self.cursor.execute("SELECT coalesce(max(idMovie), 0) FROM movie")
        return self.cursor.fetchone()[0] + 1

    def delete_movie(self, kodi_id, file_id):
        self.cursor.execute("DELETE FROM movie WHERE idMovie = ?", (kodi_id,))
        self.cursor.execute("DELETE FROM files WHERE idFile = ?", (file_id,))

    def get_movie(self, *args):
        self.cursor.execute("SELECT * FROM movie WHERE idMovie = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def update_musicvideos(self, *args):
        self.cursor.execute("UPDATE musicvideo SET c00 = ?, c04 = ?, c05 = ?, c06 = ?, c07 = ?, c08 = ?, c09 = ?, c10 = ?, c11 = ?, c12 = ?, premiered = ? WHERE idMVideo = ?", args)

    def add_musicvideos(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO musicvideo (idMVideo,idFile, c00, c04, c05, c06, c07, c08, c09, c10, c11, c12, premiered) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

    def create_entry_musicvideos(self):
        self.cursor.execute("SELECT coalesce(max(idMVideo), 0) FROM musicvideo")
        return self.cursor.fetchone()[0] + 1

    def delete_musicvideos(self, kodi_id, file_id):
        self.cursor.execute("DELETE FROM musicvideo WHERE idMVideo = ?", (kodi_id,))
        self.cursor.execute("DELETE FROM files WHERE idFile = ?", (file_id,))

    def get_musicvideos(self, *args):
        self.cursor.execute("SELECT * FROM musicvideo WHERE idMVideo = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def update_tvshow(self, *args):
        self.cursor.execute("UPDATE tvshow SET c00 = ?, c01 = ?, c02 = ?, c04 = ?, c05 = ?, c08 = ?, c09 = ?, c10 = ?, c12 = ?, c13 = ?, c14 = ?, c15 = ? WHERE idShow = ?", args)

    def add_tvshow(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO tvshow(idShow, c00, c01, c02, c04, c05, c08, c09, c10, c12, c13, c14, c15) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

    def create_entry(self):
        self.cursor.execute("SELECT coalesce(max(idShow), 0) FROM tvshow")
        return self.cursor.fetchone()[0] + 1

    def create_entry_set(self):
        self.cursor.execute("SELECT coalesce(max(idSet), 0) FROM sets")
        return self.cursor.fetchone()[0] + 1

    def get_tvshow(self, *args):
        self.cursor.execute("SELECT * FROM tvshow WHERE idShow = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def create_entry_country(self):
        self.cursor.execute("SELECT coalesce(max(country_id), 0) FROM country")
        return self.cursor.fetchone()[0] + 1

    def create_entry_unique_id(self):
        self.cursor.execute("SELECT coalesce(max(uniqueid_id), 0) FROM uniqueid")
        return self.cursor.fetchone()[0] + 1

    def add_unique_id(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO uniqueid(uniqueid_id, media_id, media_type, value, type) VALUES (?, ?, ?, ?, ?)", args)

    def add_countries(self, countries, *args):
        for country in countries:
            self.cursor.execute("INSERT OR REPLACE INTO country_link(country_id, media_id, media_type) VALUES (?, ?, ?)", (self.get_country(country),) + args)

    def add_country(self, *args):
        country_id = self.create_entry_country()
        self.cursor.execute("INSERT OR REPLACE INTO country(country_id, name) VALUES (?, ?)", (country_id,) + args)
        return country_id

    def get_country(self, *args):
        self.cursor.execute("SELECT country_id FROM country WHERE name = ? COLLATE NOCASE", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return self.add_country(*args)

    def add_boxset(self, *args):
        set_id = self.create_entry_set()
        self.cursor.execute("INSERT OR REPLACE INTO sets(idSet, strSet, strOverview) VALUES (?, ?, ?)", (set_id,) + args)
        return set_id

    def update_boxset(self, *args):
        self.cursor.execute("UPDATE sets SET strSet = ?, strOverview = ? WHERE idSet = ?", args)

    def set_boxset(self, *args):
        self.cursor.execute("UPDATE movie SET idSet = ? WHERE idMovie = ?", args)

    def remove_from_boxset(self, *args):
        self.cursor.execute("UPDATE movie SET idSet = null WHERE idMovie = ?", args)

    def delete_boxset(self, *args):
        self.cursor.execute("DELETE FROM sets WHERE idSet = ?", args)

    def create_entry_season(self):
        self.cursor.execute("SELECT coalesce(max(idSeason), 0) FROM seasons")
        return self.cursor.fetchone()[0] + 1

    def create_entry_episode(self):
        self.cursor.execute("SELECT coalesce(max(idEpisode), 0) FROM episode")
        return self.cursor.fetchone()[0] + 1

    def get_episode(self, *args):
        self.cursor.execute("SELECT * FROM episode WHERE idEpisode = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def get_total_episodes(self, *args):
        self.cursor.execute("SELECT totalCount FROM tvshowcounts WHERE idShow = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def link(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO tvshowlinkpath(idShow, idPath) VALUES (?, ?)", args)

    def get_season(self, name, *args):
        self.cursor.execute("SELECT idSeason FROM seasons WHERE idShow = ? AND season = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            season_id = Data[0]
        else:
            season_id = self.add_season(*args)

        if name:
            self.cursor.execute("UPDATE seasons SET name = ? WHERE idSeason = ?", (name, season_id))

        return season_id

    def add_season(self, *args):
        season_id = self.create_entry_season()
        self.cursor.execute("INSERT OR REPLACE INTO seasons(idSeason, idShow, season) VALUES (?, ?, ?)", (season_id,) + args)
        return season_id

    def add_episode(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO episode(idEpisode, idFile, c00, c01, c03, c04, c05, c09, c10, c12, c13, c14, idShow, c15, c16, idSeason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

    def update_episode(self, *args):
        self.cursor.execute("UPDATE episode SET c00 = ?, c01 = ?, c03 = ?, c04 = ?, c05 = ?, c09 = ?, c10 = ?, c12 = ?, c13 = ?, c14 = ?, c15 = ?, c16 = ?, idSeason = ?, idShow = ? WHERE idEpisode = ?", args)

    def delete_tvshow(self, *args):
        self.cursor.execute("DELETE FROM tvshow WHERE idShow = ?", args)

    def delete_season(self, *args):
        self.cursor.execute("DELETE FROM seasons WHERE idSeason = ?", args)

    def delete_episode(self, kodi_id, file_id):
        self.cursor.execute("DELETE FROM episode WHERE idEpisode = ?", (kodi_id,))
        self.cursor.execute("DELETE FROM files WHERE idFile = ?", (file_id,))

    def create_entry_path(self):
        self.cursor.execute("SELECT coalesce(max(idPath), 0) FROM path")
        return self.cursor.fetchone()[0] + 1

    def create_entry_file(self):
        self.cursor.execute("SELECT coalesce(max(idFile), 0) FROM files")
        return self.cursor.fetchone()[0] + 1

    def create_entry_rating(self):
        self.cursor.execute("SELECT coalesce(max(rating_id), 0) FROM rating")
        return self.cursor.fetchone()[0] + 1

    def create_entry_person(self):
        self.cursor.execute("SELECT coalesce(max(actor_id), 0) FROM actor")
        return self.cursor.fetchone()[0] + 1

    def create_entry_genre(self):
        self.cursor.execute("SELECT coalesce(max(genre_id), 0) FROM genre")
        return self.cursor.fetchone()[0] + 1

    def create_entry_studio(self):
        self.cursor.execute("SELECT coalesce(max(studio_id), 0) FROM studio")
        return self.cursor.fetchone()[0] + 1

    def create_entry_bookmark(self):
        self.cursor.execute("SELECT coalesce(max(idBookmark), 0) FROM bookmark")
        return self.cursor.fetchone()[0] + 1

    def create_entry_tag(self):
        self.cursor.execute("SELECT coalesce(max(tag_id), 0) FROM tag")
        return self.cursor.fetchone()[0] + 1

    def add_path(self, *args):
        path_id = self.get_path(*args)

        if path_id is None:
            path_id = self.create_entry_path()
            self.cursor.execute("INSERT OR REPLACE INTO path(idPath, strPath, strScraper, noUpdate) VALUES (?, ?, 'metadata.local', 1)", (path_id,) + args)

        return path_id

    def create_file(self):
        file_id = self.create_entry_file()
        return file_id





    def add_file(self, path_id, filename, dateAdded, file_id):
#        self.cursor.execute("INSERT OR REPLACE INTO files(idFile, idPath, strFilename) VALUES (?, ?, ?)", (file_id, path_id, filename))



        self.cursor.execute("INSERT OR REPLACE INTO files(idPath, strFilename, dateAdded, idPath) VALUES (?, ?, ?, ?)", (path_id, filename, dateAdded, file_id))



    def get_path(self, *args):
        self.cursor.execute("SELECT idPath FROM path WHERE strPath = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return None

    def update_path(self, *args):
        self.cursor.execute("UPDATE path SET strPath = ?, strContent = ?, strScraper = ?, noUpdate = ? WHERE idPath = ?", args)

    def add_link(self, link, person_id, args):
        self.cursor.execute("SELECT * FROM {LinkType} WHERE actor_id = ? AND media_id = ? AND media_type = ? COLLATE NOCASE".replace("{LinkType}", link), (person_id,) + args)
        Temp = self.cursor.fetchone()

        #No primary Key in DB -> INSERT OR REPLACE not working -> check manually
        if not Temp:
            self.cursor.execute("INSERT OR REPLACE INTO {LinkType}(actor_id, media_id, media_type) VALUES (?, ?, ?)".replace("{LinkType}", link), (person_id,) + args)

    def remove_path(self, *args):
        self.cursor.execute("DELETE FROM path WHERE idPath = ?", args)


    def update_file(self, *args):
        self.cursor.execute("UPDATE files SET idPath = ?, strFilename = ?, dateAdded = ? WHERE idFile = ?", args)

    def remove_file(self, path, *args):
        path_id = self.get_path(path)

        if path_id is not None:
            self.cursor.execute("DELETE FROM files WHERE idPath = ? AND strFileName = ?", (path_id,) + args)

    def get_filename(self, *args):
        self.cursor.execute("SELECT strFilename FROM files WHERE idFile = ?", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return ""

    def update_person(self, image_url, kodi_id, media, image):
        if image == 'poster' and media in ('song', 'artist', 'album'):
            return

        self.cursor.execute("SELECT url FROM art WHERE media_id = ? AND media_type = ? AND type = ?", (kodi_id, media, image,))
        result = self.cursor.fetchone()

        if result:
            url = result[0]

            if url != image_url:
                if image_url:
#                    self.LOG.info("UPDATE to kodi_id %s art: %s" % (kodi_id, image_url))
                    self.cursor.execute("UPDATE art SET url = ? WHERE media_id = ? AND media_type = ? AND type = ?", (image_url, kodi_id, media, image))
        else:
#            self.LOG.debug("ADD to kodi_id %s art: %s" % (kodi_id, image_url))
            self.cursor.execute("INSERT OR REPLACE INTO art(media_id, media_type, type, url) VALUES (?, ?, ?, ?)", (kodi_id, media, image, image_url))

    def add_people(self, people, *args):
        cast_order = 1

        for person in people:
            if 'Name' not in person:
#                self.LOG.error("Unable to identify person object")
#                self.LOG.error(person)
                continue

            person_id = self.get_person(person['Name'])

            if person['Type'] == 'Actor':
                role = person.get('Role')
                self.cursor.execute("INSERT OR REPLACE INTO actor_link(actor_id, media_id, media_type, role, cast_order) VALUES (?, ?, ?, ?, ?)", (person_id,) + args + (role, cast_order,))
                cast_order += 1
            elif person['Type'] == 'Director':
                self.add_link('director_link', person_id, args)
            elif person['Type'] == 'Writer':
                self.add_link('writer_link', person_id, args)
            elif person['Type'] == 'Artist':
                self.add_link('actor_link', person_id, args)

            if person['imageurl']:
                art = person['Type'].lower()
                if "writing" in art:
                    art = "writer"

                self.update_person(person['imageurl'], person_id, art, "thumb")

    def add_person(self, *args):
        person_id = self.create_entry_person()
        self.cursor.execute("INSERT OR REPLACE INTO actor(actor_id, name) VALUES (?, ?)", (person_id,) + args)
        return person_id

    def get_person(self, *args):
        self.cursor.execute("SELECT actor_id FROM actor WHERE name = ? COLLATE NOCASE", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return self.add_person(*args)

    #Delete current genres first for clean slate
    def add_genres(self, genres, *args):
        self.cursor.execute("DELETE FROM genre_link WHERE media_id = ? AND media_type = ?", args)

        for genre in genres:
            self.cursor.execute("INSERT OR REPLACE INTO genre_link(genre_id, media_id, media_type) VALUES (?, ?, ?)", (self.get_genre(genre),) + args)

    def add_genre(self, *args):
        genre_id = self.create_entry_genre()
        self.cursor.execute("INSERT OR REPLACE INTO genre(genre_id, name) VALUES (?, ?)", (genre_id,) + args)
        return genre_id

    def get_genre(self, *args):
        self.cursor.execute("SELECT genre_id FROM genre WHERE name = ? COLLATE NOCASE", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return self.add_genre(*args)

    def add_studios(self, studios, *args):
        for studio in studios:
            studio_id = self.get_studio(studio)
            self.cursor.execute("INSERT OR REPLACE INTO studio_link(studio_id, media_id, media_type) VALUES (?, ?, ?)", (studio_id,) + args)

    def add_studio(self, *args):
        studio_id = self.create_entry_studio()
        self.cursor.execute("INSERT OR REPLACE INTO studio(studio_id, name) VALUES (?, ?)", (studio_id,) + args)
        return studio_id

    def get_studio(self, *args):
        self.cursor.execute("SELECT studio_id FROM studio WHERE name = ? COLLATE NOCASE", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return self.add_studio(*args)

    #First remove any existing entries
    #Then re-add video, audio and subtitles
    def add_streams(self, file_id, streams, runtime):
        self.cursor.execute("DELETE FROM streamdetails WHERE idFile = ?", (file_id,))

        if streams:
            for track in streams['video']:
                track['KodiFileId'] = file_id
                track['Runtime'] = runtime
                self.add_stream_video(track['KodiFileId'], 0, track['codec'], track['aspect'], track['width'], track['height'], track['Runtime'], track['3d'])

            for track in streams['audio']:
                track['KodiFileId'] = file_id
                self.add_stream_audio(track['KodiFileId'], 1, track['codec'], track['channels'], track['language'])

            for track in streams['subtitle']:
                self.add_stream_sub(file_id, 2, track)


    def add_stream_video(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO streamdetails(idFile, iStreamType, strVideoCodec, fVideoAspect, iVideoWidth, iVideoHeight, iVideoDuration, strStereoMode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", args)

    def add_stacktimes(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO stacktimes(idFile, times) VALUES (?, ?)", args)

    def add_stream_audio(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO streamdetails(idFile, iStreamType, strAudioCodec, iAudioChannels, strAudioLanguage) VALUES (?, ?, ?, ?, ?)", args)

    def add_stream_sub(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO streamdetails(idFile, iStreamType, strSubtitleLanguage) VALUES (?, ?, ?)", args)

    #Delete the existing resume point
    #Set the watched count
    def add_playstate(self, file_id, playcount, date_played, resume, *args):
        self.cursor.execute("DELETE FROM bookmark WHERE idFile = ?", (file_id,))
        self.set_playcount(playcount, date_played, file_id)

        if resume:
            bookmark_id = self.create_entry_bookmark()
            self.cursor.execute("INSERT OR REPLACE INTO bookmark(idBookmark, idFile, timeInSeconds, totalTimeInSeconds, player, type) VALUES (?, ?, ?, ?, ?, ?)", (bookmark_id, file_id, resume,) + args)

    def set_playcount(self, *args):
        self.cursor.execute("UPDATE files SET playCount = ?, lastPlayed = ? WHERE idFile = ?", args)

    def add_tags(self, tags, *args):
        self.cursor.execute("DELETE FROM tag_link WHERE media_id = ? AND media_type = ?", args)

        for tag in tags:
            self.get_tag(tag, *args)

    def add_tag(self, *args):
        tag_id = self.create_entry_tag()
        self.cursor.execute("INSERT OR REPLACE INTO tag(tag_id, name) VALUES (?, ?)", (tag_id,) + args)
        return tag_id

    def get_tag(self, tag, *args):
        self.cursor.execute("SELECT tag_id FROM tag WHERE name = ? COLLATE NOCASE", (tag,))
        Data = self.cursor.fetchone()

        if Data:
            tag_id = Data[0]
        else:
            tag_id = self.add_tag(tag)

        self.cursor.execute("INSERT OR REPLACE INTO tag_link(tag_id, media_id, media_type) VALUES (?, ?, ?)", (tag_id,) + args)
        return tag_id

    def remove_tag(self, tag, *args):
        self.cursor.execute("SELECT tag_id FROM tag WHERE name = ? COLLATE NOCASE", (tag,))
        Data = self.cursor.fetchone()

        if Data:
            tag_id = Data[0]
        else:
            return

        self.cursor.execute("DELETE FROM tag_link WHERE tag_id = ? AND media_id = ? AND media_type = ?", (tag_id,) + args)

    def get_rating_id(self, *args):
        self.cursor.execute("SELECT rating_id FROM rating WHERE media_type = ? AND media_id = ? AND rating_type = ? COLLATE NOCASE", args)
        Data = self.cursor.fetchone()

        if Data:
            return Data[0]

        return self.create_entry_rating()

    #Add ratings, rating type and votes
    def add_ratings(self, *args):
        self.cursor.execute("INSERT OR REPLACE INTO rating(rating_id, media_id, media_type, rating_type, rating, votes) VALUES (?, ?, ?, ?, ?, ?)", args)

    #Update rating by rating_id
    def update_ratings(self, *args):
        self.cursor.execute("UPDATE rating SET media_id = ?, media_type = ?, rating_type = ?, rating = ?, votes = ? WHERE rating_id = ?", args)

    #Remove all unique ids associated.
    def remove_unique_ids(self, *args):
        self.cursor.execute("DELETE FROM uniqueid WHERE media_id = ? AND media_type = ?", args)

    #Add all artworks
    def add_artwork(self, artwork, *args):
        KODI = {
            'Primary': ['thumb', 'poster'],
            'Banner': "banner",
            'Logo': "clearlogo",
            'Art': "clearart",
            'Thumb': "landscape",
            'Disc': "discart",
            'Backdrop': "fanart"
        }

        for art in KODI:
            if art == 'Backdrop':
                num_backdrops = len(artwork['Backdrop'])
                self.cursor.execute("SELECT url FROM art WHERE media_id = ? AND media_type = ? AND type LIKE ?", args + ("fanart%",))

                if len(self.cursor.fetchall()) > num_backdrops:
                    self.cursor.execute("DELETE FROM art WHERE media_id = ? AND media_type = ? AND type LIKE ?", args + ("fanart_",))

                self.update_artwork(*(artwork['Backdrop'][0] if num_backdrops else "",) + args + ("fanart",))

                for index, backdrop in enumerate(artwork['Backdrop'][1:]):
                    self.update_artwork(*(backdrop,) + args + ("%s%s" % ("fanart", index + 1),))
            elif art == 'Primary':
                for kodi_image in KODI['Primary']:
                    self.update_artwork(*(artwork['Primary'],) + args + (kodi_image,))
            else:
                self.update_artwork(*(artwork[art],) + args + (KODI[art],))

    def update_artwork(self, image_url, kodi_id, media, image):
        if image == 'poster' and media in ('song', 'artist', 'album'):
            return

        self.cursor.execute("SELECT url FROM art WHERE media_id = ? AND media_type = ? AND type = ?", (kodi_id, media, image,))
        result = self.cursor.fetchone()

        if result:
            url = result[0]

            if url != image_url:
                if image_url:
#                    self.LOG.info("UPDATE to kodi_id %s art: %s" % (kodi_id, image_url))
                    self.cursor.execute("UPDATE art SET url = ? WHERE media_id = ? AND media_type = ? AND type = ?", (image_url, kodi_id, media, image))
        else:
#            self.LOG.debug("ADD to kodi_id %s art: %s" % (kodi_id, image_url))
            self.cursor.execute("INSERT OR REPLACE INTO art(media_id, media_type, type, url) VALUES (?, ?, ?, ?)", (kodi_id, media, image, image_url))

    #Delete artwork from kodi database and remove cache for backdrop/posters
    def delete_artwork(self, *args):
        self.cursor.execute("SELECT url, type FROM art WHERE media_id = ? AND media_type = ?", args)

        for row in self.cursor.fetchall():
            self.cursor.execute("DELETE FROM art WHERE url = ?", (row[0],))
