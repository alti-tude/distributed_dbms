INSERT INTO Theater (TheaterID, Location, NumScreens)
VALUES  (5, "Delhi", 1),
        (6, "Delhi", 1);

INSERT INTO Showing (ShowID, MovieID, TheaterID, Time, Price)
VALUE   (5, 1, 5, '2015-11-05 14:29:31',100.35),
        (6, 8, 6, '2015-11-05 14:29:32',100.35),
        (7, 12, 5, '2015-11-05 14:29:42',100.35),
        (8, 9, 6, '2015-11-05 14:29:43',100.35);

INSERT INTO User (EMail, Name, PhNo, DOB)
VALUE   ("user1", "username1", "+91111111", "2020-12-1"),
        ("user2", "username2", "+91222222", "2020-12-2"),
        ("user3", "username3", "+91422222", "2020-10-2");
