from fastapi import Header


def current_user(x_user_id: str = Header(min_length=1, max_length=64)) -> str:
    return x_user_id
