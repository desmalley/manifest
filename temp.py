
import pandas as pd

def manifest_csv_to_df(manifest_name):
    '''
    in: csv.  You should add columns for pallet URL and current bid
    out: dataframe with names and quantities
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
    if not 'bid' in df.columns or not 'purl' in df.columns:
        print("Couldn't find Purl or bid columns...leaving them out")
        df=df[['name','qty']]
        df=df.fillna("")
        return df
    else:    
        df=df[['name','qty','bid','purl']]
        df=df.fillna("")
        return df

