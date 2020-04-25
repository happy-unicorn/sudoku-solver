import os
import pickle
import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier


class KNNService:
    @staticmethod
    def train_classifier(path):
        mnist = datasets.fetch_openml('mnist_784', data_home='mnist_dataset/')
        data, target = mnist.data, mnist.target
        indices = np.random.choice(len(target), 70000, replace=False)
        classifier = KNeighborsClassifier(n_neighbors=3)
        train_img = [data[i] for i in indices[:50000]]
        train_img = np.array(train_img)
        train_target = [target[i] for i in indices[:50000]]
        train_target = np.array(train_target)
        test_img = [data[i] for i in indices[60000:70000]]
        test_img1 = np.array(test_img)
        test_target = [target[i] for i in indices[60000:70000]]
        test_target1 = np.array(test_target)
        classifier.fit(train_img, train_target)
        pickle.dump(classifier, open(path, 'wb'))

    @staticmethod
    def predict(numbers, path):
        classifier = pickle.load(open(os.path.dirname(__file__) + path, 'rb'))
        new_ar = []
        for row in numbers:
            new_row = []
            for elem in row:
                new_elem = elem.flatten()
                if new_elem.mean() < 10:
                    new_row.append(0)
                else:
                    pred = classifier.predict(np.array([new_elem]))
                    new_row.append(int(pred[0]))
            new_ar.append(new_row)

        return new_ar
