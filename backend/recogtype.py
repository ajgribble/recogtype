# ----------------------------------------------------------------------------
# --- Author:   Adam Gribble                                               ---
# --- Title:    recogtype.py                                               ---
# --- Date:     July 2, 2012                                               ---
# --- Summary:  Python module for the preprocessing, feature extracting,   ---
# ---           model building and recognition of users' keystrokes        ---

import json
import psycopg2

import pylab as pl
import matplotlib as mpl
import numpy as np

from sklearn.cross_validation import StratifiedKFold
from sklearn.mixture import GMM

class RecogDataSample():
    def __init__(self):
        self.data = []
        self.feature_types = {}
        self.features = [] 

    def set_data(self, data_id):
        # Initialize local variables
        deletion_list = []

        # Connect to the database
        try:
            conn = psycopg2.connect("** DB INFO **")
        except:
            print "Cannot connect to the database"
        
        # Query the database for the raw data
        cur = conn.cursor() 
        query = 'SELECT data FROM recogmatch_rawsample WHERE id=%s' \
            % data_id 
        cur.execute(query)
        raw_data = cur.fetchall() 
        raw_data = json.loads(raw_data[0][0])
        conn.close()
                
        # Clean up each keystroke
        for index, keystroke in enumerate(raw_data):
            if keystroke['up_code'] == 8:
                deletion_list.append(index)
            if keystroke['val_press'] != keystroke['val_up']:
                if keystroke['val_press'] == keystroke['val_up'].lower():
                    keystroke['val_up'] = keystroke['val_up'].lower()
                elif keystroke['up_code'] == 188:
                    keystroke['val_up'] = ','
                elif keystroke['press_code'] == 32:
                    keystroke['val_up'] = keystroke['val_up'].lower()
                elif keystroke['press_code'] < 65 and keystroke['val_up'] > 90:
                    keystroke['val_up'] = keystroke['val_press']
                elif keystroke['press_code'] > 122 or keystroke['press_code'] < 65:
                    keystroke['val_up'] = keystroke['val_up'].lower()
                else:
                    keystroke['val_up'] = keystroke['val_up'].lower()

        # Removes all of the uses of the delete key
        deletion_list.sort()
        deletion_list.reverse()
        for k in deletion_list:
            raw_data.pop(k)
       
        # Set the newly preprocessed data to the object
        self.data = raw_data

        return self.data

    # Features optionally chosen are flagged to be extracted, the keywork 'all'
    # may be used to extract all possible features.
    def set_feature_types(self, feature_types): 
        # Initialize local variables
        if feature_types == 'all':
            self.feature_types['dwell'] = True
            self.feature_types['latency'] = True
            self.feature_types['interval'] = True
            self.feature_types['flight'] = True
            self.feature_types['up2up'] = True
        else:
            self.feature_types['dwell'] = False
            self.feature_types['latency'] = False
            self.feature_types['interval'] = False
            self.feature_types['flight'] = False
            self.feature_types['up2up'] = False

            # Loop through list of feature types to pull and set flags
            for t in feature_types:
                if t == 'dwell':   
                    self.feature_types['dwell'] = True
                elif t == 'latency':                   
                    self.feature_types['latency'] = True
                elif t == 'interval':
                    self.feature_types['interval'] = True
                elif t == 'flight':
                    self.feature_types['flight'] = True
                elif t == 'up2up':
                    self.feature_types['up2up'] = True 
                else:
                    pass
    # Extracts requested features from: dwell, latency, interval, 
    # flight and up2up
    def set_features(self, data):
        # Initialize local variables
        feature_count = 0
        # Create empty feature matrix
        for key, val in self.feature_types.items():
            if val == True:
                feature_count += 1
        self.features = np.zeros((len(data)-1, feature_count))
 
        # Pull requested features from each digraph or individual keystroke
        for index, keystroke in enumerate(data):
            # Initiate counter for feature to pull
            feature_counter = feature_count - 1

            # Get first and second keys pressed in digraph
            key1 = keystroke
            try:
                key2 = data[index + 1]
            except IndexError:
                break
            
            # Pulls different timings as features
            digraph = key1['val_up'] + key2['val_up']
            
            if self.feature_types['dwell'] == True:
                self.features[index, feature_counter] = key1['up'] - key1['down']
                feature_counter -= 1
            if self.feature_types['interval'] == True:
                self.features[index, feature_counter] = key2['up'] - key1['down']
                feature_counter -= 1
            if self.feature_types['latency'] == True:
                self.features[index, feature_counter] = key2['down'] - key1['up']
                feature_counter -= 1
            if self.feature_types['flight'] == True:
                self.features[index, feature_counter] = key2['down'] - key1['down']
                feature_counter -= 1
            if self.feature_types['up2up'] == True:
                self.features[index, feature_counter] = key2['up'] - key1['up']
                feature_counter -= 1             

    def build_model(self):

        target = np.zeros(len(self.data))
        skf = StratifiedKFold(target, k=4)
        train_index, test_index = skf.__iter__().next()

        X_train = self.data[train_index]
        y_train = target[train_index]
        X_test = self.data[test_index]
        y_test = target[test_index]

        n_classes = len(np.unique(y_train))

        classifiers = dict((covar_type, GMM(n_components=n_classes,
                            covariance_type=covar_type, init_params='wc', \
                            n_iter=20))
                            for covar_type in ['spherical', 'diag', \
                            'tied', 'full'])

        n_classifiers = len(classifiers)

        pl.figure(figsize=(3 * n_classifiers / 2, 6))
        pl.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
                           left=.01, right=.99)

        for index, (name, classifier) in enumerate(classifiers.iteritems()):
            # Since we have class labels for the training data, we can
            # initialize the GMM parameters in a supervised manner.
            classifier.means_ = np.array([X_train[y_train == i].mean(axis=0)
                                          for i in xrange(n_classes)])

            # Train the other parameters using the EM algorithm.
            classifier.fit(X_train)

            h = pl.subplot(2, n_classifiers / 2, index + 1)
            make_ellipses(classifier, h)

            for n, color in enumerate('rgb'):
                data = self.data[target == n]
                pl.scatter(data[:, 0], data[:, 1], 0.8, color=color,
                            label=iris.target_names[n])
            # Plot the test data with crosses
            for n, color in enumerate('rgb'):
                data = X_test[y_test == n]
                pl.plot(data[:, 0], data[:, 1], 'x', color=color)

            y_train_pred = classifier.predict(X_train)
            train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
            pl.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
                            transform=h.transAxes)

            y_test_pred = classifier.predict(X_test)
            test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
            pl.text(0.05, 0.8, 'Test accuracy: %.1f' % test_accuracy,
                            transform=h.transAxes)

            pl.xticks(())
            pl.yticks(())
            pl.title(name)

        pl.legend(loc='lower right', prop=dict(size=12))


        pl.show()

        def make_ellipses(gmm, ax):
            for n, color in enumerate('rgb'):
                v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
                u = w[0] / np.linalg.norm(w[0])
                angle = np.arctan2(u[1], u[0])
                angle = 180 * angle / np.pi  # convert to degrees
                v *= 9
                ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
                                          180 + angle, color=color)
                ell.set_clip_box(ax.bbox)
                ell.set_alpha(0.5)
                ax.add_artist(ell)
