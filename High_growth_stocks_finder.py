# -*- coding: utf-8 -*-
##寻找近10年高成长股；对比日期2017年一月初和三月末；
##参数：年数、股价上涨倍数、股票分类（默认all为全部A股）
import pandas as pd
import glob
import tushare as ts
#读取10年来季报
def stock_rpt(year=10):
    i = 2017-year-1
    while i < 2017:
        for season in [1,2,3,4]:
            rpt = ts.get_report_data(i,season)
            rpt.to_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(i)+str(season),mode='a+',encoding='utf-8')
        i+=1
        
#寻找N年来业绩变化(有的股票财报不全，同时满足以下4个季报的占少数)
def stock_rpt_change(years=10): 
    j = 2017-years-1
    #rpt30 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(j)+'3',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rpt40 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(j)+'4',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    #rpt31 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+'20163',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rpt41 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+'20164',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    stock_list = []
    stocks = ts.get_stock_basics()
    count = 0
    for i in stocks.index:
        try:
            stock_name = stocks['name'].loc[i]  #业绩报表中取得股票名称
            #net30 = float(rpt30[rpt30.code==i]['net_profits'][:1])#N年前第3季度净利润
            net40 = float(rpt40[rpt40.code==i]['net_profits'][:1])#N年前净利润
            #net31 = float(rpt31[rpt31.code==i]['net_profits'][:1])#2016年3季度净利润  
            net41 = float(rpt41[rpt41.code==i]['net_profits'][:1])#2016年净利润 
            #times_3 = round(net31 / net30,2)
            times_4 = round(net41 / net40,2)
            rows_list = [i,stock_name,times_4,net40,net41]
            stock_list.append(rows_list)
        except Exception as e:
            count += 1
            pass
    print(count) 
    df = pd.DataFrame(data=stock_list,columns=['code','name','times_4','net40','net41'])
    df.to_csv('E:\\stock\\'+str(years)+'years_'+'rpt_change'+'.txt')  
    
#寻找高成长股（如：十年十倍）
def stock_finder(years=10,times=10,category='all'):
    day_list = {10:['2007/01/04','2007/03/22'],9:['2008/01/04','2008/03/24'],8:['2009/01/04','2009/03/24'],7:['2010/01/04','2010/03/22'],6:['2011/01/04','2011/03/22'],5:['2012/01/04','2012/03/22'],4:['2013/01/04','2013/03/22'],3:['2014/01/06','2014/03/24'],2:['2015/01/05','2015/03/23']}
    txt_filenames = glob.glob('E:\\stock\\'+ category +'\\*.txt')
    with open ('E:\\stock\\'+str(times)+'times_'+str(years)+'years_'+category+'.txt','w') as f:
        f.truncate
    for filename in txt_filenames:
        stock = pd.read_csv(filename,delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='gb2312')
        try: 
            judge11 = times*stock.loc[day_list[years][0]][2] < stock.loc['2017/01/04'][2]
            judge12 = times*stock.loc[day_list[years][1]][2] < stock.loc['2017/03/22'][2]
            if judge11 or judge12:
                with open(filename,'r') as f:
                    while True:
                        line = f.readline()
                        if line !=[]:
                            break
                with open ('E:\\stock\\'+str(times)+'times_'+str(years)+'years_'+category+'.txt','a') as f:
                    f.write(line.split(' ')[0]+' '+line.split(' ')[1]+'\n' )     
        except Exception as e:
            pass 
            
#全部股票N年内业绩翻倍情况
def stock_finder2(years=10,category='all'):
    day_list = {10:['2007/01/04','2007/03/22','rpt200604'],9:['2008/01/04','2008/03/24','rpt200704'],8:['2009/01/04','2009/03/24','rpt200804'],7:['2010/01/04','2010/03/22','rpt200904'],6:['2011/01/04','2011/03/22','rpt201004'],5:['2012/01/04','2012/03/22','rpt201104'],4:['2013/01/04','2013/03/22','rpt201204'],3:['2014/01/06','2014/03/24','rpt201304'],2:['2015/01/05','2015/03/23','rpt201404']}
    txt_filenames = glob.glob('E:\\data\\stock_data\\'+ category +'\\*.txt')
    stock_list = []
    for filename in txt_filenames:
        stock = pd.read_csv(filename,delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='gb2312')
        try: 
            stock_code = filename.split('#')[1].split('.')[0]  #取得文档名中股票代码
            jan0 = stock.loc[day_list[years][0]][2] 
            jan1 = stock.loc['2017/01/04'][2]
            mar0 = stock.loc[day_list[years][1]][2] 
            mar1 = stock.loc['2017/03/22'][2]
            times_jan = round(jan1 / jan0,2)
            times_mar = round(mar1 / mar0,2)
            rows_list = [stock_code,times_jan,times_mar,jan0,jan1,mar0,mar1]
            stock_list.append(rows_list)
        except Exception as e:
            pass 
        finally:
            df = pd.DataFrame(data=stock_list,columns=['code','times_jan','times_mar','jan0','mar0','jan1','mar1'])
            df.to_csv('E:\\stock\\'+str(years)+'years_'+category+'.txt')          

if __name__ == '__main__':
    #stock_finder2()
    #stock_rpt_change()
    #读取业绩和股价文件，关联生成DataFrame
    rpt = pd.read_csv('E:\\stock\\10years_rpt_change.txt',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    price = pd.read_csv('E:\\stock\\10years_all.txt',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    mg = pd.merge(rpt,price,on='code')
    mg1=mg[(mg.times_4<50) & (mg.times_4>0)][mg.times_mar>0].loc[:,['times_4','times_mar']]
    mg1.plot()

    
