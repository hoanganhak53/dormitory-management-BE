from . import auth, profile, user_type, student, post, form

user_data_routes = [
    auth.route,
    profile.route,
    user_type.route,
    student.route,
    post.route,
    form.route
]