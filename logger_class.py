from pathlib import Path
from typing import TypeAlias

File_Location: TypeAlias = Path | str
Accepted: TypeAlias = bool | str
Response: TypeAlias = Tuple[Accepted, str]

class Logger:
    def __init__(self, path: File_Location):
        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path
            
    def log(self, message: str, encoding: str = 'utf-8') -> Accepted:
        try:
            # Test a+
            with self.path.open(mode='a+', encoding=encoding) as appender:
                appender.write(message)
                
            return True
        except Exception as e:
            return str(e)
            
class ChatGptFilteredLogger(Logger):
    def __init__(self, path: File_Location):
        super().__init__(path)

    def log(self, response: Response) -> Accepted:
        if response[0] == True
            # super().log(message)
            self.log(message)
            
        return repsonse[0]
