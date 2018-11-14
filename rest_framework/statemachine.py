#Copyright IBM Corp. 2018.
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from string import upper


class StateMachine():

    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = upper(name)
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = upper(name)

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise "InitializationError", "must call .set_start() before .run()"

        if not self.endStates:
            raise "InitializationError", \
                "at least one state must be an end_state"

        while 1:
            (newState, cargo) = handler(cargo)
            if upper(newState) in self.endStates:
                break
            else:
                handler = self.handlers[upper(newState)]

    def validate(self):
        try:
            self.handlers[self.startState]
        except:
            raise "InitializationError", "must call .set_start() before .run()"

        if not self.endStates:
            raise "InitializationError", \
                "at least one state must be an end_state"

    def is_end_state(self, state):
        if upper(state) in self.endStates:
            return True
        return False

    def step(self, state, cargo):
        handler = self.handlers[upper(state)]
        if handler is None:
            print 'handlers', str(self.handlers)
            print 'handler', handler
        if state is None:
            print 'state', state
        (newState, cargo) = handler(cargo)
        return (newState, cargo)
