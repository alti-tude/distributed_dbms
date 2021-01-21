INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (3, "Mumbai", 1),
        (4, "Mumbai", 1);

INSERT INTO Screen (ScreenID, TheaterID, ScreenName, NumSeats)
VALUES  (3, 3, "MumbaiScreen1", 4),
        (4, 4, "MumbaiScreen2", 4);

INSERT INTO Screening (ShowID, MovieID, ScreenID, Time, Price)
VALUE   (9, 1, 3, '2015-11-05 14:29:38',100.35),
        (10, 1, 4, '2015-11-05 14:29:39',100.35),
        (11, 2, 3, '2015-11-05 14:29:35',100.35),
        (12, 2, 4, '2015-11-05 14:29:41',100.35);

INSERT INTO Movie (MovieID, Summary, MinAllowedAge)
VALUES  (1, "Movie 1 random summary", 10),
        (2, "Movie 2 random summary", 18);
