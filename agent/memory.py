class ConversationMemory:
    def __init__(self, max_turns=20):
        self.max_turns = max_turns
        self.history = []
        self.summary = ""

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            self._compress()

    def _compress(self):
        mid = len(self.history) // 2
        old_msgs = self.history[:mid]
        old_text = "\n".join(
            [f"{m['role']}: {m['content'][:100]}" for m in old_msgs]
        )
        self.summary = f"[历史摘要] {old_text[:500]}..."
        self.history = self.history[mid:]

    def get_messages(self, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        if self.summary:
            messages.append(
                {"role": "system", "content": f"之前的对话摘要：{self.summary}"}
            )
        messages.extend(self.history)
        return messages

    def clear(self):
        self.history = []
        self.summary = ""