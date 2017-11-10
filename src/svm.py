import pandas as pd
import numpy as np

from sklearn import svm

import utils
import stockParser as sp


class SVM(object):

    def __init__(self, model_type, zscore=False):
        self.zscore_ = zscore

        if(model_type == 0):
            self.model_ = svm.SVC(kernel='linear')
        elif(model_type == 1):
            self.model_ = svm.SVC(kernel='rbf')


    def train(self, x, y):
        # deep copy
        train_x = x[:]
        train_y = y[:]

        # apply z-score
        if(self.zscore_):
            train_x = utils.applyZScore(train_x)

        self.model_.fit(train_x.values, train_y.values.ravel())

    def predict(self, x):
        # deep copy
        test_x = x[:]

        # apply z-score
        if(self.zscore_):
            test_x = utils.applyZScore(test_x)

        predicted_y = self.model_.predict(test_x)

        # [0, 1, 0, 1] --> [[0],[1],[0],[1]]
        predicted_y = np.array([[predicted_y[i]] for i in range(len(predicted_y))])

        return predicted_y

    def test(self, test_x, test_y):
        predicted_y = self.predict(test_x)

        precision = utils.computePrecision(predicted_y.ravel(), test_y.values.ravel())
        recall = utils.computeRecall(predicted_y.ravel(), test_y.values.ravel())
        accuracy = utils.computeAccuracy(predicted_y.ravel(), test_y.values.ravel())

        print("Precision:", precision)
        print("Recall:", recall)
        print("Accuracy:", accuracy)


def main():
    AAPL = sp.stockParser(utils.AAPL_PATH)

    x, y, date = AAPL.getFluctuationVector(5)
    y = utils.sign(y)

    lm = SVM(1, zscore=True)
    lm.train(x, y)
    lm.test(x, y)

    # utils.KfoldTester(regressionModel(0, zscore=True), x, y, 5)

if __name__ == '__main__':
    main()