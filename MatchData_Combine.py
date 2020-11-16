import pandas as pd 
a = pd.DataFrame()
b = pd.DataFrame()
for i in range(2000,2021):
    print(i)
    df = pd.read_csv('DS250_SeasonData/'+str(i)+'.csv' , error_bad_lines=False)
    df['Season']=i
    b = pd.concat([a,df])
    a = b
a.to_csv('MatchData.csv')

