INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (1, "Hyderabad", 1),
        (2, "Hyderabad", 1);

INSERT INTO Screen (ScreenID, TheaterID, ScreenName, NumSeats)
VALUES  (1, 1, "HyderabadScreen1", 4),
        (2, 2, "HyderabadScreen2", 4);

INSERT INTO Movie (MovieID, Name, Genre, IMDBRating)
VALUES  (1, "Movie1", "Action", 7.3),
        (2, "Movie2", "Comedy", 9.9);

INSERT INTO Screening (ShowID, MovieID, ScreenID, Time, Price)
VALUE   (1, 1, 1, '2015-11-05 14:29:36',100.5),
        (2, 1, 2, '2015-11-05 14:29:37',100.25),
        (3, 2, 1, '2015-11-05 14:29:33',100.35),
        (4, 2, 2, '2015-11-05 14:29:34',100.35);

INSERT INTO Reservation (ShowID, UserEMail, SeatNo)
VALUE   (1, "user1", 1),
        (1, "user2", 2),
        (2, "user1", 1),
        (2, "user2", 2),
        (3, "user1", 1),
        (3, "user2", 2),
        (4, "user1", 1),
        (4, "user2", 2),
        (5, "user1", 1),
        (5, "user2", 2),
        (6, "user1", 1),
        (6, "user2", 2),
        (7, "user1", 1),
        (7, "user2", 2),
        (8, "user1", 1),
        (8, "user2", 2),
        (9, "user1", 1),
        (9, "user2", 2),
        (10, "user1", 1),
        (10, "user2", 2),
        (11, "user1", 1),
        (11, "user2", 2),
        (12, "user1", 1),
        (12, "user2", 2);

