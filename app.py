from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('rentals.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            [group] TEXT,
            sender_id INTEGER,
            username TEXT,
            message TEXT,
            country TEXT,
            city TEXT,
            Area TEXT,
            rent_type TEXT,
            price REAL,
            ISO_4217 TEXT,
            available_date TEXT,
            rooms_number INTEGER,
            property_type TEXT,
            house_rules TEXT,
            contact_information TEXT,
            rental_duration TEXT,
            roommate_gender TEXT,
            house_furniture TEXT,
            pets_allowed TEXT,
            smoking_allowed TEXT,
            Image_URL TEXT,
            created_post TEXT,
            Title TEXT,
            website_reference TEXT  -- Added new column
        )
    ''')
    # Create indexes for better query performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_country ON ads (country)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_city ON ads (city)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_created_post ON ads (created_post)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_sender_id ON ads (sender_id)')
    conn.commit()
    conn.close()

init_db()

# Route for the Mini App entry point
@app.route('/')
def index():
    # redirect user to external HTML
    return redirect("https://machino24bot.onrender.com/templates/Index.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    # redirect static file requests to external host
    return redirect(f"https://machino24bot.onrender.com/static/{filename}")

# API to get cities for a country
@app.route('/api/get_cities', methods=['GET'])
def get_cities():
    country = request.args.get('country')
    if not country:
        return jsonify([]), 400
    conn = sqlite3.connect('rentals.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT city FROM ads WHERE country = ? AND city IS NOT NULL', (country,))
    cities = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(cities)

# API to post a new ad
@app.route('/api/post_ad', methods=['POST'])
def post_ad():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    message = data.get('message')
    country = data.get('country')
    city = data.get('city')
    Area = data.get('Area')
    rent_type = data.get('rent_type')
    price = data.get('price')
    ISO_4217 = data.get('ISO_4217')
    available_date = data.get('available_date')
    rooms_number = data.get('rooms_number')
    property_type = data.get('property_type')
    house_rules = data.get('house_rules')
    contact_information = data.get('contact_information')
    rental_duration = data.get('rental_duration')
    roommate_gender = data.get('roommate_gender')
    house_furniture = data.get('house_furniture')
    pets_allowed = data.get('pets_allowed')
    smoking_allowed = data.get('smoking_allowed')
    Image_URL = data.get('Image_URL')
    Title = data.get('Title')
    website_reference = data.get('website_reference')  # Added new field
    created_post = datetime.now().isoformat()

    if not user_id:
        return jsonify({'error': 'Missing required field: user_id'}), 400

    sender_id = user_id
    group = ''

    conn = sqlite3.connect('rentals.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO ads (
            [group], sender_id, username, message, country, city, Area, rent_type,
            price, ISO_4217, available_date, rooms_number, property_type, house_rules,
            contact_information, rental_duration, roommate_gender, house_furniture,
            pets_allowed, smoking_allowed, Image_URL, created_post, Title, website_reference
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        group, sender_id, username, message, country, city, Area, rent_type,
        price, ISO_4217, available_date, rooms_number, property_type, house_rules,
        contact_information, rental_duration, roommate_gender, house_furniture,
        pets_allowed, smoking_allowed, Image_URL, created_post, Title, website_reference
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# API to get ads with filters and pagination
@app.route('/api/get_ads', methods=['GET'])
def get_ads():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))
    offset = (page - 1) * per_page
    country = request.args.get('country')
    city = request.args.get('city')
    Area = request.args.get('Area')
    rent_type = request.args.get('rent_type')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    ISO_4217 = request.args.get('ISO_4217')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    rental_duration = request.args.get('rental_duration')
    roommate_gender = request.args.get('roommate_gender')
    pets_allowed = request.args.get('pets_allowed')
    smoking_allowed = request.args.get('smoking_allowed')

    conn = sqlite3.connect('rentals.db')
    c = conn.cursor()
    
    count_query = 'SELECT COUNT(*) FROM ads WHERE 1=1'
    count_params = []
    query = 'SELECT * FROM ads WHERE 1=1'
    params = []
    
    if country:
        query += ' AND country LIKE ?'
        count_query += ' AND country LIKE ?'
        params.append(f'%{country}%')
        count_params.append(f'%{country}%')
    if city:
        query += ' AND city LIKE ?'
        count_query += ' AND city LIKE ?'
        params.append(f'%{city}%')
        count_params.append(f'%{city}%')
    if Area:
        query += ' AND Area LIKE ?'
        count_query += ' AND Area LIKE ?'
        params.append(f'%{Area}%')
        count_params.append(f'%{Area}%')
    if rent_type:
        query += ' AND rent_type = ?'
        count_query += ' AND rent_type = ?'
        params.append(rent_type)
        count_params.append(rent_type)
    if min_price:
        query += ' AND price >= ?'
        count_query += ' AND price >= ?'
        params.append(float(min_price))
        count_params.append(float(min_price))
    if max_price:
        query += ' AND price <= ?'
        count_query += ' AND price <= ?'
        params.append(float(max_price))
        count_params.append(float(max_price))
    if ISO_4217:
        query += ' AND ISO_4217 = ?'
        count_query += ' AND ISO_4217 = ?'
        params.append(ISO_4217)
        count_params.append(ISO_4217)
    if min_rooms:
        query += ' AND rooms_number >= ?'
        count_query += ' AND rooms_number >= ?'
        params.append(int(min_rooms))
        count_params.append(int(min_rooms))
    if max_rooms:
        query += ' AND rooms_number <= ?'
        count_query += ' AND rooms_number <= ?'
        params.append(int(max_rooms))
        count_params.append(int(max_rooms))
    if rental_duration:
        query += ' AND rental_duration = ?'
        count_query += ' AND rental_duration = ?'
        params.append(rental_duration)
        count_params.append(rental_duration)
    if roommate_gender:
        query += ' AND roommate_gender = ?'
        count_query += ' AND roommate_gender = ?'
        params.append(roommate_gender)
        count_params.append(roommate_gender)
    if pets_allowed:
        query += ' AND pets_allowed = ?'
        count_query += ' AND pets_allowed = ?'
        params.append(pets_allowed)
        count_params.append(pets_allowed)
    if smoking_allowed:
        query += ' AND smoking_allowed = ?'
        count_query += ' AND smoking_allowed = ?'
        params.append(smoking_allowed)
        count_params.append(smoking_allowed)
    
    query += ' ORDER BY created_post DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    
    c.execute(count_query, count_params)
    total_ads = c.fetchone()[0]
    
    c.execute(query, params)
    ads = c.fetchall()
    conn.close()
    
    return jsonify({
        'ads': [{
            'group': ad[0],
            'sender_id': ad[1],
            'username': ad[2],
            'message': ad[3],
            'country': ad[4],
            'city': ad[5],
            'Area': ad[6],
            'rent_type': ad[7],
            'price': ad[8],
            'ISO_4217': ad[9],
            'available_date': ad[10],
            'rooms_number': ad[11],
            'property_type': ad[12],
            'house_rules': ad[13],
            'contact_information': ad[14],
            'rental_duration': ad[15],
            'roommate_gender': ad[16],
            'house_furniture': ad[17],
            'pets_allowed': ad[18],
            'smoking_allowed': ad[19],
            'Image_URL': ad[20],
            'created_post': ad[21],
            'Title': ad[22],
            'website_reference': ad[23] 
        } for ad in ads],
        'total': total_ads
    })

# API to delete an ad (only by owner)
@app.route('/api/delete_ad', methods=['POST'])
def delete_ad():
    data = request.json
    created_post = data.get('created_post')
    sender_id = data.get('sender_id')

    if not created_post or not sender_id:
        return jsonify({'error': 'Missing required fields: created_post, sender_id'}), 400

    conn = sqlite3.connect('rentals.db')
    c = conn.cursor()
    c.execute('DELETE FROM ads WHERE created_post = ? AND sender_id = ?', (created_post, sender_id))
    affected_rows = c.rowcount
    conn.commit()
    conn.close()
    return jsonify({'success': affected_rows > 0})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # پیش‌فرض 5000 برای تست محلی
    app.run(host='0.0.0.0', port=port, debug=True)