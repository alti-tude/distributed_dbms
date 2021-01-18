def strFormat(value):
    value = str(value)
    return f"'{value}'"

def numericFormatOfType(type):
    return lambda value: numericFormat(value, type)
    
def numericFormat(value, type):
    value = type(value)
    return f"{value}"

