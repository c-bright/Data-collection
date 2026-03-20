UPDATE `user`
SET `password` = %s,
    email = %s
WHERE username = %s;
