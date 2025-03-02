import sys
sys.path.append('F:/Studying/GP Demo')

from CDS import db, app  

with app.app_context():
    db.create_all()

print("✅ Database tables created successfully!")
