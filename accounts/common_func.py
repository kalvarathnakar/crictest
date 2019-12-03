from accounts.models import User

def format_serializer_errors(**kwargs):
    errors_list = []
    for key , val in kwargs.items():
        str1 = " ".join(val)
        str1 = key + " : " + str1
        error_dict = {"field_name" : key, key : str1}
        errors_list.append(error_dict)
    return errors_list



    
class CustomAPIResponse():
    """docstring for ClassName"""
    def __init__(self, **kwargs):
        self.response = {
                "success" : kwargs.get('success'),
                "errors"  : kwargs.get('errors',{}),
                "data": kwargs.get('data', {}),
            }

