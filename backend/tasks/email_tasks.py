from celery_app import celery_app
from flask import Flask
from flask_mail import Mail, Message
from models.user import User
from models.reservation import Reservation
from models.parking_spot import ParkingSpot
from models.parking_lot import ParkingLot
from models import db
import csv
from io import StringIO
from datetime import datetime, timedelta
from config import (
    DATABASE_URL, 
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS,
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
)

def create_app():
    """Create Flask app for Celery tasks"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
    
    # Initialize extensions
    db.init_app(app)
    mail = Mail(app)
    
    return app, mail

@celery_app.task
def send_reminder_email(to_email, full_name):
    """Send a simple reminder email to a user"""
    app, mail = create_app()
    
    with app.app_context():
        msg = Message(
            subject="🚗 Parking Reminder",
            recipients=[to_email],
            body=f"Hi {full_name},\n\nYou have an active parking reservation. Please don't forget to check out if you're done!\n\nBest regards,\nParking Management System"
        )
        mail.send(msg)
        print(f"✅ Reminder email sent to {to_email}")
        return f"Email sent to {to_email}"

@celery_app.task
def send_daily_reminders():
    """Send daily reminders to users with active reservations"""
    app, mail = create_app()
    
    with app.app_context():
        # Find users with active reservations (using leaving_timestamp = None for active)
        active_reservations = Reservation.query.filter(
            Reservation.leaving_timestamp.is_(None)  # Active reservations
        ).all()
        
        sent_count = 0
        for reservation in active_reservations:
            user = User.query.get(reservation.user_id)
            if user and user.email:
                send_reminder_email.delay(user.email, user.full_name)
                sent_count += 1
        
        print(f"✅ Daily reminders initiated for {sent_count} users")
        return f"Sent reminders to {sent_count} users"

@celery_app.task
def send_monthly_reports():
    """Send monthly activity reports to all users"""
    app, mail = create_app()
    
    with app.app_context():
        # Get all users
        users = User.query.all()
        
        # Calculate date range for last month
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        sent_count = 0
        for user in users:
            if user.email and user.role == 'user':  # Only send to regular users, not admins
                # Get user's reservations from last month
                reservations = Reservation.query.filter(
                    Reservation.user_id == user.id,
                    Reservation.parking_timestamp >= first_day_last_month,
                    Reservation.parking_timestamp <= last_day_last_month
                ).all()
                
                # Generate report
                generate_monthly_report.delay(user.id, user.email, user.full_name, len(reservations))
                sent_count += 1
        
        print(f"✅ Monthly reports initiated for {sent_count} users")
        return f"Sent monthly reports to {sent_count} users"

@celery_app.task
def generate_monthly_report(user_id, email, full_name, reservation_count):
    """Generate and send monthly report for a specific user"""
    app, mail = create_app()
    
    with app.app_context():
        # Calculate date range for last month
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        month_name = last_day_last_month.strftime("%B %Y")
        
        # Get detailed reservations for the user
        reservations = Reservation.query.filter(
            Reservation.user_id == user_id,
            Reservation.parking_timestamp >= first_day_this_month.replace(month=first_day_this_month.month-1),
            Reservation.parking_timestamp <= last_day_last_month
        ).all()
        
        # Generate HTML report
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; text-align: center; }}
                .summary {{ background-color: #e8f4fd; padding: 15px; margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚗 Monthly Parking Report</h1>
                <h2>{month_name}</h2>
            </div>
            
            <p>Dear {full_name},</p>
            
            <div class="summary">
                <h3>📊 Summary</h3>
                <p><strong>Total Reservations:</strong> {len(reservations)}</p>
                <p><strong>Report Period:</strong> {month_name}</p>
            </div>
            
            <h3>📋 Reservation Details</h3>
        """
        
        if reservations:
            html_content += """
            <table>
                <tr>
                    <th>Date</th>
                    <th>Location</th>
                    <th>Spot</th>
                    <th>Vehicle</th>
                    <th>Check-in</th>
                    <th>Check-out</th>
                </tr>
            """
            
            for reservation in reservations:
                spot = ParkingSpot.query.get(reservation.spot_id)
                lot = ParkingLot.query.get(spot.lot_id) if spot else None
                
                # Use leaving_timestamp instead of checkout_timestamp
                checkout_time = reservation.leaving_timestamp.strftime("%H:%M") if reservation.leaving_timestamp else "Active"
                
                # Use spot ID since there's no spot_number in your model
                spot_identifier = f"Spot {spot.id}" if spot else 'N/A'
                
                html_content += f"""
                <tr>
                    <td>{reservation.parking_timestamp.strftime("%Y-%m-%d")}</td>
                    <td>{lot.location if lot else 'N/A'}</td>
                    <td>{spot_identifier}</td>
                    <td>{reservation.vehicle_number}</td>
                    <td>{reservation.parking_timestamp.strftime("%H:%M")}</td>
                    <td>{checkout_time}</td>
                </tr>
                """
            
            html_content += "</table>"
        else:
            html_content += "<p>No reservations found for this period.</p>"
        
        html_content += """
            <br>
            <p>Thank you for using our parking system!</p>
            <p>Best regards,<br>Parking Management Team</p>
        </body>
        </html>
        """
        
        # Send email with HTML report
        msg = Message(
            subject=f"📊 Monthly Parking Report - {month_name}",
            recipients=[email],
            html=html_content
        )
        
        mail.send(msg)
        print(f"✅ Monthly report sent to {email}")
        return f"Monthly report sent to {email}"

@celery_app.task
def export_csv_email(user_id, email):
    """Generate and email CSV export of user's parking history"""
    app, mail = create_app()
    
    with app.app_context():
        # Query reservation history
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        
        # Generate CSV in-memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Location', 'Spot Number', 'Check-in Date', 'Check-in Time', 'Check-out Time', 'Vehicle Number'])
        
        for reservation in reservations:
            spot = ParkingSpot.query.get(reservation.spot_id)
            lot = ParkingLot.query.get(spot.lot_id) if spot else None
            
            # Use leaving_timestamp instead of checkout_timestamp
            checkout_time = reservation.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if reservation.leaving_timestamp else "Still Active"
            
            # Use spot ID since there's no spot_number in your model
            spot_identifier = f"Spot {spot.id}" if spot else 'N/A'
            
            writer.writerow([
                reservation.id,
                lot.location if lot else 'N/A',
                spot_identifier,
                reservation.parking_timestamp.strftime("%Y-%m-%d"),
                reservation.parking_timestamp.strftime("%H:%M:%S"),
                checkout_time,
                reservation.vehicle_number
            ])
        
        # Reset string buffer position
        output.seek(0)
        
        # Create email with CSV attachment
        msg = Message(
            subject="📊 Your Parking History CSV Export",
            recipients=[email],
            body="Hello!\n\nAttached is your complete parking reservation history in CSV format.\n\nBest regards,\nParking Management System"
        )
        
        msg.attach("parking_history.csv", "text/csv", output.read())
        mail.send(msg)
        
        print(f"✅ CSV export sent to {email}")
        return f"CSV export sent to {email}"