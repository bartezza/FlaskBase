
import traceback
import uuid


def new_id():
    return str(uuid.uuid4())


def dump_exception():
    traceback.print_exc()
