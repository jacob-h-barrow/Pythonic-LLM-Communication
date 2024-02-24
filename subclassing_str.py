from datetime import datetime

class ImmutableCustomStr(str):
    pattern = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self, data):
        if isinstance(data, str):
            self.type, self.data = 'str', data
        elif isinstance(data, datetime):
            self.type, self.data = 'datetime', data.strftime(self.pattern)
        else:
            raise Exception(f'Not working with this type: { type(data) }')
                
    def get(self):
        # Only two types right now!
        match self.type:
            case 'str':
                return self.data
            case _:
                # Datetime Object
                return datetime.strptime(self.data, self.pattern)
            
    def __setitem__(self, index, value):
        raise Exception('Setting is not allowed')
        
    def __delitem__(self, index):
        raise Exception('Deletion is not allowed')
        
    def __del__(self):
        return "Out of scope still works"
        
if __name__ == "__main__":
    now_obj = datetime.now()
    now_str = now_obj.strftime(ImmutableCustomStr.pattern)

    print(f'Type of now_obj is { type(now_obj) } and the type of now_str is { type(now_str)} ')

    immutable_obj = ImmutableCustomStr(now_obj)
    immutable_str = ImmutableCustomStr(now_str)

    print(f'Type of immutable_obj is { type(immutable_obj.get()) } and the type of immutable_str is { type(immutable_str.get())} ')
