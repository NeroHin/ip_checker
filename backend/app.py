from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='../frontend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class IPRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/ip', methods=['GET'])
def get_ip():
    client_ip = request.remote_addr
    new_ip = IPRecord(ip_address=client_ip)
    db.session.add(new_ip)
    db.session.commit()
    return jsonify(new_ip.to_dict())

@app.route('/api/history', methods=['GET'])
def history():
    ips = IPRecord.query.order_by(IPRecord.id.desc()).all()
    return jsonify([ip.to_dict() for ip in ips])

@app.route('/api/clear', methods=['POST'])
def clear_history():
    try:
        db.session.query(IPRecord).delete()
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'All records have been deleted.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)