
'''
This code looks prices for lots of one item from liquidation.com
class version
'''
#libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime

#selenium options to prevent detection
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


#***************functions

def manifest_csv_to_df(manifest_name):
    '''
    special csv name including suffix (not path) in, df out
    '''
    df=pd.read_csv("manifests/"+ manifest_name)
    #find name column
    if 'Product Name' in df:
        name_key='Product Name'
    elif 'Description' in df:
        name_key='Description'        
    elif 'Product' in df:
        name_key='Product'
    elif 'Model' in df:
        name_key='Model'
    elif 'NAME' in df:
        name_key='NAME'
    elif 'name' in df:
        name_key='name'        
    else:
        raise TypeError("Couldn't find a NAME column ")
    df=df.rename(columns={name_key: "name"})
    
    #find qty column
    if 'Qty' in df:
        qty_key='Qty'
    elif 'quantity' in df:
        qty_key='quantity'
    elif 'Quantity' in df:
        qty_key='Quantity'             
    else: #assume a qty of 1
        print("Couldn't find a QTY column...setting to one ")
        df['qty']=1
        qty_key='qty'
    df=df.rename(columns={qty_key: "qty"})
    df=df.dropna(subset =["name"])#drop any empy lines
    return df[['name','qty']]

def manifest_txt_to_df(manifest_name):
    '''
    l2: txt, each line has info for product, the name is the first item on the line before the $ symbol
    string in, df out
    '''
    manifest_path="manifests/"+ manifest_name
    f = open(manifest_path, "r")
    data_text=f.read()
    f.close()
    lines=data_text.split("\n")#[2:-1] don't include leading empty space and column titles
    try:
        lines.remove('')#get rid of empty lines
    except:
        pass #do nothing
    try:
        lines.remove('Product	Quantity	Retail Price	Total Retail Price	UPC	Notes')#get comlumns names
    except:
        pass #do nothing
    pnames=[]
    qtys=[]
    for line in lines:
        elems=line.split("$")
        name_and_qty=elems[0]
        name,qty=strip_trailing_digits(name_and_qty)
        pnames.append(name)
        qtys.append(qty)
        df={'name':pnames,'qty':qtys}    
    return df
    

def strip_trailing_digits(mixed_string):
    '''
    in: string with trailing digits
    out: tuple (string w/o digits, integer digits)
    '''
    if not isinstance(mixed_string, str):
        raise TypeError("strip_trailing_digits() only accepts strings, Silly!")
    mixed_string=mixed_string.strip() #elim trailing whitespace
    inverted_mixed_string=mixed_string[::-1]
    i=0
    inverted_qty_string=""
    if mixed_string[-1].isdigit(): #check last char to see if digit
        while inverted_mixed_string[i].isdigit():
            inverted_qty_string+=inverted_mixed_string[i]
            i+=1
        qty_string=inverted_qty_string[::-1]
        qty=int(qty_string)
        name=mixed_string[:-len(qty_string)]
        return name,qty
    else:
        raise TypeError("No quantity found in string, Silly!")




#fetches just first ebay price
def fetch_ebay_price(product_name):
    '''
    in: string product name
    out: tuple float, string  price,url
    '''
    if not isinstance(product_name,str):
        print('Your input is not a string name, instead you input {}'.format(product_name))
        return 0,'no url'
    elif not product_name:
        print('Your entered an empty string as a product name, Silly!')
        return 0,'no url'
    else: #normal operation
        browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
        browser.get('https://www.ebay.com/')
        searchbar=browser.find_element_by_id("gh-ac")
        searchbar.send_keys(product_name)
        searchbar.send_keys(Keys.ENTER)
        url=browser.current_url

        try:
            price=browser.find_element_by_class_name("s-item__price")
            tprice=price.text
            print("EBAY PRICE for {} IS:{}".format(product_name,tprice))
            first_tprice_elem=tprice.split(" ")[0]
            try:
                dig_punc_only=first_tprice_elem.replace('$','')
                dig_only=dig_punc_only.replace(',','')
                fprice=float(dig_only)
            except: #not a valid price example, Best Buy click to see price
                print("not a valid price")
                fprice=0
        except:  #for example selenium.common.exceptions.NoSuchElementException:  thrown when 'no exact matches found'
            fprice=0
        #print(fprices)    
        browser.quit()
        try:
            return fprice,url
        except:
            return float(0),url 


def update_cache(new_df):
    cache_df=pd.read_csv('ebay_cache_lower.csv')
    cache_df=cache_df.append(new_df, ignore_index=True)
    cache_df.to_csv('ebay_cache_lower.csv',index=False)


def find_prices(name_qty_df):
    '''
    in: data frame with two columns: 'name' and 'qty'
    out: data frame with cols: 'name' 'qty' 'price' 'url' 'date'
    '''
    name_qty_dict=dict(zip(name_qty_df.name.to_list(),name_qty_df.qty.to_list()))
    name_list=name_qty_df["name"].to_list()
    old_name=""
    old_price=0
    old_url=''
    cache_df=pd.read_csv('ebay_cache_lower.csv')
    master_df=pd.DataFrame({'name':[None],'qty':[None],'price':[None],'date':[None],'url':[None]})
    for name,qty in name_qty_dict.items():
        print("PRODUCT NAME: {}".format(name))
        if name:
            if name==old_name: #Did we just looked up this price?
                print("(Repeat Price)")
                price=old_price
                url=old_url
            elif cache_df['name'].str.contains(name,regex=False).any():#Is this price in the cache?
                print("(Cached Price)")
                row=cache_df[cache_df.name==name]
                price=row.price.values[0]
                url=row.url.values[0]
            else: #If not, let's look up the price on ebay
                print("Fetch Ebay Price")
                price,url=fetch_ebay_price(name)
                cache_entry_df=pd.DataFrame({'name':[name],'price':[price],'date':[datetime.datetime.now()],'url':[url]})
                update_cache(cache_entry_df)
            session_df=pd.DataFrame({'name':[name], 'qty':[qty],'price':[price], 'date':[datetime.datetime.now()],'url':[url]})    
            master_df=master_df.append(session_df, ignore_index=True)
        else:
            print('no name')
            price=0
        old_name=name
        old_url=url
        old_price=price
        master_df=master_df.fillna('')
    return master_df



#***************classes


class pallet:
    def __init__(self, pallet_url, bid, manifest):
        """
        url: string
        bid: float
        manifest: string of manifest filename and path including suffix
        """
        self.pallet_url=pallet_url
        self.bid=bid
        self.data=pd.DataFrame({'NAME':'Session Start', 'PRICE':0, 'QTY':0,'URL':'www.google.com'})
        self.qty_tot=0
        self.post_num=0    
        self.names=''
        self.prices=[]
        self.gross=0
        self.profit=0
        
    def load_data(self):
        df=manifest_to_df(manifest)
        self.names=df.names.tolist()
        self.prices,self.df=ebay.find_prices(self.names) #should return list of floats
        self.gross=sum(self.prices)
        self.qty_tot=len(self.prices)
        self.post_num=len(set(self.names))
        self.profit=self.gross-self.bid
           

#***************script
#url='https://www.bulq.com/detail/csaa182421/cell-phone-accessories-playtek-hifuture-fally/'
#bid=381

manifest='bravia.csv'
name_qty_df=manifest_csv_to_df(manifest)
print(name_qty_df)
master_df=find_prices(name_qty_df)
print(master_df)





#***************depricated functions****************
def b1_read(manifest_path):
    '''
    b1:  csv "Product Name" column, no quantity (just repeated name)
    string in, df out
    '''
    man_df= pd.read_csv('manifests/b3.csv')
    man_df=df.fillna(" ")    
    pnames=man_df["Product Name"].to_list()
    qtys=[1]*len(pnames)
    df = {'name':pnames, 'qty':qtys}
    return df
    
def l1_read(manifest_path):
    '''
    l1:  csv, columns= Description, Qty (could be in a different order)
    string in, df out
    '''
    data = pd.read_csv(manifest_path)
    data=data.rename(columns={"Description": "name","Quantity":"qty"})
    df = data[['name', 'qty']].copy()    
    return df
    
def l2_read(manifest_path):
    '''
    l2: txt, each line has info for product, the name is the first item on the line before the $ symbol
    string in, df out
    '''
    f = open(manifest_path, "r")
    data_text=f.read()
    f.close()
    lines=data_text.split("\n")[2:-1] #don't include leading empty space and column titles
    try:
        lines.remove('')#get rid of empty lines
    except:
        pass #do nothing
    pnames=[]
    qtys=[]
    for line in lines:
        elems=line.split("$")
        print(elems)
        name_and_qty=elems[0]
        name,qty=strip_trailing_digits(name_and_qty)
        print(name)
        pnames.append(name)
        qtys.append(qty)
        df={'name':pnames,'qty':qtys}    
    return df

