CREATE INDEX playlist_created IF NOT EXISTS FOR (p:Playlist) ON (p.createdAt);
