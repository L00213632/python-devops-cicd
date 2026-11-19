

from flask import Blueprint, jsonify, render_template
from datetime import datetime, timezone

main = Blueprint("main", __name__)

START_TIME = datetime.now(timezone.utc)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Python DevOps application is running",
        "application": "DevOps Control Centre",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@main.route("/api/dashboard")
def dashboard():
    uptime = datetime.now(timezone.utc) - START_TIME

    return jsonify({
        "status": "healthy",
        "uptime_seconds": int(uptime.total_seconds()),
        "application": "Python DevOps Control Centre",
        "pipeline": [
            "GitHub",
            "Jenkins",
            "Testing",
            "Docker",
            "Deployment",
            "Monitoring"
        ]
    }), 200
