import copy
import random
from players.scripts.Script import Script


class DSL:
    
    def __init__(self):
        
        self.start = 'S'
        
        self._grammar = {}
        self._grammar[self.start] = ['B S', '']
        self._grammar['B'] = ['B1', 'B1 and B1']
        self._grammar['B1'] = ['DSL.isDoubles(a)', 'DSL.containsNumber(a, NUMBER )', 'DSL.actionWinsColumn(state,a)', 'DSL.hasWonColumn(state)',
                               'DSL.numberPositionsProgressedThisRoundColumn(state, NUMBER ) > SMALL_NUMBER and DSL.isStopAction(a)', 'DSL.isStopAction(a)',
                               'DSL.numberPositionsConquered(state, NUMBER ) > SMALL_NUMBER and DSL.containsNumber(a, NUMBER )']
        # dont put space in function parameter if no Number
        self._grammar['NUMBER'] = ['2', '3', '4', '5', '6']
        self._grammar['SMALL_NUMBER'] = ['0', '1', '2']

        self.numberOfRules = 1  # used for random generate rules

    def generateRandomScript(self, SCNumber=1):
        randomScripts = []
        for a in range(SCNumber):
            realRules = []
            self.numberOfRules = 1
            NumGeneRule = 0
            while NumGeneRule < self.numberOfRules:
                rule = 'S'
                rule = self._grammar[rule][0]  # 'B S'
                rules = rule.split(' ')
                realRule = ''
                for i in rules:
                    partialRule = self.geneRule(i)
                    realRule = realRule + partialRule
                realRules.append([realRule, 1])
                NumGeneRule = NumGeneRule + 1

            # I don't know why we should have the second parameter of real rule
            randomScript = Script(realRules, a)
            randomScripts.append(randomScript)
        return randomScripts

    def geneRule(self, previousRule):
        if previousRule in self._grammar:
            if previousRule == 'S':
                ran_num = random.uniform(0, 1)
                if ran_num > 0.5:
                    self.numberOfRules = self.numberOfRules + 1
                return ''
            nextRule = random.choice(self._grammar[previousRule])
            #nextRule = self._grammar[previousRule][1]
            return self.geneRule(nextRule)
        elif len(previousRule.split(' ')) > 1:
            dividedRule = previousRule.split(' ')
            nextRule = ''
            for i in dividedRule:
                dealedRule = self.geneRule(i)
                if dealedRule == 'and':
                    nextRule = nextRule + ' '
                nextRule = nextRule + dealedRule
                if dealedRule == 'and':
                    nextRule = nextRule + ' '
        else:
            nextRule = previousRule
        return nextRule


    @staticmethod
    def isYNAction(actions):
        if 'n' in actions:
            return True
        else:
            return False

    @staticmethod
    def hasAvailableNeuralMarker(state):
        finished_columns = list(set(state.finished_columns + state.player_won_column))
        return state.count_neutral_markers() < 3 and len(finished_columns) < 3

    @staticmethod
    def hasWonColumn(state):
        """
        Returns true if the player has won a column, i.e., if the player progressed all the way
        to the top of a given column.
        """
        return len(state.columns_won_current_round()) > 0

##############################################################################################

    @staticmethod
    def isDoubles(action):
        """
        Returns true if the action is a double. 
        
        Examples of doubles: (2, 2), (3, 3), (4, ,4)
        """
        if len(action) > 1 and action[0] == action[1]:
            return True
        else:
            return False


    @staticmethod
    def containsNumber(action, number):
        """
        Returns true if the action contains the number
        
        Example: returns true for action (2, 3) and number 3
                 returns true for action (2, 6) and number 4
        """
        if not isinstance(action, str):
            if number in action:
                return True
        return False
    
    @staticmethod
    def actionWinsColumn(state, action):
        """
        Returns true if the action completes a column for the player
        """
        copy_state = copy.deepcopy(state)
        copy_state.play(action)
        columns_won = copy_state.columns_won_current_round()
        columns_won_previously = state.columns_won_current_round()
        if len(columns_won) > 0 and columns_won != columns_won_previously:
            return True
        return False

    @staticmethod
    def continueBecausehighProbNotBust(state):
        progressedColumn = []
        for i in range(2, 7):
            if DSL.numberPositionsProgressedThisRoundColumn(state, i) > 0:
                progressedColumn.append(i)

        finished_columns = list(set(state.finished_columns + state.player_won_column))
        if 4 in finished_columns or (3 in finished_columns and 5 in finished_columns):
            return False
        if (4 in progressedColumn and (3 in progressedColumn or 5 in progressedColumn)) or (3 in progressedColumn and 5 in progressedColumn):
            return True
        return False

    @staticmethod
    def actionEasyToPrograss(state, action):
        if len(action) == 1:
            progressedColumn = []
            for i in range(2, 7):
                if DSL.numberPositionsProgressedThisRoundColumn(state, i) > 0:
                    progressedColumn.append(i)
        else:
            if 4 in action and (3 in action or 5 in action):
                return True
        return False

    @staticmethod
    def actionsUseLessMarker(state, actions):
        progressedColumn = []
        for i in range(2, 7):
            if DSL.numberPositionsProgressedThisRoundColumn(state, i) > 0:
                progressedColumn.append(i)

        goodActions = []
        bestActions = []
        for action in actions:
            if len(action) == 1:
                if action[0] in progressedColumn:
                    bestActions.append(action)
            else:
                if action[0] in progressedColumn and action[1] in progressedColumn:
                    bestActions.append(action)
                elif action[0] in progressedColumn or action[1] in progressedColumn:
                    goodActions.append(action)

        if bestActions:
            return bestActions
        if goodActions:
            return goodActions
        return actions

####################################################################################

    @staticmethod
    def numberPositionsProgressedThisRoundColumn(state, column):
        """
        Returns the number of positions progressed in a given column in the current round.
        A round finishes once the player chooses to stop, which is action n in this implementation.
        """
        return state.number_positions_conquered_this_round(column)

    @staticmethod
    def numberPositionsConquered(state, column):
        """
        Returns the number of positions conquered in a given column. A position is
        conquered once the player progresses in the column and decides to stop. By stopping, the
        temporary markers are replaced by permanent markers and the positions are conquered. 
        """
        return state.number_positions_conquered(column)
    
    @staticmethod
    def isStopAction(action):
        """
        Returns true if the action is a stop action, i.e., action n in this implementation.
        """
        if isinstance(action, str) and action == 'n':
            return True
        return False

    # @staticmethod
    # def actionWillWin(state, action):
    # # already implemented before??
    #     goingToWinColumn = []
    #     for i in range(2, 7):
    #         if DSL.numberPositionsConquered(state, i) == 5 - 2*abs(i-4):
    #             goingToWinColumn.append(i)
    #     for i in range(2, 7):
    #         if DSL.numberPositionsProgressedThisRoundColumn(state, i) == 5 - 2*abs(i-4):
    #             goingToWinColumn.append(i)
    #     list(set(goingToWinColumn))
    #     assert len(goingToWinColumn) <= 3
    #     for i in goingToWinColumn:
    #         for j in action:
    #             if j == i:
    #                 return True
    #     return False