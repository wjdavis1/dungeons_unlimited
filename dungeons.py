from app import create_app, db
from app.models.auth.user import User, Campaigns

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User,'Campaigns':Campaigns}
