INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (3, "Mumbai", 1),
        (4, "Mumbai", 1),
        (10, "Mumbai", 4),
        (11, "Mumbai", 6),
        (12, "Mumbai", 8),
        (13, "Mumbai", 3);

INSERT INTO Showing (ShowID, MovieID, TheaterID, Time, Price)
VALUE   (9, 1, 3, '2015-11-05 14:29:38',100.35),
        (10, 1, 4, '2015-11-05 14:29:39',100.35),
        (11, 2, 10, '2015-11-05 14:29:35',100.35),
        (12, 2, 13, '2015-11-05 14:29:41',100.35);

INSERT INTO Movie (MovieID, Summary, MinAllowedAge)
VALUES  (1, "Movie 1 random summary", 10),
        (2, "Movie 2 random summary", 18),
        (3, "Movie3 random summary", 12),
        (4, "Movie4 random summary", 12),
        (5, "Movie5 random summary", 18),
        (6, "Movie6 random summary", 3),
        (7, "Movie7 random summary", 12),
        (8, "Movie8 random summary", 15),
        (9, "Movie9 random summary", 3),
        (10, "Movie10 random summary", 18),
        (11, "Movie11 random summary", 15),
        (12, "Movie12 random summary", 12),
        (13, "Movie13 random summary", 13);
