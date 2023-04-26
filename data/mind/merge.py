import pandas as pd

df1 = pd.read_csv('MINDlarge_train/behaviors.tsv', sep = '\t', header = None, names = ['impression_id', 'user_id', 'time', 'history', 'impressions'])
df2 = pd.read_csv('MINDlarge_dev/behaviors.tsv', sep = '\t', header = None, names = ['impression_id', 'user_id', 'time', 'history', 'impressions'])

df = pd.concat([df1, df2])
df.to_csv('behaviors.tsv', sep = '\t', index = None, header = None)
