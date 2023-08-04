def check_input(input) :
    """_To check the type of an input_
 
    Args:
        input (_input_): _The input whose type we want to know_

    Returns:
        type (_type_): _The type of the input_
    """
    try :
        # Convert it into integer
        val = int(input)
        if float(val) == float(input) :
            type = 'int'
        else : 
            type = 'float'
    except ValueError :
        try :
            # Convert it into float
            val = float(input)
            type = 'float'
        except ValueError :
            type = 'str'
    return type