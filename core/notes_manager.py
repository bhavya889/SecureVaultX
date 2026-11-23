import json

from core.encryption import CryptoEngine


class NotesManager:
    """Small application layer keeping note serialization and encryption together."""

    def __init__(self, database):
        self.database = database

    def create_note(self, dek, title, body):
        payload = json.dumps(
            {"title": title, "body": body},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        encrypted = CryptoEngine.encrypt_note(dek, payload)
        return self.database.add_note(encrypted)

    def read_notes(self, dek):
        result = []
        for row in self.database.get_all_notes():
            try:
                data = json.loads(CryptoEngine.decrypt_note(dek, row["encrypted_data"]))
                result.append({
                    "id": row["id"],
                    "title": data.get("title", "Untitled"),
                    "body": data.get("body", ""),
                    "pinned": row["pinned"],
                })
            except (ValueError, KeyError, TypeError):
                # Do not expose unreadable/corrupted ciphertext as plaintext.
                continue
        return result

    def delete_note(self, note_id):
        self.database.delete_note(note_id)
