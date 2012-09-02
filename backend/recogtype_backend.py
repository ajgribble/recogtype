# ----------------------------------------------------------------------------
# --- Author:   Adam Gribble                                               ---
# --- Title:    recogtype.py                                               ---
# --- Date:     July 2, 2012                                               ---
# --- Summary:  Python module for the preprocessing, feature extracting,   ---
# ---           model building and recognition of users' keystrokes        ---

import json

import pylab as pl
import matplotlib as mpl
import numpy as np

from sklearn import svm

from django.conf import settings
#from sklearn.mixture import GMM, DPGMM
#from sklearn import preprocessing

class RecogDataSample():
    def __init__(self):
        self.clean_data = []
        self.feature_types = []
        self.feature_vals = np.array([])
        self.feature_digraphs = np.array([])
        self.keystroke_dict = {}

    def set_data(self, raw_data_item):
        # Inner method to clean up keystrokes
        def ks_clean_up(raw_item):
            deletion_list = []

            # Clean up each keystroke
            for index, keystroke in enumerate(raw_item):
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
                raw_item.pop(k)

            # Append the newly preprocessed data to the clean_data list
            self.clean_data.append(raw_item)
 
        # If an external data item was not given 
        if isinstance(raw_data_item, list):
            # For each element in list
            for item in raw_data_item: 
                raw_item = json.loads(item)
                ks_clean_up(raw_item)
        else:
            raw_item = json.loads(raw_data_item)
            ks_clean_up(raw_item)
       
        return True
    
    # Load the dictionary of digraphs and trigraphs to pull from observations
    def load_keystroke_list(self, external_ks_dict=None, selective_ks_list=None):
            # Creates the default keystroke lists based on statistics on the 
            # English language

            # Selective ks list options
            selective_ks_list_options = ('first letters','second letters',
                                         'third letters','ending letters',
                                         'common digraphs','common trigraphs',
                                         'common doubles','common 2l words',
                                         'common 3l words','common 4l words',
                                         'most common words')

            # The most common first letter in a word in order of frequency
            first_letters = ['t','o','a','w','b','c','d','s','f', 
                             'm','r','h','i','y','e','g','l','n', 
                             'u','j','k']

            # The most common second letter in a word in order of frequency
            second_letters = ['h','o','e','i','a','u','n','r','t']

            # The most common third letter in a word in order of frequency
            third_letters = ['e','s','a','r','n','i']

            # More than half of all words end with
            ending_letters = ['e','t','d','s']

            # Most common digraphs on order of frequency
            common_digraphs = ['th','he','an','in','er','on','re','ed','nd', 
                               'ha','at','en','es','of','nt','ea','ti','to', 
                               'io','le','is','ou','ar','as','de','rt','ve']
            
            # The most common trigraphs in order of frequency
            common_trigraphs = ['the','and','tha','ent','ion','tio','for','nde', 
                                'has','nce','tis','oft','men']

            # The most common double letters in order of frequency
            common_doubles = ['ss','ee','tt','ff','ll','mm','oo']

            # The most common two-letter words in order of frequency
            common_2l_words = ['of','to','in','it','is','be','as','at','so', 
                               'we','he','by','or','on','do','if','me','my', 
                               'up','an','go','no','us','am'] 

            # The most common three-letter words in order of frequency
            common_3l_words = ['the','and','for','are','but','not','you', 
                               'all','any','can','had','her','was','one', 
                               'our','out','day','get','has','him','his', 
                               'how','man','new','now','old','see','two', 
                               'way','who','boy','did','its','let','put', 
                               'say','she','too','use'] 

            # The most common four-letter words in order of frequency
            common_4l_words = ['that','with','have','this','will','your', 
                               'from','they','know','want','been','good', 
                               'much','some','time','very','when','come', 
                               'here','just','like','long','make','many', 
                               'more','only','over','such','take','than', 
                               'them','well','were'] 
    
            # The most commonly used words in the English language 
            # in order of frequency
            most_common_words =['the','of','and','to','in','a','is','that',
                                'be','it','by','are','for','was','as','he',
                                'with','on','his','at','which','but','from',
                                'has','this','will','one','have','not','were',
                                'or','all','their','an','I','there','been',
                                'many','more','so','when','had','may','today',
                                'who','would','time','we','about','after',
                                'dollars','if','my','other','some','them',
                                'being','its','no','only','over','very','you',
                                'into','most','than','they','day','even',
                                'made','out','first','great','must','these',
                                'can','days','every','found','general','her',
                                'here','last','new','now','people','public',
                                'said','since','still','such','through',
                                'under','up','war','well','where','while',
                                'years','before','between','country','debts',
                                'good','him','interest','large','like','make',
                                'our','take','upon','what'] 

            # If user has not provided an external list of character groupings
            if not external_ks_dict and not selective_ks_list:
                self.keystroke_dict = {'first letters': first_letters,
                                       'second letters': second_letters,
                                       'third letters': third_letters,
                                       'ending letters': ending_letters,
                                       'common digraphs': common_digraphs,
                                       'common trigraphs': common_trigraphs,
                                       'common doubles': common_doubles,
                                       'common 2l words': common_2l_words,
                                       'common 3l words': common_3l_words,
                                       'common 4l words': common_4l_words,
                                       'most common words': most_common_words}
            
            elif external_ks_dict:
                self.keystroke_dict = external_ks_dict

            elif selective_ks_list:
                for i in selective_ks_list:
                    for j in selective_ks_list_options:
                        if i == j:
                            dict_val = j.replace(' ', '_')
                            self.keystroke_dict[j] = eval(dict_val)
            else:
                return False


    # Extracts requested features from: dwell, latency, interval, 
    # flight and up2up
    def pull_features(self, feature_list):
        # Set feature definition dictionary
        feature_dict = {'dwell': "key1['up'] - key1['down']",
                        'interval': "key2['up'] - key1['down']",
                        'latency': "key2['down'] - key1['up']",
                        'flight': "key2['down'] - key1['down']",
                        'up2up': "key2['up'] - key1['up']"}
       
        # Keyword 'all' may be used to collect every feature type
        if feature_list[0] == 'all':
            for key, val in feature_dict.iteritems():
                self.feature_types.append(key)
        else:
            for key, val in feature_dict.iteritems():
                if key in feature_list:
                    self.feature_types.append(key)

        temp_feature_vals = []

        # For each list of keystrokes in self.clean_data
        for item in self.clean_data:
            temp_feature_digraphs = []
            # Pull requested features from each digraph or individual keystroke
            for index, keystroke in enumerate(item):
                if index != len(item) - 1:
                    # Get first and second keys pressed in digraph
                    key1 = keystroke
                    key2 = item[index + 1]
                
                    # Pulls the digraph being examined
                    digraph = key1['val_up'] + key2['val_up']

                    # Only pulls features out of the digraph if it is 
                    # recognized in the keystroke dictionary
                    for key, val in self.keystroke_dict.items():
                        if digraph.lower() in val:
                            temp_row = []
                            temp_feature_digraphs.append(digraph)
                            
                            for i, val in enumerate(self.feature_types):
                                feature = eval(feature_dict[val])
                                temp_row.append(feature)
                            temp_feature_vals.append(temp_row)
            
            if self.feature_vals.shape != (0,):
                self.feature_vals = np.vstack((self.feature_vals,
                                               np.array(temp_feature_vals)))
            else:
                self.feature_vals = np.array(temp_feature_vals)
            
        self.feature_digraphs = np.asarray(temp_feature_digraphs)

        return self.feature_vals.shape

# Default data model which implements a one class SVM to 
# detect novelties in typing samples
class RecogNoveltyDetector():

    # Initializes default values
    def __init__(self, ks_to_examine, feature_list):
        self.model = svm.OneClassSVM()
        self.ks_to_examine = ks_to_examine
        self.feature_list = feature_list

    # Training of the algorithm
    def train(self, train_data, params=None):
        rds_train = RecogDataSample()

        # Build the training set
        rds_train.set_data(train_data)
        rds_train.load_keystroke_list(selective_ks_list=self.ks_to_examine)
        rds_train.pull_features(self.feature_list)

        # If specific params exist, update the SVM
        if params:
            for attr, val in self.model.__dict__.iteritems():
                if attr in params:
                    self.model.__dict__[attr] = params[attr]

        # Train the system
        self.model.fit(rds_train.feature_vals)

        return 'Success!'



    # Will eventually be named train once data can be stored
    # For now will represent both training and testing of a model
    def challenge(self, test_data):
        # Build the test set
        rds_test = RecogDataSample()
        rds_test.set_data(test_data)
        rds_test.load_keystroke_list(selective_ks_list=self.ks_to_examine)
        rds_test.pull_features(self.feature_list)
        
        # Test the system
        prediction = self.model.predict(rds_test.feature_vals)

        bad = 0
        good = 0
        for item in prediction:
            if item == -1:
                bad += 1
            else:
                good += 1
        result = [bad, good]

        # Below is code to store the data as json in the db but currently
        # it is not possible to rebuild the model.
        """
        # Format the model as a dictionary and dump into json format
        model_dict = self.model.__dict__

        # $$ Need to make this code block for efficient and not hardcoded
        model_dict['support_vectors_'] = model_dict['support_vectors_'].tolist()
        model_dict['support_'] = model_dict['support_'].tolist()
        model_dict['label_'] = model_dict['label_'].tolist()
        model_dict['dual_coef_'] = model_dict['dual_coef_'].tolist()
        model_dict['class_weight_'] = model_dict['class_weight_'].tolist()
        model_dict['n_support_'] = model_dict['n_support_'].tolist()
        model_dict['_intercept_'] = model_dict['_intercept_'].tolist()
        model_dict['intercept_'] = model_dict['intercept_'].tolist()
        model_dict['probB_'] = model_dict['probB_'].tolist()
        model_dict['probA_'] = model_dict['probA_'].tolist()
        model_dict['class_weight_label_'] = model_dict['class_weight_label_'].tolist()

        # Dumps model into json format
        model_dump = json.dumps(model_dict)
        """
        return result
    """        
    def challenge(self, rds, ks_to_examine, feature_list, params=None):
        # Connect to the database
        try:
            conn = (DB INFO GOES HERE)
                )
        except:
            print "Cannot connect to the database"
        
        # Query the database for the current model
        cur = conn.cursor() 
        cur.execute('SELECT bio_model \
                     FROM recogmatch_biotemplate \
                     WHERE user_id=%s', 
                     (self.user_id,))
        model_dict = cur.fetchall() 
        conn.close()

        self.model.fit(rds.feature_vals)

        # $$ Need to make this code block for efficient and not hardcoded
        model_load = json.loads(model_dict[0][0])
        
        self.model['support_vectors_'] = np.array([model_load['support_vectors_']])
        self.model['support_'] = np.array([model_load['support_']])
        self.model['label_'] = np.array([model_load['label_']])
        self.model['dual_coef_'] = np.array([model_load['dual_coef_']])
        self.model['class_weight_'] = np.array([model_load['class_weight_']])
        self.model['n_support_'] = np.array([model_load['n_support_']])
        self.model['_intercept_'] = np.array([model_load['_intercept_']])
        self.model['intercept_'] = np.array([model_load['intercept_']])
        self.model['probB_'] = np.array([model_load['probB_']])
        self.model['probA_'] = np.array([model_load['probA_']])
        self.model['class_weight_label_'] = np.array([model_load['class_weight_label_']])

        for key, val in model_load.iteritems():
            if isinstance(val, unicode):
                val = str(val)
            if isinstance(val, np.ndarray):
                val = val[0]
            self.model.__dict__[key] = val
        
        self.model.train(ks_to_examine, feature_list, params)
        prediction = self.model.predict(rds.feature_vals)

        return prediction

class RecogDataModel():
    def __init__(self):
        self.observed_samples = np.array([])
        self.observed_digraphs = np.array([])
    
    def train_model(self, observed_samples, observed_digraphs): 
        # Creates numerical label for each observed keystroke
        def create_targets(ods):
            target_array = np.zeros((len(ods.ravel())), dtype='int64') #np.zeros(np.shape(ods.ravel()))
            counter = 0
            for i, val1 in enumerate(ods):
                target = np.in1d(self.observed_digraphs, val1)
                for j, val2 in enumerate(target):
                    if val2:
                        target_array[i] = j
            return target_array


        # Creates or appends digraphs observed for labeling purposes
        def update_observed_digraphs(ods):
            if np.shape(self.observed_digraphs) == (0,):
                temp_list = []
                for i, val in enumerate(ods):
                    if val not in temp_list:
                        temp_list.append(val)
                self.observed_digraphs = np.asarray(temp_list)
            else:
                temp = np.in1d(ods, self.observed_digraphs)
                for i, val in enumerate(temp):
                    if not val:
                        self.observed_digraphs = np.append(self.observed_digraphs, 
                                                           ods[i]) 

        def make_ellipses(gmm, ax):
            n = 0
            while n != gmm.n_components:
                v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
                u = w[0] / np.linalg.norm(w[0])
                angle = np.arctan2(u[1], u[0])
                angle = 180 * angle / np.pi  # convert to degrees
                v *= 9
                ell = mpl.patches.Ellipse(gmm.means_[0, :2], v[0], v[1],
                                          180 + angle, color='r')
                ell.set_clip_box(ax.bbox)
                ell.set_alpha(0.5)
                ax.add_artist(ell)
                n += 1
        
        for n, sample_set in enumerate(observed_samples):
            update_observed_digraphs(observed_digraphs[n])
            
            X_train = sample_set
            Y_train = create_targets(observed_digraphs[n])
            n_classes = len(np.unique(Y_train))
            
            classifiers = dict((covar_type, GMM(covariance_type=covar_type, 
                                n_components=n_classes,
                                init_params='wc', n_iter=200)) \
                                for covar_type in ['spherical', 'diag', \
                                'tied', 'full'])
            
            n_classifiers = len(classifiers)

            pl.figure(figsize=(3 * n_classifiers / 2, 6))
            pl.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
                               left=.01, right=.99)

            for index, (name, classifier) in enumerate(classifiers.iteritems()):
                temp_means = []
                for i in xrange(n_classes):
                    temp_mean = X_train[Y_train == i].mean(axis=0)
                    if np.isnan(temp_mean).any():
                        #print X_train[Y_train == i]
                        #print Y_train
                        #print i
                        #raw_input()
                        pass
                    else:
                        temp_means.append(temp_mean.round(decimals=3))
                classifier.means_ = np.array(temp_means)
                print np.shape(classifier.means_)
                
                # Train the parameters using the EM algorithm.
                classifier.fit(X_train)
                #print classifier.covars_          
                #print classifier.means_
                #print classifier.weights_
                #print classifier.converged_
                
                h = pl.subplot(2, n_classifiers / 2, index + 1)
                make_ellipses(classifier, h)
               
                # Plot the training data with circles
                pl.scatter(X_train[:, 0], X_train[:, 1], 0.8, color='b',
                            label="Training")

                y_train_pred = classifier.predict(X_train)
                train_accuracy = np.mean(y_train_pred.ravel())
                pl.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
                                transform=h.transAxes)

                pl.xticks(())
                pl.yticks(())
                pl.title(name)

            pl.legend(loc='lower right', prop=dict(size=12))

        fig_name = 'test' + str(n+1) + '.pdf'
        pl.savefig(fig_name)
"""
