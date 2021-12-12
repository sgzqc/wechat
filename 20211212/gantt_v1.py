import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pandas import Timestamp

##### DATA #####
data = {'Task': {0: 'TSK M',
                 1: 'TSK N',
                 2: 'TSK L',
                 3: 'TSK K',
                 4: 'TSK J',
                 5: 'TSK H',
                 6: 'TSK I',
                 7: 'TSK G',
                 8: 'TSK F',
                 9: 'TSK E',
                 10: 'TSK D',
                 11: 'TSK C',
                 12: 'TSK B',
                 13: 'TSK A'},

        'Department': {0: 'IT',
                       1: 'MKT',
                       2: 'ENG',
                       3: 'PROD',
                       4: 'PROD',
                       5: 'FIN',
                       6: 'MKT',
                       7: 'FIN',
                       8: 'MKT',
                       9: 'ENG',
                       10: 'FIN',
                       11: 'IT',
                       12: 'MKT',
                       13: 'MKT'},

        'Start': {0: Timestamp('2022-03-17 00:00:00'),
                  1: Timestamp('2022-03-17 00:00:00'),
                  2: Timestamp('2022-03-10 00:00:00'),
                  3: Timestamp('2022-03-09 00:00:00'),
                  4: Timestamp('2022-03-04 00:00:00'),
                  5: Timestamp('2022-02-28 00:00:00'),
                  6: Timestamp('2022-02-28 00:00:00'),
                  7: Timestamp('2022-02-27 00:00:00'),
                  8: Timestamp('2022-02-26 00:00:00'),
                  9: Timestamp('2022-02-23 00:00:00'),
                  10: Timestamp('2022-02-22 00:00:00'),
                  11: Timestamp('2022-02-21 00:00:00'),
                  12: Timestamp('2022-02-19 00:00:00'),
                  13: Timestamp('2022-02-15 00:00:00')},

        'End': {0: Timestamp('2022-03-20 00:00:00'),
                1: Timestamp('2022-03-19 00:00:00'),
                2: Timestamp('2022-03-13 00:00:00'),
                3: Timestamp('2022-03-13 00:00:00'),
                4: Timestamp('2022-03-17 00:00:00'),
                5: Timestamp('2022-03-02 00:00:00'),
                6: Timestamp('2022-03-05 00:00:00'),
                7: Timestamp('2022-03-03 00:00:00'),
                8: Timestamp('2022-02-27 00:00:00'),
                9: Timestamp('2022-03-09 00:00:00'),
                10: Timestamp('2022-03-01 00:00:00'),
                11: Timestamp('2022-03-03 00:00:00'),
                12: Timestamp('2022-02-24 00:00:00'),
                13: Timestamp('2022-02-20 00:00:00')},

        'Completion': {0: 0.0,
                       1: 0.0,
                       2: 0.0,
                       3: 0.0,
                       4: 0.0,
                       5: 1.0,
                       6: 0.4,
                       7: 0.7,
                       8: 1.0,
                       9: 0.5,
                       10: 1.0,
                       11: 0.9,
                       12: 1.0,
                       13: 1.0}}

##### DATA PREP #####
df = pd.DataFrame(data)

# project start date
proj_start = df.Start.min()

# number of days from project start to task start
df['start_num'] = (df.Start - proj_start).dt.days

# number of days from project start to end of tasks
df['end_num'] = (df.End - proj_start).dt.days

# days between start and end of each task
df['days_start_to_end'] = df.end_num - df.start_num


fig, ax = plt.subplots(1, figsize=(16,6))
ax.barh(df.Task, df.days_start_to_end, left=df.start_num)
plt.show()
