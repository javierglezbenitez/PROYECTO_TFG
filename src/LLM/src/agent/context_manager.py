class ContextManager:

    def __init__(self):
        self.state = {}

    def _ensure_user(self, user_id):
        if user_id not in self.state:
            self.state[user_id] = {
                "history": [],
                "current_name": None,
                "flags": {}
            }

    def has_key(self, user_id, key):
        self._ensure_user(user_id)
        return self.state[user_id]["flags"].get(key, False)

    def set_key(self, user_id, key):
        self._ensure_user(user_id)
        self.state[user_id]["flags"][key] = True

    def set_current_name(self, user_id, name):
        self._ensure_user(user_id)
        self.state[user_id]["current_name"] = name

    def get_current_name(self, user_id):
        self._ensure_user(user_id)
        return self.state[user_id].get("current_name")

    def clear_user(self, user_id):
        if user_id in self.state:
            del self.state[user_id]


context_manager = ContextManager()