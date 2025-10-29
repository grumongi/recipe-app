print("Hello World!")

In [1]: import bcrypt # type: ignore
In [2]: password = b"A super complicated password"
In [3]: hashed = bcrypt.hashpw(password, bcrypt.gensalt())
In [4]: print(hashed)

