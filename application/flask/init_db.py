from database import db, User


try:
    # creates the database
    db.create_all()

    # creates 2 users
    db.session.add(User(username='toto', email='toto@example.com'))
    db.session.add(User(username='titi', email='titi@example.com'))

    db.session.commit()
except Exception as e:
    pass
