from . import db


class User(db.Model):
    __tablename__ = 'front_stage_user_data'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_first_name = db.Column(db.String(20))
    user_last_name = db.Column(db.String(20))
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_phone = db.Column(db.String(11))
    user_address = db.Column(db.String(50))
    user_enable_status = db.Column(db.Boolean)
    user_signup_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_last_change_code_time = db.Column(db.DateTime)
    user_mobile_bar_code = db.Column(db.String(20))
    user_password = db.Column(db.String(255), nullable=False)  # Removed validate from here



    def __repr__(self):
        return f'<User {self.user_id} {self.user_email}>'
