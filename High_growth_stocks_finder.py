# -*- coding: utf-8 -*-
##寻找近10年高成长股；对比日期2017年一月初和三月末；
##参数：年数、股价上涨倍数、股票分类（默认all为全部A股）
import pandas as pd
import glob
import tushare as ts
#tushare有时下载不一样。
#0 准备。读取10年来季报
def stock_rpt(year=10):
    i = 2017-year-1
    while i < 2017:
        for season in [1,2,3,4]:
            rpt = ts.get_report_data(i,season)
            rpt.to_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(i)+str(season),mode='a+',encoding='utf-8')#注意模式不要重复哟
        i+=1
        
#1 所有记录在案股票，N年来业绩变化(有的股票财报不全);
#20170619新增：选择参考年后一年和15年的年报加入对比，作更多参考。
def stock_rpt_change(years=10): 
    j = 2017-years-1
    rpt30 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(j+1)+'4',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rpt40 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+str(j)+'4',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rpt31 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+'20154',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rpt41 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt'+'20164',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    stock_list = []
    stocks = ts.get_stock_basics()
    count = 0
    for i in stocks.index:
        try:
            stock_name = stocks['name'].loc[i]  #业绩报表中取得股票名称
            
            net30 = float(rpt30[rpt30.code==i]['net_profits'][:1])#N-1年前净利润
            
            net40 = float(rpt40[rpt40.code==i]['net_profits'][:1])#N年前净利润
            
            net31 = float(rpt31[rpt31.code==i]['net_profits'][:1])#2015年净利润  
            #print('test')
            net41 = float(rpt41[rpt41.code==i]['net_profits'][:1])#2016年净利润 
            #print('test')
            times_3 = round(net31 / net30,2)
            times_4 = round(net41 / net40,2)
            
            rows_list = [i,stock_name,times_3,times_4,net30,net40,net31,net41]
            stock_list.append(rows_list)
        except Exception as e:
            count += 1
            pass
    print(count) 
    df = pd.DataFrame(data=stock_list,columns=['code','name','times_3','times_4','net30','net40','net31','net41'])
    df.to_csv('E:\\stock\\'+str(years)+'years_'+'rpt_change'+'.txt')  
    
#2 寻找高成长股（如：股价十年十倍）--筛选版
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
                with open(filename,'r') as f:#读取文件里面的股票信息
                    while True:
                        line = f.readline()
                        if line !=[]:
                            break
                with open ('E:\\stock\\'+str(times)+'times_'+str(years)+'years_'+category+'.txt','a') as f:
                    f.write(line.split(' ')[0]+' '+line.split(' ')[1]+'\n' )     
        except Exception as e:
            pass 
            
#3 全部股票N年内价格变动情况 - 完整版（供与业绩对比分析）
def stock_price(years=10,category='all'):  #需要确定以下日期有股价信息
    day_list = {10:['2007/01/04','2007/03/22'],9:['2008/01/04','2008/03/24'],8:['2009/01/05','2009/03/24'],7:['2010/01/04','2010/03/22'],6:['2011/01/04','2011/03/22'],5:['2012/01/04','2012/03/22'],4:['2013/01/04','2013/03/22'],3:['2014/01/06','2014/03/24'],2:['2015/01/05','2015/03/23']}
    txt_filenames = glob.glob('E:\\data\\stock_data\\'+ category +'\\*.txt')
    stock_list = []
    for filename in txt_filenames:
        stock = pd.read_csv(filename,delimiter='\t',header=1,index_col=0,parse_dates=True,encoding='gb2312')#日期为索引的股价
        try: 
            stock_code = filename.split('#')[1].split('.')[0]  #取得文档名中股票代码
            jan0 = stock.loc[day_list[years][0]][3] 
            jan1 = stock.loc['2017/01/04'][3]
            mar0 = stock.loc[day_list[years][1]][3] 
            mar1 = stock.loc['2017/03/22'][3]
            times_jan = round(jan1 / jan0,2)
            times_mar = round(mar1 / mar0,2)
            rows_list = [stock_code,times_jan,times_mar,jan0,jan1,mar0,mar1]
            stock_list.append(rows_list) #把单个股票变动情况加入汇总列表
        except Exception as e:
            pass 
        finally:
            df = pd.DataFrame(data=stock_list,columns=['code','times_jan','times_mar','jan0','mar0','jan1','mar1'])
            df.to_csv('E:\\stock\\'+str(years)+'years_'+category+'.txt')          

if __name__ == '__main__': 
    #股价和业绩变动
    stock_price(years=8,category='bx')
    stock_rpt_change(years=8)
    #分别读取业绩和股价文件，关联生成DataFrame
    rpt = pd.read_csv('E:\\stock\\8years_rpt_change.txt',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    price = pd.read_csv('E:\\stock\\8years_bx.txt',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    mg = pd.merge(rpt,price,on='code')
    mg1=mg[(mg.times_4>0)][mg.times_mar>0].loc[:,['code','times_3','times_4','net30','net40','net31','net41','times_jan','times_mar']]
    
    
    #业绩股价相关性
    mg1.corr()
    
    #绘图
    mg1.plot()
    #======测试平安业绩 与 股价(结果，股价波动太大，应选择有代表性的点或时间段)
    mg1[mg1.code=='601318']
    price[price.code=='601318']
    rpt00[rpt00.code=='002594']
    
    #=============查看某公司年报是否获得
    rptxx = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt20164',header=0,index_col=0,encoding='utf-8',dtype={'code':'object'})
    rptxx[rptxx.name==u'中国平安'] 
    

    
