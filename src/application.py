import reddit_api_handle
from flask import Flask
from flask import render_template
from flask import request
from random import randint
import requests
from flask import Blueprint
import os

rh = reddit_api_handle.RedditApiHandle('cCVvYBslK27M_A',
                                       'Utx0lA24OaKWbvUUfKjAow8e9BQ')
app = Flask(__name__)
rand=randint(100, 999)

blueprint = Blueprint('tempdl', __name__, static_url_path='/static/tempdl', static_folder='static/tempdl')
app.register_blueprint(blueprint)

@app.route('/')
def view_frontpage():
    page = {
        'title': 'front page',
        'path': '/',
        'limit': '10'
    }
    
    post_list = rh.get_posts_hot(page['path'], page['limit'])
    
    return render_template('view_posts.html',
                           page=page,
                           posts=post_list.posts)


@app.route('/r/<subreddit>')
def view_subreddit(subreddit):
    page = {
        'title': subreddit,
        'path': '/r/' + subreddit + '/',
    }
    post_list = rh.get_posts_hot(page['path'], 10)
    return render_template('view_posts.html',
                           page=page,
                           posts=post_list.posts)

@app.route('/<ran>/post', methods=['GET', 'POST'])
def view_image(ran):
    for file in os.listdir("static/tempdl"):
        if file.endswith(".jpg"):
            print 'removing..'
            print(os.path.join("static/tempdl", file))
            os.remove(os.path.join("static/tempdl", file))

    posturl = request.args.get('imageurl')
    ##print posturl
    filename=posturl.split('/')[-1]
    ##ext=filename.split('.')[-1]
    ##filename='temp.' + ext
    
    
    #handle different files
    if  '.jpg' in posturl:
        downloadImage(posturl, filename)
        return render_template("view_image.html",
                             image=filename)
    elif '.png' in posturl:
        downloadImage(posturl, filename)
        return render_template("view_image.html",
                             image=filename)
    elif 'reddit.com' in posturl:
        return 'Reddit post mirrors not available yet'
    else:
        return render_template("view_post.html",
                             post=filename)


@app.route('/u/<username>')
def view_user(username):
    # Show the user profile of a requested user.
    user_details = rh.get_user_details(username)
    return render_template('view_user.html',
                           user=user_details)


@app.route('/u/<username>/comments')
def view_user_comments(username):
    # Show the comments of a requested user.
    comments_list = rh.get_profile_comments(username, 100, 8)
    return render_template('view_user_comments.html',
                           username=username,
                           comments=comments_list)


@app.route('/u/<username>/submissions')
def view_user_submissions(username):
    # Show the comments of a requested user.
    submissions_list = rh.get_profile_submissions(username, 10)
    return render_template('view_user_submissions.html',
                           username=username,
                           posts=submissions_list.posts)


@app.route('/comments/<post_id>')
def view_comments(post_id):
    # Show the post with the requested id (integer).
    post_details = rh.get_post_details(post_id)
    comments_list = rh.get_all_comments(post_id, 500, 8)
    return render_template('view_comments.html',
                           post=post_details,
                           comments=comments_list)


@app.route('/comments/<post_id>/<comment_id>')
def view_single_comment(post_id):
    return ('Hello world.')


@app.route('/authorise')
def authorise_callback():
    return


def downloadImage(imageUrl, localFileName):
   response = requests.get(imageUrl)
   if response.status_code == 200:
      print('Downloading %s...' % (localFileName))
      with open('static\\tempdl\\' + localFileName, 'wb') as fo:
           for chunk in response.iter_content(4096):
               fo.write(chunk)

#a standard call looks like this
#get_images('http://www.wookmark.com')



# def is_link_img(img):
#     return img.contains(".jpg")

if (__name__ == '__main__'):
    app.run()
