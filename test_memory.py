from db import init_db, add_user, add_memory, get_memories


init_db()

add_user("jeff", "Jeff")

add_memory(
    "jeff",
    "Jeff's favorite test animal is an otter."
)

memories = get_memories("jeff")

print("Jeff's memories:")

for memory in memories:
    print("-", memory)