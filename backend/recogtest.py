# ----------------------------------------------------------------------------
# --- Author:   Adam Gribble                                               ---
# --- Title:    recogtest.py                                               ---
# --- Date:     August 20, 2012                                            ---
# --- Summary:  Python module for creating a summary report on the         ---
# --- RecogType system.                                                    ---

from recogtype_backend import RecogDataSample, RecogNoveltyDetector

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.ticker as tkr

import numpy as np

import psycopg2
import psycopg2.extras

from datetime import date, timedelta
from math import ceil
from random import choice

class RecogSummaryReport():
    def __init__(self):
        self.raw_sample_data = []

        self.user_stats = {}
        self.sample_stats = {}
        self.algo_stats = {}

        self.complete = {
                            'tier 0': 0,
                            'tier 1': 0,
                            'tier 2': 0,
                            'tier 3': 0,
                            'tier 4': 0,
                        }
    
    def get_user_stats(self):
        # Initialize list local variables
        today = date.today()
        age_range_dict = {
                            '18 to 24': 0,
                            '25 to 34': 0,
                            '35 to 44': 0,
                            '45 to 54': 0,
                            '55 to 64': 0,
                            '65+': 0,
                        }
        user_stats = {
                        'dob': {},
                        'sex': {},
                        'handed': {},
                        'daily_usage': {},
                        'country': {},
                        'language': {},
                    }

        # Connect to the database
        try:
            conn = psycopg2.connect("dbname='recogtype' user='postgres' \
                                    host='localhost' password='14elbbirg14'")
        except:
            print "Unable to connect to the database"

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Run query to get raw user data
        cur.execute("""SELECT dob, sex, handed, daily_usage, country, language \
                       FROM profiles_profile""")
        user_results = cur.fetchall()
        conn.close()

        user_count = len(user_results)
        user_inact = 0

        # Loop through query results to pull data
        # Some users have signed up without creating a profile however
        for row in user_results:
            # If the profile has not been completed, user is deemed inactive
            if '' in row.values() or None in row.values():
                user_inact += 1
            else:
                for key, val in row.iteritems():
                    if val in user_stats[key]:
                        user_stats[key][val] += 1
                    else:
                        user_stats[key][val] = 1

        # Creates user statistics
        for outter_key, outter_val in user_stats.iteritems():
            # DOB is a special case
            if outter_key == 'dob':
                for key, val in outter_val.iteritems():
                    # Try/except for February 29 when not a leap year
                    try:
                        birthday = key.replace(year=today.year)
                    except ValueError:
                        birthday = key.replace(year=today.year, day=born.day-1)
                    
                    # Calculate user's age
                    if birthday > today:
                        age = today.year - key.year - 1
                    else:
                        age = today.year - key.year

                    # Calculate user's age range
                    if age in range(18, 25):
                        age_range_dict['18 to 24'] += 1
                    elif age in range(25, 35):
                        age_range_dict['25 to 34'] += 1
                    elif age in range(35, 45):
                        age_range_dict['35 to 44'] += 1
                    elif age in range(45, 55):
                        age_range_dict['45 to 54'] += 1
                    elif age in range(55, 65):
                        age_range_dict['55 to 64'] += 1
                    elif age >= 65:
                        age_range_dict['65+'] += 1
                    else:
                        print birthday, "Underage!"
                
                for key, val in age_range_dict.iteritems():

                    if outter_key in self.user_stats:
                        self.user_stats[outter_key][key] = int(round(float(val) \
                                                  / (float(user_count) \
                                                  - float(user_inact)) \
                                                  * 100))
                    else:
                        self.user_stats[outter_key] = { key: int(round(float(val) \
                                                  / (float(user_count) \
                                                  - float(user_inact)) \
                                                  * 100)) }
            else:
                for key, val in outter_val.iteritems():
                    if not key:
                        key = 'N/A'

                    if outter_key in self.user_stats:
                        self.user_stats[outter_key][key] = int(round(float(val) \
                                                  / (float(user_count) \
                                                  - float(user_inact)) \
                                                  * 100))
                    else:
                        self.user_stats[outter_key] = { key: int(round(float(val) \
                                                  / (float(user_count) \
                                                  - float(user_inact)) \
                                                  * 100)) } 

        # Number of users who have signed up
        self.complete['tier 0'] = user_count

        # Number of users who have completed their profile
        self.complete['tier 1'] = user_count - user_inact

        return self.complete

    def get_sample_stats(self):
        # Initialize local dictionaries
        user_dict = {}
        os_dict = {}
        browser_dict = {}
        keyboard_dict = {}

        # Connect to the database
        try:
            conn = psycopg2.connect("dbname='recogtype' user='postgres' \
                                    host='localhost' password='14elbbirg14'")
        except:
            print "Unable to connect to the database"

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Run query to get raw sample data
        cur.execute("""SELECT * FROM recogmatch_rawsample""")
        self.raw_sample_data = cur.fetchall()

        # Run query to get number of possible training challenges
        cur.execute("""SELECT COUNT(id) \
                       FROM recogmatch_challenge \
                       WHERE challenge_use = 't' """)
        challenge_count = cur.fetchall()
        conn.close()

        # Loop through data and pull total numbers
        for sample in self.raw_sample_data:
            # Counts unique users who have submitted data
            if sample['user_id'] in user_dict:
                user_dict[sample['user_id']] += 1
            else:
                user_dict[sample['user_id']] = 1

            # Counts number of each os used
            if sample['os'] in os_dict:
                os_dict[sample['os']] += 1
            else:
                os_dict[sample['os']] = 1

            # Counts number of each browser used
            if sample['browser'] in browser_dict:
                browser_dict[sample['browser']] += 1
            else:
                browser_dict[sample['browser']] = 1

            # Counts number of each keyboard used
            if sample['keyboard'] in keyboard_dict:
                keyboard_dict[sample['keyboard']] += 1
            else:
                keyboard_dict[sample['keyboard']] = 1

        # Sets number of samples
        num_samples = len(self.raw_sample_data)

        # Sets number of users who have completed their biometric template
        for key, val in user_dict.iteritems():
            percent_complete = int(float(val) / challenge_count[0]['count'] * 100)
            
            # Number of users who have attempted at least one training challenge 
            self.complete['tier 2'] += 1

            # Number of users who have completed training
            if percent_complete > 66:
                self.complete['tier 3'] += 1
            
        # Sets statistics for each os, browser and keyboard used to give samples
        for key, val in os_dict.iteritems():
            self.sample_stats['os_' + key] = str(int(round(float(val)/ float(num_samples) * 100))) + '%'
        for key, val in browser_dict.iteritems():
            self.sample_stats['browser_' + key] = str(int(round(float(val)/ float(num_samples) * 100))) + '%'
        for key, val in keyboard_dict.iteritems():
            self.sample_stats['keyboard_' + key] = str(int(round(float(val)/ float(num_samples) * 100))) + '%'

        return self.sample_stats

    # Method to collect statistics for backend recognition algorithm
    def get_algorithm_stats(self):
        # Settings for testing algorithm
        ks_list_options = ('first letters','second letters',
                       'third letters','ending letters',
                       'common digraphs','common trigraphs',
                       'common doubles','common 2l words',
                       'common 3l words','common 4l words',
                       'most common words')
        feature_list = ['dwell', 'interval', 'latency', 'up2up', 'flight']
        params = {
                'nu': 0.1,
                #'gamma': 0.1,
                'kernel': 'linear'
             }

        # Initialize local variables
        train_chlgs = {}
        test_chlgs = {}
        raw_data_dict = {}
        user_id_list = []

        # Connect to the database
        try:
            conn = psycopg2.connect("dbname='recogtype' user='postgres' \
                                    host='localhost' password='14elbbirg14'")
        except:
            print "Unable to connect to the database"

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Run query to get ids of challenges
        cur.execute("""SELECT id, challenge_type, challenge_use \
                       FROM recogmatch_challenge""")

        challenges = cur.fetchall()
        cur.close()

        # Divide challenges into train and test, fixed and variable
        for challenge in challenges:
            if challenge['challenge_use'] == 't':
                train_chlgs[challenge['id']] = [
                                                    challenge['challenge_type'],
                                                    challenge['challenge_use'],
                                               ]
            else:
                test_chlgs[challenge['id']] = [
                                                    challenge['challenge_type'],
                                                    challenge['challenge_use'],
                                              ]

        # Creates a dictionary of users and their training/test data
        for sample in self.raw_sample_data:
            user_id = sample['user_id']
            data = sample['data']
            challenge_id = sample['challenge_id_id']

            # If user has not been encountered
            if user_id not in raw_data_dict:
                # If challenge is for training
                if challenge_id in train_chlgs:
                    raw_data_dict[user_id] = { 
                                                'training': [data,],
                                                'testing': [],
                                             }
                else:
                    raw_data_dict[user_id] = { 
                                                'training': [],
                                                'testing': [data,],
                                             }

                    # Adds unique id to list of completed profiles
                    if user_id not in user_id_list:
                        user_id_list.append(user_id)
            else:
                # If challenge is for training
                if challenge_id in train_chlgs:
                    raw_data_dict[user_id]['training'].append(data)
                else:
                    raw_data_dict[user_id]['testing'].append(data)

                    # Adds unique id to list of completed profiles
                    if user_id not in user_id_list:
                        user_id_list.append(user_id)

        # For each user in raw_data_dict, run their data against the system as genuine
        for gen_id, gen_data in raw_data_dict.iteritems(): 
            # Initialize the novelty detector
            rnd = RecogNoveltyDetector(ks_list_options, feature_list)

            # If user has both trained and tested the system
            if gen_data['testing']:

                # Initialize the user entry in the algo_stats dictionary as a list
                self.algo_stats[gen_id] = []

                # Choose a random id to represent impostor
                impostor = choice(user_id_list)

                # Train the NoveltyDetector
                rnd.train(gen_data['training'], params)

                # For each test sample belonging to the user
                for test_sample in gen_data['testing']:

                    # Challenge the system with the test sample
                    result = rnd.challenge(test_sample)

                    # Calculate percentage of passing features
                    if result[1] != 0:
                        score = int(ceil(float(result[1]) / (result[0] + result[1]) * 100))
                    else:
                        score = 0

                    # Record testing results of both genuine and impostor 
                    self.algo_stats[gen_id].append(score)
                
                # Number of users who have completed at least 1 testing challenge
                self.complete['tier 4'] += 1

            else:
                    print "Didn't test!"


        return self.algo_stats
    
    # Methods to create visual diagrams and reports from data collected

    # Create a visual of recruitment dynamics
    def create_recruitment_report(self):
        # Connect to the database
        try:
            conn = psycopg2.connect("dbname='recogtype' user='postgres' \
                                    host='localhost' password='14elbbirg14'")
        except:
            print "Unable to connect to the database"

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Run query to get ids of challenges
        cur.execute("""SELECT username, last_login, date_joined \
                       FROM auth_user""")

        results = cur.fetchall()
        cur.close()

        # Initialize data structures
        deltas = ()
        dates_joined = {}
        date_range = []
        value_range = ()

        # Calculate active days and date joined for each user
        for row in results:
            date_joined = row['date_joined'].date()
            temp_delta = row['last_login'] - row['date_joined']

            # Sometimes temp_delta can be -1
            if temp_delta.days < 0:
                deltas += (0,)
            else:
                deltas += (temp_delta.days,)

            # If the date joined has already been represented
            if date_joined in dates_joined:
                dates_joined[date_joined] += 1
            else:
                dates_joined[date_joined] = 1

        # Create a sorted time frame of users signed up
        sorted_keys = dates_joined.keys()
        sorted_keys.sort()
 
        # Create a range of unique delta spans
        uniq_deltas = list(set(deltas))
        uniq_deltas.sort()

        # Time delta between first signup and last
        span_delta = sorted_keys[-1] - sorted_keys[0]
        temp_day = timedelta(days=0)

        # Counts number of users who signed up on each day
        for x in range(temp_day.days, span_delta.days):
            current_date = sorted_keys[0] + timedelta(days=x)
            date_range.append(current_date)

            if current_date in sorted_keys:
                value_range += (dates_joined[current_date],)
            else:
                value_range += (0,)

        # Sort the date range
        date_range.sort()

        # Set figure dimensions
        fig1 = plt.figure()
        fig2 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax2 = fig2.add_subplot(111)

        # Initialize fig1
        months = mdates.MonthLocator()
        days = mdates.DayLocator()
        months_fmt = mdates.DateFormatter('%b \'%y')

        # Initialize figure 2
        multiple = tkr.MultipleLocator(10)

        # Plot subplot 1 and update
        ax1.plot(date_range, value_range, '-')

        ax1.spines['right'].set_color('none')
        ax1.spines['top'].set_color('none')
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')

        ax1.xaxis.set_major_locator(months)
        ax1.xaxis.set_major_formatter(months_fmt)
        ax1.xaxis.set_minor_locator(days)

        #datemin = date(date_range[0].month, 1, 1)
        #datemax = date(date_range[-1].month+1, 1, 1)
        #ax1.set_xlim(datemin, datemax)
        ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        fig1.autofmt_xdate()

        # Plot subplot 2 and update
        N, bins, patches = ax2.hist(deltas, range(0, uniq_deltas[-1]+1))

        ax2.tick_params(axis='both', pad=8)
        ax2.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')
        ax2.xaxis.set_ticks_position('bottom')
        ax2.yaxis.set_ticks_position('left')
        ax2.xaxis.set_major_locator(multiple)
        ax2.set_xlim(-1, uniq_deltas[-1]+1)

        # Add titles to subplot 1
        ax1.set_xlabel('Date Registered')
        ax1.set_ylabel('# Of Users')
        ax1.set_title('Dynamics of Recruitment')
        
        # Add titles to subplot 2
        ax2.set_xlabel('# of Days Active')
        ax2.set_ylabel('# of Users')
        ax2.set_title('Active Span Among Users')

        fig_name1 = 'reports/' + 'recruitment.pdf'
        fig_name2 = 'reports/' + 'days_active.pdf'
        fig1.savefig(fig_name1)
        fig2.savefig(fig_name2)

    # Create a visual depiction of user life cycle
    def create_life_cycle(self):
        # Set figure dimensions
        fig = plt.figure()
        ax = fig.add_subplot(111)
        N = len(self.complete)
        M = 20
        width = 0.5
        yind = np.arange(0,M,1)
        xind = np.arange(N)
        title = 'User Life Cycle \"Drop-offs\"'
    
        bars = ()
        labels = ()

        # Create a sorted list of dictionary keys
        sorted_keys = self.complete.keys()
        sorted_keys.sort()

        # Order the bars and associated labels
        for item in sorted_keys:
            bars += (self.complete[item],)
            labels += (item.title(),)

        # Graph the data
        bars = ax.bar(xind, bars, width, color='r', align='center') 
        ax.set_ylabel('# of Users')
        ax.set_xlabel('Life Cycle Tier Completed')
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_xticklabels(labels)

        fig_name = 'reports/' + 'life_cycle.pdf'
        plt.savefig(fig_name)
        
    # Create a bar graph from general sample data
    def create_bar_graph(self, report_type, metric):
   
        # Set figure dimensions
        fig = plt.figure()
        ax = fig.add_subplot(111)

        if report_type == 'user_stats':
            N = len(self.user_stats[metric])
            M = 105
            width = 0.5
            yind = np.arange(0,M,5)
            xind = np.arange(N)
            title = metric.replace('_', ' ').title()
        
            bars = ()
            labels = ()

            # Create a sorted list of dictionary keys
            sorted_keys = self.user_stats[metric].keys()
            sorted_keys.sort()

            for item in sorted_keys:
                item_val = self.user_stats[metric][item]
                # If attribute doesn't apply to any users in the system
                if item_val != 0:
                    if '<' in item:
                        labels = (item,) + labels
                        bars = (item_val,) + bars
                    else:
                        labels += (item,)
                        bars += (item_val,)

            bars = ax.bar(xind, bars, width, color='b', align='center') 
            ax.set_ylabel('% of Users')
            ax.set_xlabel('Hours a Day')
            ax.set_title(title)
            ax.set_yticks(yind)
            ax.set_xticks(xind)
            ax.set_xticklabels(labels)
 
        fig_name = 'reports/' + title + '.pdf'
        plt.savefig(fig_name)
