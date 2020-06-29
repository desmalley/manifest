import my_ebay_lib as ebay
import pprint as pp
import numpy as np
#import pdb
'''
This code looks prices for lots of one item from liquidation.com
class version
you must have all of your manifests in a folder called 'manifests' in your working directory
you must also have a csv file called ebay_cache_lower.csv in your working directory
'''


def phone_rank(file_path):
    """
    in: filename
    out: dictionary of bestseller phones
    """
    ranks={}
    with open(file_path) as record:
      text=record.read()
      entries=text.split('#')#text split into entries
      entries.remove("")
      for entry in entries:
        lines=entry.splitlines()
        #print(lines)
        rank=lines[0]
        name=lines[1]
        ranks.update({name:rank})
      return ranks 

def strip_dollar_format(str_price):
    'in:dollar format, out: float'
    dig_punc_only=str_price.replace('$','')
    dig_only=dig_punc_only.replace(',','')
    fprice=float(dig_only)
    return fprice

#***************classes
class pallet:
    def __init__(self, df):
        """
        in: DataFrame with 'name':[None],'qty':[None],'price':[None],'date':[None],'url':[None]
        maybe purl and bid
        out: pallet object
        """
       
        try:
            self.purl=df.purl.iloc[0]
        except:
            self.purl=input('What is the url:  ')
        try:
            self.bid=df.bid.iloc[0]
        except:
            self.bid=input('What is the bid:  ')
        self.name=df.name.tolist()
        price_list_strings=df.price.tolist()
        price_list=[float(price) for price in price_list_strings]
        qty_list_strings=df.qty.tolist()
        qty_list=[float(qty) for qty in qty_list_strings]
        self.qty_tot=sum(qty_list)
        posts=zip(price_list,qty_list)
        self.gross=sum([price*qty for price,qty in posts])
        self.post_num=len(set(self.name))
        print(self.bid)
        print(type(self.bid))
        print(self.gross)
        print(type(self.gross))

        if isinstance(self.bid,str):  
            self.profit=self.gross-strip_dollar_format(self.bid)
        elif isinstance(self.bid,float): 
            self.profit=self.gross-self.bid 
        elif isinstance(self.bid,int): 
            self.profit=self.gross-self.bid
        elif isinstance(self.bid,np.integer): 
            self.profit=self.gross-self.bid
        else:
             self.profit=self.gross-self.bid 
        self.wage=self.profit/self.post_num
    def __str__(self):
        output_string='''
        purl:  {}
        bid:  {}
        gross:  {}
        qty_tot:  {}
        post_num:  {}
        profit:  {}
        wage:  {}
        '''.format(self.purl,self.bid,self.gross,self.qty_tot,self.post_num,self.profit,self.wage)
        return output_string    

#***************script
#url='https://www.bulq.com/detail/csaa182421/cell-phone-accessories-playtek-hifuture-fally/'
#bid=381
#pdb.set_trace() 
manifest_list=ebay.fetch_csv_data()
pallet_list=[]
for manifest in manifest_list:
    name_qty_df=ebay.manifest_csv_to_df(manifest)
#    pdb.set_trace() 
    master_df=ebay.find_prices(name_qty_df)
    print(master_df[['name','price']])
    pallet_obj=pallet(master_df)
    pallet_list.append(pallet_obj)
    print(pallet_obj)
#name_qty_df=ebay.manifest_csv_to_df('manifests/b3.csv')
#print(name_qty_df)
#master_df=ebay.find_prices(name_qty_df)
#print(master_df)
#pallet_obj=pallet(master_df)
#print(pallet_obj)
