class Task:
    def __init__(self, title: str, priority: int = 2, done: bool = False):
        self.title = title
        self.priority = priority
        self.done = done

    def toggle_status(self):
        self.done = not self.done

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            priority = data.get("priority", 2),
            done = data.get("done", False)
        )

    def __str__(self):
        status = "✅" if self.done else "🔲"
        icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(self.priority, "")
        return f"{status} {icon} {self.title}"
