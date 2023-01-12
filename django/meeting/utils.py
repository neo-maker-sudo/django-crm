import secrets

rooms = []

def generate_room_name():
    global rooms

    while True:
        room_name = secrets.token_hex(10)

        if room_name not in rooms:
            rooms.append(room_name)
            break

    return room_name