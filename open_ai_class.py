import openai
import json
import time

from typing import Any, TypeAlias, Tuple
from re import search

Accepted: TypeAlias = bool | str
Options: TypeAlias = Tuple[str]
Response: TypeAlias = Tuple[Accepted, str]

class PromptEngineering:
    # Need to tweak/modify here!!
    failures: Options = ('Please provide me', 'Can\'t find the data', 'Not provided')
    
    def __init__(self, openai_key: str, model: str = "gpt-3.5-turbo", rate_limited_per_min: int = 3):
        self.openai_key = openai_key
        self.model = model
        self.messages = []
        
        self.load_key()
        
    def load_key(self):
        openai.api_key = self.openai_key
        
    def append_prompt(self, prompt: str) -> bool:
        self.messages.append(
            {"role": "user", "content": prompt},
        )
        
    def solicit_response(self, temperature: int) -> Any: # Not sure the type... look up later
        return openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )
        
    def sucessful_response(self, response: str) -> Accepted:
        for search_pattern in self.failures:
            if re.search(search_pattern, response, re.IGNORECASE):
                raise Exception(f'The response matched a failure pattern: {search_pattern}.\nHere is the response: {response}')
        
        return True
        
    def get_completion(self, prompt: str, temperature: int = 0) -> Response:
        self.append_prompt(prompt)
        
        chat = self.solicit_response(temperature)
        response = chat.choices[0].message.content
        accepted_check = self.successful_response(response)
        
        # Automatic Failure -> Redundant... could later print the error message
        if accepted_check == True:
            return (True, response)
            
        return (False, response)
