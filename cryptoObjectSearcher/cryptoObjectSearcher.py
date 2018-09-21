import csv
import spacy
import os

from .collocation import Collocation

class CryptoObjectSearcher:
    def __init__(self):
        self._nlp = spacy.load('en')
        self._collocationGroups = {}
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects.csv"), "r") as fp:
            reader = csv.reader(fp, delimiter=";")
            header = True
            for row in reader:
                if header == True:
                    header = False
                    continue
                objectId = row[0]
                objectName = row[1]
                objectType = row[2]
                
                separateLemmatizedWords = []
                collocation = Collocation()
                collocation.setMaxDistance(0)
                tokens = self._nlp(objectName)
                for token in tokens:
                    separateLemmatizedWords.append(token.lemma_)
                    collocation.setWords(separateLemmatizedWords)
                    self.addCollocation(collocation, objectId, objectType)
        
    def search(self, doc):
        tokens = self._nlp(doc)
        sentenceLemmatizedWords = []
        for token in tokens:
            sentenceLemmatizedWords.append(token.lemma_)
        
        mentionedObjects = {"projects" : [], "tokens" : []}
        closedPositions = set()
        groupSizes = list(self._collocationGroups.keys())
        groupSizes.sort()
        groupNum = len(groupSizes) - 1
        while groupNum > 0:
            for cw in self._collocationGroups[groupNum]:
                diapasons = cw["collocation"].search(sentenceLemmatizedWords, closedPositions)
                if len(diapasons) != 0:
                    if cw["objectType"] == "project":
                        mentionedObjects["projects"].append(cw["objectId"])
                    else:
                        mentionedObjects["tokens"].append(cw["objectId"])
            groupNum -= 1
        return mentionedObjects
    
    # Setters and getters:
    
    def addCollocation(self, collocation, objectId, objectType):
        length = collocation.getCollocationSize()
        if length not in self._collocationGroups:
            self._collocationGroups[length] = []
        self._collocationGroups[length].append({"collocation" : collocation, "objectId" : objectId, "objectType" : objectType})
    
    # Fields:
    
    _nlp = None
    _collocationGroups = None
    
    