class LuscherTestHandler:
    def __init__(self) -> None:
        pass

    LuscherTestResult = []
    LuscherTestCur = ['blue', 'green', 'red', 'yellow', 'purple', 'black', 'grey', 'brown']
    LuscherTestDone = False

    def clear_results(self):
        LuscherTestHandler.LuscherTestResult = []
        LuscherTestHandler.LuscherTestCur = ['blue', 'green', 'red', 'yellow', 'purple', 'black', 'grey', 'brown']
        LuscherTestHandler.LuscherTestDone = False
