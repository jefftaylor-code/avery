import subprocess
import sys
import tempfile
from pathlib import Path

import db


JEFF_MEMORY = "Jeff's favorite test animal is an otter."
USER2_MEMORY = "Test User 2's favorite test animal is a red panda."


def verify_database(db_path):
    db.DB_PATH = Path(db_path)

    jeff_memories = db.get_memories("jeff")
    user2_memories = db.get_memories("testuser2")

    assert JEFF_MEMORY in jeff_memories, \
        "Jeff's otter memory was not found after restart."

    assert USER2_MEMORY in user2_memories, \
        "Test User 2's red panda memory was not found after restart."

    assert USER2_MEMORY not in jeff_memories, \
        "FAIL: Test User 2 memory leaked into Jeff."

    assert JEFF_MEMORY not in user2_memories, \
        "FAIL: Jeff memory leaked into Test User 2."

    print("PASS: persistence survived process restart")
    print("PASS: Jeff -> otter")
    print("PASS: Test User 2 -> red panda")
    print("PASS: no cross-user memory leakage")


def run_test():
    with tempfile.TemporaryDirectory() as temp_dir:

        test_db = Path(temp_dir) / "gate0_test.db"

        db.DB_PATH = test_db
        db.init_db()

        db.add_user("jeff", "Jeff")
        db.add_user("testuser2", "Test User 2")

        db.add_memory_if_new(
            "jeff",
            JEFF_MEMORY
        )

        db.add_memory_if_new(
            "testuser2",
            USER2_MEMORY
        )

        # Verify isolation in the current process.
        jeff_memories = db.get_memories("jeff")
        user2_memories = db.get_memories("testuser2")

        assert JEFF_MEMORY in jeff_memories
        assert USER2_MEMORY in user2_memories
        assert USER2_MEMORY not in jeff_memories
        assert JEFF_MEMORY not in user2_memories

        print("PASS: initial user isolation")

        # Launch a completely new Python process against the same DB.
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--verify",
                str(test_db)
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout, end="")

        if result.returncode != 0:
            print(result.stderr)
            raise SystemExit(
                "FAIL: restart verification process failed."
            )

        print("\nGATE 0 REGRESSION: PASS")


if __name__ == "__main__":

    if len(sys.argv) == 3 and sys.argv[1] == "--verify":
        verify_database(sys.argv[2])

    else:
        run_test()