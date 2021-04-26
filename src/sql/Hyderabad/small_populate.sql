INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (1, "Hyderabad", 1),
        (2, "Hyderabad", 1),
        (7, "Hyderabad", 6),
        (8, "Hyderabad", 3),
        (9, "Hyderabad", 5);

INSERT INTO Movie (MovieID, Name, Genre, IMDBRating)
VALUES  (1, "Movie1", "Action", 7.3),
        (2, "Movie2", "Comedy", 9.9),
        (3, "Movie3", "Thriller", 5),
        (4, "Movie4", "Horror", 6.5),
        (5, "Movie5", "Action", 2.3),
        (6, "Movie6", "Thriller", 8.2),
        (7, "Movie7", "Action", 4.5),
        (8, "Movie8", "Comedy", 8.0),
        (9, "Movie9", "Comedy", 6.3),
        (10, "Movie10", "Horror", 7.6),
        (11, "Movie11", "Thriller", 4.8),
        (12, "Movie12", "Action", 6.8),
        (13, "Movie13", "Comedy", 8.9);

INSERT INTO Showing (ShowID, MovieID, TheaterID, Time, Price)
VALUE   (1, 1, 1, '2015-11-05 14:29:36',100.5),
        (2, 1, 2, '2015-11-05 14:29:37',100.25),
        (3, 2, 1, '2015-11-05 14:29:33',100.35),
        (4, 2, 2, '2015-11-05 14:29:34',100.35),
        (13, 10, 8, '2010-11-05 14:29:34',120.35),
        (14, 4, 9, '2010-12-07 17:29:34',99.35),
        (15, 8, 7, '2010-05-04 19:30:34',50.5),
        (16, 11, 7, '2020-03-01 13:30:34',55.5);

INSERT INTO Reservation (ShowID, UserEMail, SeatNo)
VALUE   (1, "user1", 1),
        (1, "user2", 3),
        (2, "user1", 5),
        (2, "user2", 2),
        (3, "user1", 1),
        (3, "user2", 25),
        (4, "user1", 1),
        (4, "user2", 2),
        (5, "user1", 1),
        (5, "user2", 4),
        (6, "user1", 1),
        (6, "user2", 2),
        (7, "user1", 7),
        (7, "user2", 8),
        (8, "user1", 18),
        (8, "user3", 22),
        (9, "user1", 31),
        (9, "user2", 2),
        (10, "user1", 1),
        (10, "user2", 2),
        (11, "user1", 41),
        (11, "user2", 20),
        (12, "user1", 1),
        (12, "user2", 2),
        (13, "user2", 2);