from CDS import app, db
from CDS.models import User, CancerType, UserCancerMapping, CancerImageBase, LungCancerImage, SkinCancerImage, BrainCancerImage, Prediction, ChatbotQuestion

with app.app_context():
    user = User.query.first()
    print(user)
    print(user.password)