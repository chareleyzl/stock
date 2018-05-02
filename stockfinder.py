# -*- coding:utf-8 -*-
import pandas as pd
import glob
import os
# 1 全部股票业绩信息
def stock_report(years=10):
    if os.path.exists('E:\\stock\\' + str(years) + 'years_' + 'rpt_change' + '.txt'):
        return
    filenames = glob.glob('E:\\data\\stock_data\\reports\\*.csv')
    stock_list = []
    count = 0
    j = 2017 - years
    for f in filenames:
        stock = pd.read_csv(f)
        try:
            name = stock['sname'][:1].values[0]
            code = stock['scode'][:1].values[0]
            roe07 = stock.loc[stock['reportdate'].apply(lambda x:x.split('-')[0]+x.split('-')[1]) == str(j)+'12'][:1]['roeweighted'].values[0]
            net07 = round(
                stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == str(j) + '12'][:1][
                    'parentnetprofit'] / 10000, 2).values[0]
            roe08 = stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == str(j+1)+'12'][:1][
                    'roeweighted'].values[0]
            net08 = round(stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == str(j+1)+'12'][:1][
                    'parentnetprofit'] / 10000, 2).values[0]
            roe16 = stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == '201612'][:1][
                    'roeweighted'].values[0]
            net16 = round(
                stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == '201612'][:1][
                    'parentnetprofit'] / 10000, 2).values[0]
            roe17 = stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == '201712'][:1][
                    'roeweighted'].values[0]
            net17 = round(
                stock.loc[stock['reportdate'].apply(lambda x: x.split('-')[0] + x.split('-')[1]) == '201712'][:1][
                    'parentnetprofit'] / 10000, 2).values[0]

            times_17 = round(net17 / net07, 2)
            times_16 = round(net16 / net08, 2)
            rows_list = [code, name, times_17, times_16, net07, net08, net16, net17, roe07, roe08, roe16, roe17]
            stock_list.append(rows_list)
        except Exception as e:
            count += 1
            pass
    print(count)
    df = pd.DataFrame(data=stock_list,
                      columns=['code', 'name', '17ReportX', '16ReportX', str(j) + 'net',  str(j+1) + 'net', '16net', '17net', str(j) + 'roe', str(j+1) + 'roe',  '16roe', '17roe'])
    df.to_csv('E:\\stock\\' + str(years) + 'years_' + 'rpt_change' + '.txt', encoding='utf8')

# 2 全部股票N年内价格变动情况
def stock_price(years=10, category='all'):
    if os.path.exists('E:\\stock\\' + str(years) + 'years_' + category + '.txt'):
        return
    # 确定以下日期有股价信息
    day_list = {10: ['2008/01/02', '2009/01/05'], 9: ['2009/01/05', '2010/01/04'], 8: ['2010/01/04', '2011/01/04'],
                7: ['2011/01/04', '2012/01/04'], 6: ['2012/01/04', '2013/01/04'], 5: ['2013/01/04', '2014/01/06'],
                4: ['2014/01/06', '2015/01/05'], 3: ['2015/01/05', '2016/01/04']}
    txt_filenames = glob.glob('E:\\data\\stock_data\\' + category + '\\*')
    stock_list = []
    for filename in txt_filenames:
        stock = pd.read_csv(filename, delimiter='\t', header=None, index_col=0, parse_dates=True,
                            encoding='gb2312')  # 日期为索引的股价
        try:
            stock_code = filename.split('#')[1].split('.')[0]  # 取得文档名中股票代码
            p16 = stock.loc['2017/01/04'][3]
            p08 = stock.loc[day_list[years][1]][3]
            p07 = stock.loc[day_list[years][0]][3]
            p17 = stock.loc['2018/01/04'][3]
            times_17 = round(p17 / p07, 2)
            times_16 = round(p16 / p08, 2)
            rows_list = [stock_code, times_17, times_16]
            stock_list.append(rows_list)  # 把单个股票变动情况加入汇总列表
        except Exception as e:
            pass

    df = pd.DataFrame(data=stock_list,
                      columns=['code', '17PriceX', '16PriceX'])
    df.to_csv('E:\\stock\\' + str(years) + 'years_' + category + '.txt', encoding='utf8')

# 3 合并数据框
def stock_comp(year=10, category='all'):
    # 业绩和股价变动
    stock_report(years=year)
    stock_price(years=year, category=category)
    # 分别读取业绩和股价文件，关联生成DataFrame。在读取rpt的时候，6、8年存在问题，怀疑是该年度有公司的roe值异常。
    n = 2017 - year
    rpt = pd.read_csv('E:\\stock\\'+str(year)+'years_rpt_change.txt', header=0, index_col=0)
    #
    price = pd.read_csv('E:\\stock\\'+str(year)+'years_'+category+'.txt', header=0, index_col=0)
    mg1 = pd.merge(rpt, price, on='code')
    #调整列的顺序，把股价倍数前移
    cols = list(mg1)
    cols.insert(4, cols.pop(cols.index('17PriceX')))
    cols.insert(5, cols.pop(cols.index('16PriceX')))
    mg1 = mg1.ix[:, cols]
    # 将roe的类型转换为字符型
    mg1[['17ReportX', '16ReportX', '17PriceX', '16PriceX',str(n) + 'roe', str(n+1) + 'roe', '16roe', '17roe']] = mg1[['17ReportX', '16ReportX', '17PriceX', '16PriceX',str(n) + 'roe', str(n+1) + 'roe', '16roe', '17roe']].apply(
        lambda x: pd.to_numeric(x, errors='drop'))
    # 排除有负数的情况,将其整行删除；按17年业绩倍数排序
    mg = mg1[(mg1['16PriceX'] > 0) & (mg1['16ReportX'] > 0) & (mg1['17PriceX'] > 0) & (mg1['17ReportX'] > 0)].dropna().sort_values(by='17ReportX', ascending=False)
    # 将Dataframe保存到桌面excel
    mg.to_csv('E:\\stock\\'+ category + str(year) +'.csv', mode='w', index=False, encoding='utf8')
    mgh = mg[(mg['17ReportX']>10) & (mg['17net']>100000)].sort_values(by = ['17ReportX'], ascending = False)
    mgh.to_csv('E:\\stock\\h_'+ category + str(year) +'.csv', mode='w', index=False, encoding='utf8')
if __name__ == '__main__':
    stock_comp(year=10, category='jx')



