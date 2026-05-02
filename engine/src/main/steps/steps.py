from abc import ABC, abstractmethod

class Step(ABC):

    @abstractmethod
    def execute(self, action, ctx):
        pass

    @abstractmethod
    def available_actions(self, ctx):
        pass

# class ChooseSourceStep(Step):
#     def     