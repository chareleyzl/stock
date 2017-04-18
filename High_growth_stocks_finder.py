# -*- coding: utf-8 -*-
##寻找近10年高成长股；对比日期2017年一月初和三月末；
##参数：年数、股价上涨倍数、股票分类（默认ls为全部A股）
import pandas as pd
import glob

def stock_finder(years=10,times=10,category='ls'):
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
        
if __name__ == '__main__':
    stock_finder(5,10,'ls')
