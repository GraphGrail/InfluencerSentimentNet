import copy

class Collocation:
    def __init__(self):
        self._words = None
        self._maxDistance = 0
        self._orderRespect = False
        
    def search(self, wordList, closedPositions=set()):
        collocationPositions = []
        minPosition = 0
        while True:
            openDiapason = self._findClosestOpenDiapason(minPosition, len(wordList) - 1, closedPositions)
            if openDiapason is None:
                return collocationPositions
            collocDiapason = None
            if self._orderRespect == True:
                collocDiapason = self._findCollocationInDiapason(wordList, openDiapason)
            else:
                collocDiapason = self._findCollocationInDiapasonWithoutOrderRespect(wordList, openDiapason)
            if len(collocDiapason) == 0:
                minPosition = openDiapason[1] + 1
                continue
            collocationPositions.append(collocDiapason)
            minPosition = collocDiapason[1] + 1
            for bias in range(collocDiapason[1] - collocDiapason[0] + 1):
                closedPositions.add(bias + collocDiapason[0])
    
    # Setters and getters:
    
    def setMaxDistance(self, d):
        self._maxDistance = d
    def getMaxDistance(self):
        return self._maxDistance
    
    def setWords(self, words):
        self._words = words
    def getWords(self):
        return self._words
    def getCollocationSize(self):
        return len(self._words)
    
    def setOrderRespect(self, orderRespect):
        self._orderRespect = orderRespect
    def orderRespect(self):
        return self._orderRespect
        
    # Private functions:
    
    @staticmethod
    def _findClosestOpenDiapason(pos, maxPos, closedPositions):
        openDiapason = []
        while pos <= maxPos:
            if pos not in closedPositions:
                openDiapason.append(pos)
                openDiapason.append(pos)
                break
            pos += 1
        if len(openDiapason) == 0:
            return None
        pos += 1
        while pos <= maxPos:
            if pos in closedPositions:
                openDiapason[1] = pos - 1
                return openDiapason
            pos += 1
        openDiapason[1] = maxPos
        return openDiapason
            
    def _findCollocationInDiapason(self, wordList, openDiapason):
        if openDiapason[1] - openDiapason[0] + 1 < len(self._words):
            return []
        openDiapason = copy.copy(openDiapason)
        previousPosition = None
        collocationDiapason = []
        i = 0
        while i < len(self._words):
            pos = self._searchForWordPosition(wordList, self._words[i], openDiapason)
            if pos is None:
                return []
            if previousPosition is not None and pos - previousPosition > self._maxDistance + 1:
                openDiapason[0] += 1
                i = 0
                previousPosition = None
                collocationDiapason = []
                continue
            if len(collocationDiapason) == 0:
                collocationDiapason.append(pos)
                collocationDiapason.append(pos)
            else:
                collocationDiapason[1] = pos
            openDiapason[0] = pos + 1
            previousPosition = pos
            i += 1
            
        return collocationDiapason
    
    def _findCollocationInDiapasonWithoutOrderRespect(self, wordList, openDiapason):
        if openDiapason[1] - openDiapason[0] + 1 < len(self._words):
            return []
        openDiapason = copy.copy(openDiapason)
        collocationDiapason = []
        wordFound = [False] * len(self._words)
        i = openDiapason[0]
        while i <= openDiapason[1]:
            if len(collocationDiapason) != 0 and i - collocationDiapason[1] > self._maxDistance + 1:
                collocationDiapason = []
                wordFound = [False] * len(self._words)
            g = 0
            while g < len(self._words):
                if wordList[i] == self._words[g]:
                    wordFound[g] = True
                    if len(collocationDiapason) == 0:
                        collocationDiapason.append(i)
                        collocationDiapason.append(i)
                    else:
                        collocationDiapason[1] = i
                    allWordsFound = True
                    for wf in wordFound:
                        if wf == False:
                            allWordsFound = False
                            break
                    if allWordsFound == True:
                        return collocationDiapason
                    break
                g += 1
            i += 1
        return []
                
    @staticmethod
    def _searchForWordPosition(wordList, word, openDiapason=None):
        if openDiapason is None:
            i = 0
            while i < len(wordList):
                if word == wordList[i]:
                    return i
                i += 1
        else:
            i = openDiapason[0]
            while i < openDiapason[1]:
                if word == wordList[i]:
                    return i
                i += 1
        return None
            
       # Fields:
    
    _words = None
    _maxDistance = None
    _orderRespect = None
    
    