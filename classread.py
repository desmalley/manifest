import my_ebay_lib as ebay
#import pdb
'''
This code looks prices for lots of one item from liquidation.com
class version
you must have all of your manifests in a folder called 'manifests' in your working directory
you must also have a csv file called ebay_cache_lower.csv in your working directory
'''

#***************classes
class pallet:
    def __init__(self, df):
        """
        in: DataFrame with 'name':[None],'qty':[None],'price':[None],'date':[None],'url':[None]
        maybe purl and bid
        out: pallet object
        """
        try:
            self.purl=df.purl[0]
        except:
            self.purl=input('What is the url:  ')
        try:
            self.bid=df.bid[0]
        except:
            self.bid=input('What is the bid:  ')
        self.name=df.name.tolist()
        price_list_strings=df.price.tolist()
        price_list=[float(price) for price in price_list_strings]
        qty_list_strings=df.qty.tolist()
        qty_list=[float(qty) for qty in qty_list_strings]
        self.qty_tot=sum(qty_list)
        self.gross=sum([price*qty for price in price_list for qty in qty_list])
        self.post_num=len(set(self.name))
        self.profit=float(self.gross)-float(self.bid)
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

#manifest_list=ebay.fetch_csv_data()
#pallet_list=[]
#for manifest in manifest_list:
#    name_qty_df=ebay.manifest_csv_to_df(manifest)
#    master_df=ebay.find_prices(name_qty_df)
#    print(master_df)
#    pallet_list.append(pallet(master_df))
#print(pallet_list)    

manifest='manifests/iphone6.csv'
name_qty_df=ebay.manifest_csv_to_df(manifest)
master_df=ebay.find_prices(name_qty_df)
p1=pallet(master_df)
print(p1)