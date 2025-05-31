from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_blog_post(dict_blog_post):
    if 'title' not in dict_blog_post or 'content' not in dict_blog_post:
        return False
    return True


@app.route('/api/posts', methods = ['POST'])
def add_posts():
    new_blog_post = request.get_json()
    print(new_blog_post)
    if not validate_blog_post(new_blog_post):
        return 'Input invalid', 400

    if len(POSTS) > 0:
        new_id = max(blog_post['id'] for blog_post in POSTS) + 1
    else:
        new_id = 1

    new_blog_post['id'] = new_id

    POSTS.append(new_blog_post)
    return jsonify(new_blog_post), 201


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
