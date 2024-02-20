from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, TravelAgent
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Handle search functionality
        location = request.form.get('location')
        posts = Post.query.filter(Post.location.ilike(f"%{location}%")).all()
    else:
        # Retrieve all posts from the database
        posts = Post.query.all()

    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        location = request.form.get('location') 

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, location=location, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

@views.route("/plan")
@login_required
def planner():
    return render_template("planner.html", user=current_user)

@views.route("/travel",  methods=["GET", "POST"])
@login_required
def travel():
    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")
        location = request.form.get("location")

        # Create TravelAgent instance and add to the database
        new_agent = TravelAgent(name=name, contact=contact, location=location)
        db.session.add(new_agent)
        db.session.commit()

        flash("Travel Agent added successfully!", category="success")
        return redirect(url_for("views.travel"))
    return render_template("travel.html", user=current_user)

@views.route("/travel-agents", methods=['GET', 'POST'])
@login_required
def travel_agents():
    if request.method == 'POST':
        # Handle search functionality
        location = request.form.get('location')
        agents = TravelAgent.query.filter(TravelAgent.location.ilike(f"%{location}%")).all()
    else:
        # Retrieve all travel agents from the database
        agents = TravelAgent.query.all()

    return render_template("travel_agents.html", user=current_user, agents=agents)


@views.route("/places", methods=['GET', 'POST'])
@login_required
def places():
    return render_template("places.html", user=current_user)

