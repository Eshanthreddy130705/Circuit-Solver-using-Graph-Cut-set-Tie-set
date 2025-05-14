def check_float(string):
    try:
        float(string)
        return True
    except:
        return False