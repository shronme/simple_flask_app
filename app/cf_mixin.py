from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CFMixin(object):

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def refresh(self):
        db.session.expire(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def populate(self, values):
        for key, value in values.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
