from wsgiref.util import request_uri

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_blog_post(dict_blog_post):
    """Checking if title and content was provided."""
    if 'title' not in dict_blog_post or 'content' not in dict_blog_post:
        return False
    return True


@app.route('/api/posts', methods = ['POST'])
def add_posts():
    """logic to add blog post to the list"""
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
    """Logic to load blog posts. If Parameters sort and direction are provided
    result is sorte accordingly. If not, results are not sorted. """
    str_sort = request.args.get('sort', '')
    str_direction = request.args.get('direction', '')

    if str_direction == '' and str_sort == '':
        return jsonify(POSTS)

    if (str_direction == 'asc' or str_direction == 'desc'
        ) and (str_sort == 'title' or str_sort == 'content'):
        if str_direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x[str_sort])
        else:
            sorted_posts = sorted(POSTS, key=lambda x: x[str_sort], reverse = True)
        return jsonify(sorted_posts)
    return 'Bad Request', 400


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Logic to delete post"""
    global POSTS
    # Find the post with the given ID
    post_del = find_post_by_id(id)
    # If the post wasn't found, return a 404 error
    if post_del is None:
        return '404 Not found', 404
    # Remove the post from the list
    POSTS = [post for post in POSTS if post['id'] != id]
    return jsonify({"message": f"Post with id {id} has been deleted successfully."})


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Logic top update post"""
    # Find the post with the given ID

    post = find_post_by_id(id)
    # If the post wasn't found, return a 404 error
    if post is None:
        return '404 Not found', 404

    # Update the book with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated book
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Logic to search posts by title or content"""
    title = request.args.get('title', '')
    content = request.args.get('content', '')
    lst_search_results = []
    if title != '':
        for post in POSTS:
            if title in post['title']:
                lst_search_results.append(post)
    if content != '':
        for post in POSTS:
            if content in post['content']:
                lst_search_results.append(post)
    if len(lst_search_results) == 0:
        return ""
    return jsonify(lst_search_results)


def find_post_by_id(post_id):
    """Returns post with specific id. If none is found, None is returned."""
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
