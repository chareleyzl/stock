# -*- coding: utf-8 -*-
# 改字符集
import sys
reload(sys)
sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

import pandas as pd
import tushare as ts
#on ricequant, choose stock_list from list
stock_list=all_instruments()
stock_list.loc[stock_list['order_book_id'].apply(lambda x:x[-5:])=='.XSHE']
#pure tushare -用于获股票列表，以及单笔走势验证
ts.get_h_data(code='601318',start='2007-01-01', end='2015-03-16')
ts.get_report_data(2016,3)

######################历史个股数据分析（10年涨幅，从西南证券下载）
#上证综指
sh = pd.read_csv('e:\stock\SH#999999.txt',delimiter='\t',encoding='utf-8')
sh['收盘']
#浦发银行测试

#dateparse = lambda dates: pd.datetime.strptime(dates,'%Y/%m/%d') 
stock = pd.read_csv('E:\\stock\\ls\\SZ#300085.txt',delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='gb2312')
stock.iloc[:,3].plot()
sh = pd.read_csv('E:\\stock\\SH#999999.txt',delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='utf-8')
sh.iloc[:,3].plot()

ts.get_stock_basics().loc['600744',:]#选取索引
#读取所有4季报并存档
i = 2006
while i < 2017:
    rpt=ts.get_report_data(i,4)
    rpt.to_csv('E:\\stock\\fin_rpt\\rpt200604_1604',mode='a+',encoding='utf-8')
    i+=1
    
##目标：寻找高成长股与业绩增长的关联关系，衡量价值投资在A股市场的价值。
##方法：分别清理业绩和股价，读入数据框综合分析：先看业绩高成长股价表现，再看股价高成长业绩表现，最后分析关联度。
##误差分析与控制：
def stock_finder(years=10,times=10,category='ls'):
    import pandas as pd
    import glob
    day_list = {10:['2007/01/04','2007/03/22','rpt200604'],9:['2008/01/04','2008/03/24','rpt200704'],8:['2009/01/04','2009/03/24','rpt200804'],7:['2010/01/04','2010/03/22','rpt200904'],6:['2011/01/04','2011/03/22','rpt201004'],5:['2012/01/04','2012/03/22','rpt201104'],4:['2013/01/04','2013/03/22','rpt201204'],3:['2014/01/06','2014/03/24','rpt201304'],2:['2015/01/05','2015/03/23','rpt201404']}
    txt_filenames = glob.glob('E:\\stock\\'+ category +'\\*.txt')
    with open ('E:\\stock\\'+str(times)+'times_'+str(years)+'years_'+category+'.txt','w') as f:
        f.truncate
        f.write('code  name  times1  times3  net_profit_times  net_profit_times_check\n')
    rpt = pd.read_csv('E:\\stock\\fin_rpt\\rpt200604_1604',header=0)#读取10年来年报大全
    for filename in txt_filenames:
        stock = pd.read_csv(filename,delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='gb2312')
        try: 
            jan0 = stock.loc[day_list[years][0]][2] 
            jan1 = stock.loc['2017/01/04'][2]
            mar0 = stock.loc[day_list[years][1]][2] 
            mar1 = stock.loc['2017/03/22'][2]
            stock_code = filename.split('#')[1].split('.')[0]  #取得文档名中股票代码
            stock_name = rpt[rpt.code==stock_code].iloc[-1,2]  #业绩报表中取得股票名称
            net1 = float(rpt[rpt.code==stock_code].iloc[-years-1,-4])#N年前净利润
            net2 = float(rpt[rpt.code==stock_code].iloc[-years,-4])#N+1年前净利润，消除利润误差
            net3 = float(rpt[rpt.code==stock_code].iloc[-1,-4])#2006年净利润
  
        except Exception as e:
            pass 
        finally:
            if times*jan0 < jan1 or times*mar0 < mar1:
                jan_times = round(jan1 / jan0,2)
                mar_times = round(mar1 / mar0,2)
                net_times = round(net3 / net1,2)
                net_times_c = round(net3 / net2,2)
                with open ('E:\\stock\\'+str(times)+'times_'+str(years)+'years_'+category+'.txt','a') as f:#需要设置系统环境为utf8，否则中文乱码
                    f.write(stock_code+' '+stock_name.encode('gb2312')+' '+str(jan_times)+' '+str(mar_times)+' '+str(net_times)+' '+str(net_times_c)+'\n')   






