from flask import jsonify

def message_response(status, message):
    return jsonify({
        "success": status,
        "message": message
    })