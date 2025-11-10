class MixedColorTypesError(TypeError):
    """Raised when ANSI and HTML color types are both used in the same style call."""

    def __init__(self, fg_type: str, bg_type: str):
        self.fg_type = fg_type
        self.bg_type = bg_type
        super().__init__(
            "Cannot mix ANSI and HTML color types. "
            f"Foreground: {fg_type}, Background: {bg_type}. "
        )
