from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.images.models import Image
from instagram.donations.models import Donation
from flask_login import login_required, current_user
from instagram import super_admins, generate_client_token, gateway, db, S3_LOCATION
from instagram.helpers import send_donation_email


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates/')


@donations_blueprint.route("/<image_id>/new", methods=["GET"])
@login_required
def create(image_id):
    client_token = generate_client_token()
    return render_template('donations/new.html', image_id=image_id, client_token=client_token)


@donations_blueprint.route("<image_id>/checkout", methods=["POST"])
def checkout(image_id):
    amount = request.form["amount"]
    nonce_from_the_client = request.form["payment_method_nonce"]
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    image_owner_id = Image.query.get(image_id).user_id
    if result.is_success:
        new_donation = Donation(
            current_user.id, image_owner_id, image_id, amount)
        db.session.add(new_donation)
        db.session.commit()
        send_donation_email(current_user.email, amount)
        flash('Donation received successfully.')
        return redirect(url_for('users.profile', id=image_owner_id))
    else:
        flash(result.transaction.status)
        flash(f'{result.transaction.processor_response_code} : {result.transaction.processor_response_text}')
        flash(result.transaction.additional_processor_response)
        return redirect(url_for('users.profile', id=image_owner_id))


@donations_blueprint.route("/", methods=["GET"])
@login_required
def index():
    if current_user.username in super_admins:
        donations = Donation.query.all()
        return render_template('donations/index.html', S3_LOCATION=S3_LOCATION, Image=Image, donations=donations)
    flash('UNAUTHORIZED!!')
    return render_template('users/profile.html', id=current_user.id)
