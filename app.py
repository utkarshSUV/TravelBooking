from flask import Flask, request, jsonify, abort, render_template
from models import db
import services

app = Flask(__name__)

# Configure the database connection
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_VKbztk8GN2Je@ep-super-mode-a4emkx94.us-east-1.aws.neon.tech:5432/neondb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to book an item
@app.route("/book", methods=["POST"])
def book():
    request_data = request.get_json()
    member_id = request_data.get("member_id")
    inventory_id = request_data.get("inventory_id")

    result = services.book_item(db.session, member_id, inventory_id)
    if "error" in result:
        return jsonify(result), 400
    elif "SQLAlchemy_Error" in result:
        return jsonify(result), 500
    elif "unexpected_error" in result:
        return jsonify(result), 500
    return jsonify(result)


# Endpoint to cancel a booking
@app.route("/cancel/<int:booking_id>", methods=["DELETE"])
def cancel(booking_id):
    result = services.cancel_booking(db.session, booking_id)
    if "error" in result:
        return jsonify(result), 400
    elif "SQLAlchemy_Error" in result:
        return jsonify(result), 500
    elif "unexpected_error" in result:
        return jsonify(result), 500

    return jsonify(result)


# Endpoint to upload members CSV
@app.route("/upload/members", methods=["POST"])
def upload_members():
    if 'file' not in request.files:
        abort(400, description="No file part")

    file = request.files['file']
    file_content = file.read()

    result = services.upload_members(file_content, db.session)

    if "error" in result:
        return jsonify(result), 400
    elif "SQLAlchemy_Error" in result:
        return jsonify(result), 500

    return jsonify(result)


# Endpoint to upload inventory CSV
@app.route("/upload/inventory", methods=["POST"])
def upload_inventory():
    if 'file' not in request.files:
        abort(400, description="No file part")

    file = request.files['file']
    file_content = file.read()

    result = services.upload_inventory(file_content, db.session)

    if "error" in result:
        return jsonify(result), 400
    elif "SQLAlchemy_Error" in result:
        return jsonify(result), 500

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

