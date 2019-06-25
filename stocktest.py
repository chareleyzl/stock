stock = pd.read_csv('E:\\data\\stock_data\\reports\\sh600196.csv',  index_col=0)
round(stock.loc[stock['REPORTDATE'].apply(lambda x:x.split('-')[0]+x.split('-')[1])=='201709'][:1]['SJL']/10000,2)

# 读取已生成的excel
mg = pd.read_csv('E:\\stock\\rjhlw10.csv', header=0, index_col=0, encoding='utf8')
# 相关性分析
# 业绩增长与平均roe的关联(结果表明，股价与近期的roe有一定关联，与均值无关联)
mg['roe_mean'] = mg[['16roe','17roe']].apply(lambda x: x.mean(), axis=1)
mg[['17PriceX','16PriceX','17ReportX','16ReportX','17roe','16roe']].corr()

# 总体上涨情况
mg[['17PriceX', '16PriceX','17roe','16roe']].describe()
mg[['17PriceX', '17ReportX']].corr()

# 业绩低增长的上涨情况2017
mg[['17PriceX','17roe']][mg['17ReportX']<4].describe()
# 业绩低增长的上涨情况2016
mg[['16PriceX','16roe']][mg['16ReportX']<4].describe()

# 业绩中等增长的上涨情况2017
mg[['17PriceX','17roe']][(mg['17ReportX']>4) & (mg1['17ReportX']<10)].describe()
# 业绩中等增长的上涨情况2016
mg[['16PriceX','16roe']][(mg['16ReportX']>4) & (mg1['16ReportX']<10)].describe()

# 业绩高增长的上涨情况2017
mg[['17PriceX','17roe']][mg['17ReportX']>10].describe()
# 业绩高增长的上涨情况2016
mg[['16PriceX','16roe']][mg['16ReportX']>10].describe()

# 10年业绩成长>10倍，2017净利润>10亿的公司
mgh = mg[(mg['17ReportX']>10) & (mg['17net']>100000)].sort_values(by = ['17ReportX'],ascending = False )
mgh.to_csv('C:\\Users\\Administrator\\Desktop\\all_high.csv', mode='w')

# 获取恒瑞复兴平安10年的净利润和roe，以及比亚迪6年的 stock[['reportdate','roeweighted','parentnetprofit']]
import pandas as pd
#复星
filenames1 = 'E:\\data\\stock_data\\reports\\sh600196.csv'
stock1 = pd.read_csv(filenames1)
df1 = stock1[stock1['reportdate'].apply(lambda x:x.split('-')[1]) == '12'][['reportdate','parentnetprofit','roeweighted']]
df1['parentnetprofit']=df1['parentnetprofit'].apply(lambda x:round(x/100000000,2))
#恒瑞
filenames2 = 'E:\\data\\stock_data\\reports\\sh600276.csv'
stock2 = pd.read_csv(filenames2)
df2 = stock2[stock2['reportdate'].apply(lambda x:x.split('-')[1]) == '12'][['reportdate','parentnetprofit','roeweighted']]
df2['parentnetprofit']=df2['parentnetprofit'].apply(lambda x:round(x/100000000,2))

#平安
filenames3 = 'E:\\data\\stock_data\\reports\\sh601318.csv'
stock3 = pd.read_csv(filenames3)
df3 = stock3[stock3['reportdate'].apply(lambda x:x.split('-')[1]) == '12'][['reportdate','parentnetprofit','sjltz','roeweighted']]
df3['parentnetprofit']=df3['parentnetprofit'].apply(lambda x:round(x/100000000,2))
df3['reportdate']=df3['reportdate'].astype('datetime64')
df3['parentnetprofit']=df3['parentnetprofit'].astype('float64')
df3['roeweighted']=df3['roeweighted'].astype('float64')
df3['sjltz']=df3['sjltz'].astype('float64')
df3.to_csv('C:\\Users\\Administrator\\Desktop\\pingan.csv', mode='w', index=False)

#BYD
filenames3 = 'E:\\data\\stock_data\\reports\\sz002594.csv'
stock3 = pd.read_csv(filenames3)
df3 = stock3[stock3['reportdate'].apply(lambda x:x.split('-')[1]) == '12'][['reportdate','parentnetprofit','sjltz','roeweighted']]
df3['parentnetprofit']=df3['parentnetprofit'].apply(lambda x:round(x/100000000,2))
df3['reportdate']=df3['reportdate'].astype('datetime64')
df3['parentnetprofit']=df3['parentnetprofit'].astype('float64',raise_on_error = False)
df3['roeweighted']=df3['roeweighted'].astype('float64',raise_on_error = False)
df3['sjltz']=df3['sjltz'].astype('float64',raise_on_error = False)
df3.to_csv('C:\\Users\\Administrator\\Desktop\\BYD.csv', mode='w', index=False)

#复星恒瑞合并对比
a = pd.merge(df1, df2, on='reportdate')
a.to_csv('C:\\Users\\Administrator\\Desktop\\1.csv', mode='w', index=False)
a['reportdate']=a['reportdate'].astype('datetime64')
a['roeweighted_x']=a['roeweighted_x'].astype('float64')
a['roeweighted_y']=a['roeweighted_y'].astype('float64')
b = a.sort_values(by = ['reportdate'], ascending = True).set_index('reportdate')
#显示
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
b.columns = [u'复星净利润（亿元）',u'复星ROE（%）',u'恒瑞净利润（亿元）',u'恒瑞ROE（%）']
b.plot()
plt.show()






