from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram import super_admins, current_user, db
from instagram.followings.models import Users_Users
from instagram.users.models import User


followings_blueprint = Blueprint(
    'followings', __name__, template_folder='templates/')


@followings_blueprint.route("<follower>/<following>/follow")
def follow(follower, following):
    if current_user.username in super_admins or int(follower) == current_user.id:
        new_follow = Users_Users(follower, following)
        db.session.add(new_follow)
        db.session.commit()
        print(new_follow)
        flash(f'You are now following {User.query.get(following).username}')
        # send_follow_email(new_user.email) You have a new follower!
        return redirect(url_for('users.profile', id=following))
    else:
        flash('UNAUTHORIZED!!')
        return redirect(url_for('users.profile', id=current_user.id))


@followings_blueprint.route("<unfollower>/<unfollowing>/unfollow")
def unfollow(unfollower, unfollowing):
    if current_user.username in super_admins or int(unfollower) == current_user.id:
        unfollow = Users_Users.query.filter_by(
            follower_id=unfollower, followed_id=unfollowing).first()
        db.session.delete(unfollow)
        db.session.commit()
        flash(f'You have unfollowed {User.query.get(unfollowing).username}')
        # send_follow_email(new_user.email) You have a new follower!
        return redirect(url_for('users.profile', id=unfollowing))
    else:
        flash('UNAUTHORIZED!!')
        return redirect(url_for('users.profile', id=current_user.id))
