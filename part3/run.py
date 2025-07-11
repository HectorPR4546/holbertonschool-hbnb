from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@hbnb.io').first():
        admin = User(first_name='Admin', last_name='User', email='admin@hbnb.io', password='admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
