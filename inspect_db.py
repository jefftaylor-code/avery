from db import get_connection


with get_connection() as conn:

    print("\nUSERS")
    print("-----")

    users = conn.execute(
        "SELECT id, display_name FROM users ORDER BY id"
    ).fetchall()

    for user in users:
        print(user)

    print("\nMEMORIES")
    print("--------")

    memories = conn.execute(
        """
        SELECT id, user_id, memory, created_at
        FROM memories
        ORDER BY id
        """
    ).fetchall()

    for memory in memories:
        print(memory)