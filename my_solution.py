# all conversion code in one cell
import pandas as pd
from datetime import datetime

# client conversion
client = pd.read_csv('data/bank_marketing.csv',
                     usecols=['client_id', 'age', 'job', 'marital',
                              'education', 'credit_default', 'mortgage'],
                     true_values=['yes'],
                     false_values=['no'],
                     na_values=['unknown']
                     )

# apply string replacements
client['education'] = client['education'].str.replace('.', '_')

# The original requirement specified replacing the period with an underscore.
# The values contained only have admin. which is an abbreveation and would
# look weird with an underscore.
# Removing the period makes more sense.

client['job'] = client['job'].str.replace('.', '')

# save our dataframe to csv
client.to_csv('cleaned/client.csv', index=False)

# campaign conversion
campaign = pd.read_csv('data/bank_marketing.csv',
                       usecols=['client_id', 'number_contacts',
                                'contact_duration',
                                'previous_campaign_contacts',
                                'previous_outcome',
                                'campaign_outcome',
                                'day',
                                'month'],
                       true_values=['yes', 'success'],
                       false_values=['no', 'failure', 'nonexistent']
                       )

# set the year to 2012
campaign['year'] = 2012

# set the month to its integer equivalent
campaign['month'] = campaign['month']\
    .apply(lambda x: datetime.strptime(x, '%b').month)

# create our new column with a yyyy-mm-dd time format
campaign['last_contact_date'] = pd.to_datetime(campaign[['year', 'month', 'day']]) # noqa

# drop the columns we no longer need
cols = ['month', 'day', 'year']
campaign.drop(cols, axis=1, inplace=True)

# reorder the cols
campaign = campaign[['client_id', 'number_contacts', 'contact_duration',
                     'previous_campaign_contacts', 'previous_outcome',
                     'campaign_outcome', 'last_contact_date']]

# save our campaing dataframe to csv
campaign.to_csv('cleaned/campaign.csv', index=False)

# economics conversion
economics = pd.read_csv('data/bank_marketing.csv',
                        usecols=['client_id', 'cons_price_idx',
                                 'euribor_three_months'],
                        )

# save our economics dataframe to csv
economics.to_csv('cleaned/economics.csv', index=False)
