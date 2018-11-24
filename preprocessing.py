import numpy as np 
import pandas as pd
import argparse

"""
Script for pre-proceeding.

Astro-ph only


"""

class AstroPhData:
    """
    Object for astro-ph data
    """
    # assign label and remove those with sub-categories..
    target_name_dict = { 'astro-ph.GA' : 0,
                        'astro-ph.SR' : 1,
                        'astro-ph.IM' : 2,
                        'astro-ph.EP' : 3,
                        'astro-ph.HE' : 4,
                        'astro-ph.CO' : 5
                    }
    def __init__(self, filename):
        self.filename = filename
        store = pd.HDFStore(self.filename, 'r')
        self.df = store['df']
        store.close()

    def preprocess(self):
        """preprocess:

            select the category as label based on FIRST-OCCURENCE in astro-ph
        """
        
        # create a new column.
        self.df['label'] = None # not sure if this is the best way

        for i, rows in self.df.iterrows():
            cat = self.df['categories'].at[i]
            if any(['astro-ph.' in c for c in cat]):
                for j in range(len(cat)):
                    if cat[j] in self.target_name_dict.keys():
                        label = self.target_name_dict[cat[j]]
        #                print(i, label, cat)
                        self.df['label'].at[i] = int(label)
                        break
            else:
                self.df.drop(i, inplace=True)
                
        # https://stackoverflow.com/questions/28885073/reindexing-after-pandas-drop-duplicates
        self.df.reset_index(drop=True, inplace=True) # reset the index after dropping

        # set label to integer
        self.df['label'] = pd.to_numeric(self.df['label'], downcast='integer')

    def output(self):
        self.outputfile = self.filename.split('.h5')[0] + "_p.h5"
        store = pd.HDFStore(self.outputfile, 'w')
        store['df'] = self.df
        store.close()
        print("# finished output()")


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('h5file', type=str, help="input file")
    args = parser.parse_args()

    data = AstroPhData(args.h5file)
    data.preprocess()
    data.output()
    