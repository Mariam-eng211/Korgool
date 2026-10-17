# app.py
from flask import Flask, request, jsonify, render_template, send_file
from datetime import datetime
import sqlite3
from database import (
    init_db, insert_case, get_all_cases, resolve_case, get_stats, lookup_codeword, 
    seed_demo_registry, store_callback_number, get_callback_number, purge_expired_callbacks,
    register_woman, get_all_registered, get_active_case_by_codeword, update_case_repeat
)
from anonymizer import anonymize
from classifier import classify, detect_callback, detect_codeword

app = Flask(__name__)
init_db()
seed_demo_registry()
purge_expired_callbacks()

def process_incoming(raw_message, sender_number=None, source='SMS'):
    raw_message = raw_message.strip()
    if not raw_message: return None

    codeword = detect_codeword(raw_message)
    registry_match = 0
    registry_info = None
    if codeword:
        registry_info = lookup_codeword(codeword)
        if registry_info: registry_match = 1

    callback_requested = 1 if detect_callback(raw_message) else 0
    clean_message = anonymize(raw_message)
    severity, category = classify(clean_message)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if codeword and registry_match:
        active_case_id = get_active_case_by_codeword(codeword)
        if active_case_id:
            update_case_repeat(active_case_id, timestamp)
            return {'status': 'updated', 'case_id': active_case_id, 'severity': severity, 'category': category, 'callback_requested': callback_requested, 'codeword': codeword, 'registry_match': registry_match, 'registry_info': registry_info}

    case_id = insert_case(timestamp, clean_message, severity, category, callback_requested, codeword, registry_match)

    if callback_requested and sender_number:
        store_callback_number(case_id, sender_number, minutes=30)

    return {'status': 'received', 'case_id': case_id, 'severity': severity, 'category': category, 'callback_requested': callback_requested, 'codeword': codeword, 'registry_match': registry_match, 'registry_info': registry_info}

@app.route('/')
def dashboard(): return render_template('dashboard.html')

@app.route('/register')
def register_page(): return render_template('register.html')

@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    data = request.get_json() if request.is_json else request.form
    result = process_incoming(data.get('message') or data.get('Body', ''), data.get('from') or data.get('From'), source='SMS')
    return jsonify(result), 200 if result else 400

@app.route('/api/simulate', methods=['POST'])
def simulate_sms():
    data = request.get_json()
    if not data or 'message' not in data: return jsonify({'error': 'No message'}), 400
    result = process_incoming(data['message'], data.get('from', '+996 555 000 000'), source='SIM')
    return jsonify(result), 200 if result else 400

@app.route('/api/cases', methods=['GET'])
def api_cases():
    return jsonify([{'id': r[0], 'timestamp': r[1], 'message': r[2], 'severity': r[3], 'category': r[4], 'status': r[5], 'callback_requested': r[6], 'codeword': r[7], 'registry_match': r[8]} for r in get_all_cases()])

@app.route('/api/stats', methods=['GET'])
def api_stats(): return jsonify(get_stats())

@app.route('/api/callback/<int:case_id>', methods=['GET'])
def api_callback(case_id):
    phone = get_callback_number(case_id)
    return jsonify({'case_id': case_id, 'phone': phone}) if phone else (jsonify({'error': 'Expired'}), 404)

@app.route('/api/resolve/<int:case_id>', methods=['POST'])
def api_resolve(case_id):
    resolve_case(case_id)
    return jsonify({'status': 'resolved'})

@app.route('/api/purge', methods=['POST'])
def api_purge(): return jsonify({'status': 'purged'})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    try:
        register_woman(data['codeword'].strip(), data['name'].strip(), data.get('address', '').strip(), data.get('disability', '').strip(), data.get('safe_contact', '').strip(), data.get('registered_by', '').strip())
        return jsonify({'status': 'registered'}), 200
    except Exception as e: return jsonify({'error': str(e)}), 400

@app.route('/api/registry', methods=['GET'])
def api_registry(): return jsonify(get_all_registered())

@app.route('/api/registry/lookup', methods=['POST'])
def api_registry_lookup():
    info = lookup_codeword(request.get_json().get('codeword'))
    return jsonify({'codeword': request.get_json().get('codeword'), 'name': info[0], 'address': info[1], 'disability': info[2], 'safe_contact': info[3], 'registered_by': info[4]}) if info else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/backup')
def api_backup(): return send_file('korgool.db', as_attachment=True)

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)