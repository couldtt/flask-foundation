from flask_security import UserMixin, RoleMixin

from app.extensions import db, cache, bcrypt
from app.models.mixin import CURDMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(CURDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False, unique=True)
    nickname = db.Column(db.String(64), server_default='无名氏')
    mobile = db.Column(db.String(128), nullable=True, unique=True)
    pw_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(),
                           server_default=db.func.current_timestamp(), )
    updated_at = db.Column(db.DateTime(),
                           onupdate=db.func.current_timestamp(), )
    remote_addr = db.Column(db.String(20))
    is_active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    list_columns = ['id', 'username', 'nickname', 'mobile', 'created_at', 'updated_at', 'roles']

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password, 10)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    @classmethod
    def stats(cls):
        active_users = cache.get('active_users')
        if not active_users:
            active_users = cls.query.filter_by(is_active=True).count()
            cache.set('active_users', active_users)

        inactive_users = cache.get('inactive_users')
        if not inactive_users:
            inactive_users = cls.query.filter_by(is_active=False).count()
            cache.set('inactive_users', inactive_users)

        return {
            'all': active_users + inactive_users,
            'active': active_users,
            'inactive': inactive_users
        }


class Role(CURDMixin, RoleMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
