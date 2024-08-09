from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from models import db, Campaign, Link, Click, Conversion
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpa_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
Bootstrap(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    campaigns = Campaign.query.all()
    return render_template('index.html', campaigns=campaigns)

@app.route('/campaign/new', methods=['GET', 'POST'])
def new_campaign():
    if request.method == 'POST':
        name = request.form.get('name')
        campaign = Campaign(name=name)
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!')
        return redirect(url_for('index'))
    return render_template('new_campaign.html')

@app.route('/campaign/<int:campaign_id>/link/new', methods=['GET', 'POST'])
def new_link(campaign_id):
    if request.method == 'POST':
        url = request.form.get('url')
        link = Link(campaign_id=campaign_id, url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link created successfully!')
        return redirect(url_for('index'))
    return render_template('new_link.html', campaign_id=campaign_id)

@app.route('/click/<int:link_id>', methods=['GET'])
def track_click(link_id):
    ip_address = request.remote_addr
    click = Click(link_id=link_id, timestamp=datetime.utcnow(), ip_address=ip_address)
    db.session.add(click)
    db.session.commit()
    return redirect(Link.query.get(link_id).url)

@app.route('/postback', methods=['GET', 'POST'])
def track_conversion():
    click_id = request.args.get('click_id')
    revenue = request.args.get('revenue')
    conversion = Conversion(click_id=click_id, timestamp=datetime.utcnow(), revenue=revenue)
    db.session.add(conversion)
    db.session.commit()
    return "Conversion recorded", 200

if __name__ == '__main__':
    app.run(debug=True)
