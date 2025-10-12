class LLMError(TypeError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"
