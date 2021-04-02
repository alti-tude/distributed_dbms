INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (5, "Delhi", 1),
        (6, "Delhi", 1);

INSERT INTO Screen (ScreenID, TheaterID, ScreenName, NumSeats)
VALUES  (5, 5, "DelhiScreen1", 4),
        (6, 6, "DelhiScreen2", 4);

INSERT INTO Screening (ShowID, MovieID, ScreenID, Time, Price)
VALUE   (5, 1, 5, '2015-11-05 14:29:31',100.35),
        (6, 1, 6, '2015-11-05 14:29:32',100.35),
        (7, 2, 5, '2015-11-05 14:29:42',100.35),
        (8, 2, 6, '2015-11-05 14:29:43',100.35);

INSERT INTO User (EMail, Name, PhNo, DOB)
VALUE   ("user1", "username1", "+91111111", "2020-12-1"),
        ("user2", "username2", "+91222222", "2020-12-2");
