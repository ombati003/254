import uuid

def generate_ref_code():
    refferal_code = str(uuid.uuid4()).replace("-", "")[:12]
    return refferal_code