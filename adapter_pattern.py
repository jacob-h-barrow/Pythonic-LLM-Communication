"""
    Adapter Pattern
    
    - Instead of creating destination-specific subclasses, we adapt each destination to the behavior of a file and then pass the adapter to a Logger as its output file.
    - Python encourages duck typing, so an adapter’s only responsibility is to offer the right methods — our adapters, for example, are exempt from the need to inherit from either the classes they wrap or from the file type they are imitating. 
    - They are also under no obligation to re-implement the full slate of more than a dozen methods that a real file offers.
"""

from sys import argv
from logger_class import FilteredLogger, Accepted
from open_ai_class import PromptEngineering, Options
from typing import TypeAlias, Tuple

class SatTesting(PromptEngineering):
    reading_comprehension: str = 'Create a paired passage question of literature for reading and writing section in SAT with difficulty level %s along with answer and explanation. Use the following topic to guide your passage: %s' # % (difficulty, topic)
    math_comprehension: str = 'Create a word problem question for math section in SAT with difficulty level %s along with answer and explanation. Use the following topic to guide your word problem: %s' # % (difficulty, topic)
    
    question_types: Options = ('reading_comprehension', 'math_comprehension')
    difficulties: Options = ('easy', 'medium', 'hard')
    # topics: Options = (Any)
    
    
    def __init__(self, open_ai_key: str):
        super().__init__(oepn_ai_key)
        
    def compose_question(self, question_type: str, difficulty: str, topic: str) -> str:
        prompt: str = ''
        
        if question_type not in self.question_types or difficulty not in self.difficulties: # or topic not in self.topics
            raise Exception(f'{question_type} or {difficulty} or {topic} isnt supported!')
            
        match question_type:
            case 'reading_comprehension':
                prompt = self.reading_comprehension % (difficulty, topic)
            case _:
                prompt = self.math_comprehension % (difficulty, topic)
                
        return prompt
        
    # question type -> reading/math comprehension
    # difficulty -> easy, medium, hard
    # topic -> unguided check right now
    def generate_question(self, question_type: str, difficulty: str, topic: str) -> Accepted:
        prompt = self.compose_question(question_type, difficulty, topic)
        
        return self.get_completion(prompt)
        
if __name__ == "__main__":
    openai_key: str = argv[1]
    
    highschool = SatTesting(openai_key)
    # Better option with bridge here???
    gradeschool = GradeSchool(openai_key, grade='1')
    
    sat_logger = ChatGptFilterLogger('/var/log/sat.log')
    gradeschool_logger = ChatGptFilterLogger('/var/log/gradeschool.log')
    
    sat_logger.log(highschool.generate_question('reading_comprehension', 'medium', 'cybersecurity related to customer\'s data privacy retention laws'))
    gradeschool_logger.log(gradeschool.generate_question('math_comprehension', 'hard', 'trigonometry'))    
