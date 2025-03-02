from datetime import datetime
from CDS import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    cancers = db.relationship('UserCancerMapping', back_populates='user', cascade='all, delete-orphan')
    lung_images = db.relationship('LungCancerImage', back_populates='user', cascade='all, delete-orphan')
    skin_images = db.relationship('SkinCancerImage', back_populates='user', cascade='all, delete-orphan')
    brain_images = db.relationship('BrainCancerImage', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}')"


class CancerType(db.Model):
    __tablename__ = 'cancer_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    users = db.relationship('UserCancerMapping', back_populates='cancer_type', cascade='all, delete-orphan')
    lung_images = db.relationship('LungCancerImage', back_populates='cancer_type', cascade='all, delete-orphan')
    skin_images = db.relationship('SkinCancerImage', back_populates='cancer_type', cascade='all, delete-orphan')
    brain_images = db.relationship('BrainCancerImage', back_populates='cancer_type', cascade='all, delete-orphan')
    questions = db.relationship('ChatbotQuestion', back_populates='cancer_type', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"CancerType('{self.name}')"


class UserCancerMapping(db.Model):
    __tablename__ = 'user_cancer_mapping'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cancer_type_id = db.Column(db.Integer, db.ForeignKey('cancer_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='cancers')
    cancer_type = db.relationship('CancerType', back_populates='users')
    
    def __repr__(self):
        return f"UserCancerMapping(User ID: {self.user_id}, CancerType ID: {self.cancer_type_id})"


class CancerImageBase:
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cancer_type_id = db.Column(db.Integer, db.ForeignKey('cancer_types.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class LungCancerImage(db.Model, CancerImageBase):
    __tablename__ = 'lung_cancer_images'
    
    user = db.relationship('User', back_populates='lung_images')
    cancer_type = db.relationship('CancerType', back_populates='lung_images')
    
    def __repr__(self):
        return f"LungCancerImage(User ID: {self.user_id}, Path: {self.image_path}, Prediction: {self.prediction_result})"


class SkinCancerImage(db.Model, CancerImageBase):
    __tablename__ = 'skin_cancer_images'
    
    user = db.relationship('User', back_populates='skin_images')
    cancer_type = db.relationship('CancerType', back_populates='skin_images')
    
    def __repr__(self):
        return f"SkinCancerImage(User ID: {self.user_id}, Path: {self.image_path}, Prediction: {self.prediction_result})"


class BrainCancerImage(db.Model, CancerImageBase):
    __tablename__ = 'brain_cancer_images'
    
    user = db.relationship('User', back_populates='brain_images')
    cancer_type = db.relationship('CancerType', back_populates='brain_images')
    
    def __repr__(self):
        return f"BrainCancerImage(User ID: {self.user_id}, Path: {self.image_path}, Prediction: {self.prediction_result})"


class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.String(50), nullable=False)  # Malignant / Benign
    confidence = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Prediction(Image ID: {self.image_id}, Prediction: {self.prediction}, Confidence: {self.confidence})"


class ChatbotQuestion(db.Model):
    __tablename__ = 'chatbot_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    cancer_type_id = db.Column(db.Integer, db.ForeignKey('cancer_types.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    
    cancer_type = db.relationship('CancerType', back_populates='questions')
    
    def __repr__(self):
        return f"ChatbotQuestion(CancerType ID: {self.cancer_type_id}, Question: {self.question})"