from pre_processing import get_data_for_model
from utils import *
from sklearn.tree import DecisionTreeClassifier
from utils import cross_validation
from BinaryTree import BinaryTree
import numpy as np
import time


# https://dataaspirant.com/2017/01/30/how-decision-tree-algorithm-works/
# https://www.geeksforgeeks.org/decision-tree-introduction-example/
# https://en.wikipedia.org/wiki/Decision_tree
# https://www.youtube.com/watch?v=Qdi0GBWrDO8
# https://medium.com/deep-math-machine-learning-ai/chapter-4-decision-trees-algorithms-b93975f7a1f1
# https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
# http://www.csun.edu/~twang/595DM/Slides/Week4.pdf
# https://learning.oreilly.com/library/view/data-mining-concepts/9780123814791/xhtml/ST0025_CHP008.html#ST0025_CHP008
class DecisionTree:
    "Decision Tree algorithm"
    binaryTree = None
    i = 0

    def create_training_label(self, training, label, index, training_aux):
        has_word_index = np.nonzero(training_aux[:, index])[0]
        has_not_word_index = np.where(training_aux[:, index] == 0)[0]
        has_word_training = []
        has_word_label = []
        has_not_word_training = []
        has_not_word_label = []
        for i in has_word_index:
            has_word_training.append(training[i])
            has_word_label.append(label[i])
        for i in has_not_word_index:
            has_not_word_training.append(training[i])
            has_not_word_label.append(label[i])
        return has_word_training, has_word_label, has_not_word_training, has_not_word_label

    def build_tree(self, training, label, removed_features):
        self.i += 1
        tree = BinaryTree()
        major_class = sum(label)
        negative = (len(label) - major_class) / len(label)
        positive = major_class / len(label)
        if negative >= 0.9:
            tree.value = TRUE_NEWS
            tree.frequency = len(training)
            return tree
        elif positive >= 0.9:
            tree.value = FAKE_NEWS
            tree.frequency = len(training)
            return tree
        elif len(removed_features) == (len(training[1]) - 1) or len(training) <= 576:
            if negative > 0.5:
                tree.value = TRUE_NEWS
                tree.frequency = len(training)
            else:
                tree.value = FAKE_NEWS
                tree.frequency = len(training)
            return tree
        training_aux = np.asarray(training)
        label_aux = np.asarray(label)
        gini_value, word = calculate_gini(training_aux, label_aux, removed_features)
        hwt, hwl, hnwt, hnwl = self.create_training_label(training, label, word, training_aux)
        removed_features.append(word)
        training_aux = None
        label_aux = None
        tree.value = word
        tree.gini = gini_value
        tree.frequency = len(hwt) + len(hnwt)
        if len(hwt) > 3:
            tree.insertHasWord(self.build_tree(hwt, hwl, removed_features))
        if len(hnwt) > 3:
            tree.insertHasNoWord(self.build_tree(hnwt, hnwl, removed_features))
        if len(hwt) <= 3 or len(hnwt) <= 3:
            if negative > 0.5:
                tree.value = TRUE_NEWS
            else:
                tree.value = FAKE_NEWS
            return tree
        return tree

    def fit(self, training, label):
        self.i = 0
        init = time.time()
        self.binaryTree = None
        removed_features =[]
        self.binaryTree = self.build_tree(training, label,removed_features)
        end = time.time()
        print(self.i)
        print(end - init)

    def predict(self, training):
        predictions = []
        for case in training:
            predictions.append(self.binaryTree.find(case))
        return predictions


X, y = get_data_for_model()
print("start")
init = time.time()
# clf_gini = DecisionTreeClassifier(criterion="gini")
cross_validation(X, y, DecisionTree())
end = time.time() - init
print(end)
