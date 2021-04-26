class INTERNAL:
    QUERY = "/internal/query"
    PUT = "/internal/put"

class COMMIT:
    PREPARE = "/commit/prepare"
    GLOBAL_ABORT = "/commit/global_abort"
    GLOBAL_COMMIT = "/commit/global_commit"