
class ETLError(Exception):
    pass


class DataGenerationError(ETLError):
    def __init__(self, message="Error generating data"):
        super().__init__(message)


class DataCleaningError(ETLError):
    def __init__(self, message="Error cleaning data"):
        super().__init__(message)


class MetricsGenerationError(ETLError):
    def __init__(self, message="Error generating metrics"):
        super().__init__(message)
