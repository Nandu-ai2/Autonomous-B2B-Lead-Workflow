
from typing import Dict
class BaseAgent:
    def __init__(self, step: Dict, env: Dict):
        self.step = step
        self.env = env
        self.logs = []
    def log(self, *args):
        self.logs.append(' '.join(map(str, args)))
        print('[LOG]', *args)
    def run(self, inputs):
        self.log('BaseAgent fallback for', self.step.get('id'))
        return {'ok': True}
