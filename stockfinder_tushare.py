# -*- coding: utf-8 -*-
# 寻找近10年高成长股；对比日期2017年一月初和三月末；
# 参数：年数、股价上涨倍数、股票分类（默认all为全部A股）
import pandas as pd
import glob
import tushare as ts

# 0 准备。读取10年来季报。注：tushare有时下载不一样。
def stock_rpt(year=10):
    i = 2017 - year - 1
    while i < 2017:
        for season in [1, 2, 3, 4]:
            rpt = ts.get_report_data(i, season)
            rpt.to_csv('E:\\data\\stock_data\\fin_rpt\\rpt' + str(i) + str(season), mode='a+',
                       encoding='utf-8')  # 注意模式不要重复哟
        i += 1


# 年报汇总
def get_fin_all():
    i = 2007
    while i < 2018:
        j = 1
        while j < 5:
            try:
                rpt = ts.get_report_data(i, j)
                rpt['P'] = str(i) + str(j)
                rpt.to_csv('E:\\data\\stock_data\\fin_rpt\\rpt2007-2017', mode='a+', encoding='utf-8')
                j += 1
            except Exception as e:
                break
        i += 1


# 日期转换为年/季度格式函数
def Get_season(x):
    try:
        P_year = x.split('/')[0]
        P_month = x.split('/')[1]
        if P_month in ['01', '02', '03']:
            season = '1'
        if P_month in ['04', '05', '06']:
            season = '2'
        if P_month in ['07', '08', '09']:
            season = '3'
        if P_month in ['10', '11', '12']:
            season = '4'
        return P_year + season
    except Exception as e:
        pass


# 1 所有记录在案股票，N年来业绩变化(有的股票财报不全);
def stock_rpt_change(years=10):
    j = 2017 - years - 1
    rpt10 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt' + str(j + 1) + '1', header=0, index_col=0,
                        encoding='utf-8', dtype={'code': 'object'})
    rpt40 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt' + str(j) + '4', header=0, index_col=0, encoding='utf-8',
                        dtype={'code': 'object'})
    rpt11 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt' + '20171', header=0, index_col=0, encoding='utf-8',
                        dtype={'code': 'object'})
    rpt41 = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt' + '20164', header=0, index_col=0, encoding='utf-8',
                        dtype={'code': 'object'})
    stock_list = []
    stocks = ts.get_stock_basics()
    count = 0
    for i in stocks.index:
        try:
            stock_name = stocks['name'].loc[i]  # 业绩报表中取得股票名称
            net10 = float(rpt10[rpt10.code == i]['net_profits'].iloc[0])  # N -1年前1季度净利润
            net40 = float(rpt40[rpt40.code == i]['net_profits'].iloc[0])  # N 年前净利润
            net11 = float(rpt11[rpt11.code == i]['net_profits'].iloc[0])  # 2017年1季度净利润
            net41 = float(rpt41[rpt41.code == i]['net_profits'].iloc[0])  # 2016年净利润
            times_1 = round(net11 / net10, 2)
            times_4 = round(net41 / net40, 2)
            rows_list = [i, stock_name, times_1, times_4, net10, net40, net11, net41]
            stock_list.append(rows_list)
        except Exception as e:
            count += 1
            pass
    print(count)
    df = pd.DataFrame(data=stock_list,
                      columns=['code', 'name', '201701times', '2016times', 'net30', 'net40', 'net31', 'net41'])
    df.to_csv('E:\\stock\\' + str(years) + 'years_' + 'rpt_change' + '.txt')


# 2 全部股票N年内价格变动情况
def stock_price(years=10, category='all'):  # 需要确定以下日期有股价信息
    day_list = {10: ['2007/01/04', '2007/03/22'], 9: ['2008/01/04', '2008/03/24'], 8: ['2009/01/05', '2009/03/24'],
                7: ['2010/01/04', '2010/03/22'], 6: ['2011/01/04', '2011/03/22'], 5: ['2012/01/04', '2012/03/22'],
                4: ['2013/01/04', '2013/03/22'], 3: ['2014/01/06', '2014/03/24'], 2: ['2015/01/05', '2015/03/23']}
    txt_filenames = glob.glob('E:\\data\\stock_data\\' + category + '\\*.txt')
    stock_list = []
    for filename in txt_filenames:
        stock = pd.read_csv(filename, delimiter='\t', header=None, index_col=0, parse_dates=True,
                            encoding='gb2312')  # 日期为索引的股价
        try:
            stock_code = filename.split('#')[1].split('.')[0]  # 取得文档名中股票代码
            jan0 = stock.loc[day_list[years][0]][3]
            jan1 = stock.loc['2017/01/04'][3]
            mar0 = stock.loc[day_list[years][1]][3]
            mar1 = stock.loc['2017/03/22'][3]
            times_jan = round(jan1 / jan0, 2)
            times_mar = round(mar1 / mar0, 2)
            rows_list = [stock_code, times_jan, times_mar, jan0, jan1, mar0, mar1]
            stock_list.append(rows_list)  # 把单个股票变动情况加入汇总列表
        except Exception as e:
            pass

    df = pd.DataFrame(data=stock_list,
                      columns=['code', 'times_jan', 'times_mar', 'jan0', 'jan1', 'mar0', 'mar1'])
    df.to_csv('E:\\stock\\' + str(years) + 'years_' + category + '.txt')


# 2.5 寻找高成长股，写入文件（如：股价十年十倍）--筛选版
def stock_finder(years=10, times=10, category='all'):
    day_list = {10: ['2007/01/04', '2007/03/22'], 9: ['2008/01/04', '2008/03/24'], 8: ['2009/01/04', '2009/03/24'],
                7: ['2010/01/04', '2010/03/22'], 6: ['2011/01/04', '2011/03/22'], 5: ['2012/01/04', '2012/03/22'],
                4: ['2013/01/04', '2013/03/22'], 3: ['2014/01/06', '2014/03/24'], 2: ['2015/01/05', '2015/03/23']}
    txt_filenames = glob.glob('E:\\stock\\' + category + '\\*.txt')
    with open('E:\\stock\\' + str(times) + 'times_' + str(years) + 'years_' + category + '.txt', 'w') as f:
        f.truncate
    for filename in txt_filenames:
        stock = pd.read_csv(filename, delimiter='\t', header=1, index_col=0, parse_dates=True, encoding='gb2312')
        try:
            judge11 = times * stock.loc[day_list[years][0]][2] < stock.loc['2017/01/04'][2]
            judge12 = times * stock.loc[day_list[years][1]][2] < stock.loc['2017/03/22'][2]
            if judge11 or judge12:
                with open(filename, 'r') as f:  # 读取文件里面的股票信息
                    while True:
                        line = f.readline()
                        if line != []:
                            break
                with open('E:\\stock\\' + str(times) + 'times_' + str(years) + 'years_' + category + '.txt', 'a') as f:
                    f.write(line.split(' ')[0] + ' ' + line.split(' ')[1] + '\n')
        except Exception as e:
            pass


# 3 个股股价与净利润绘制（10年变化，从西南证券/tushare下载，一张图显示）
def plot_stockandprofit(code, cat='bx'):
    # 读取一支股票
    #  stock = pd.read_csv('E:\\data\\stock_data\\bx\\SH#601318.txt',delimiter='\t',header=1,parse_dates=True,encoding='gb2312')
    stock = pd.read_csv('E:\\data\\stock_data\\' + cat + '\\SH#' + code + '.txt', delimiter='\t', header=1,
                        parse_dates=True, encoding='gb2312')
    # 添加年/季度字段P
    stock['P'] = stock.iloc[:, 0].apply(Get_season)
    # 获取年报净利润
    rpt = pd.read_csv('E:\\data\\stock_data\\fin_rpt\\rpt2007-2017', header=0,
                      usecols=['code', 'name', 'net_profits', 'eps', 'P'])
    # 取得一支股票净利润，并去掉重复
    net = rpt[rpt.code == code].loc[:, ['net_profits', 'eps', 'P']].drop_duplicates()
    # 把净利润转换为数值型以便画图
    net['net_profits'] = pd.to_numeric(net['net_profits'], errors='coerce')
    # 关联股价和利润；以股价为准，没有利润就空缺
    s = pd.merge(stock.iloc[:, [0, 4, 7]], net, on='P', how='left')
    # 日期转换为序列，只有通过序列，才可以把左右纵坐标画在同一个图
    s.index = s.iloc[:, 0]
    # 结算TTM，将来与股价图画在一起(直接以季度利润算，波动太大！但严格往前算4个季度的利润，取值又不全)
    s['ttm'] = s.iloc[:, 1] / pd.to_numeric(s.iloc[:, 4], errors='coerce') * s.iloc[:, 2].apply(
        lambda x: 4 / int(x[-1]))
    # 股票名称
    name = rpt[rpt.code == code].iloc[-1, 1]
    import matplotlib.pyplot as plt
    plt.figure()
    plt.title(name)
    # 股价
    s.iloc[:, 1].plot(label='股价（元）', grid=True)
    plt.legend(loc='upper center')
    # PE
    s.iloc[:, 5].apply(lambda x: x if x > 0 else 0).plot()
    # 右边纵坐标作出净利润
    s.iloc[:, 3].plot(secondary_y=True, label='净利润（万元）', grid=True)
    plt.legend(loc='upper right')


if __name__ == '__main__':
    # 业绩和股价变动
    stock_rpt_change(years=10)
    stock_price(years=10, category='yy')
    # 分别读取业绩和股价文件，关联生成DataFrame
    rpt = pd.read_csv('E:\\stock\\10years_rpt_change.txt', header=0, index_col=0, dtype={'code': 'object'})
    rpt.columns = ['code', 'name', '201701times', '2016times', 'n1 net', 'n net', '201701net', '2016net']
    price = pd.read_csv('E:\\stock\\10years_yy.txt', header=0, index_col=0, dtype={'code': 'object'})
    mg = pd.merge(rpt, price, on='code')
    mg1 = mg[(mg['2016times'] > 0)][(mg['201701times'] > 0)][(mg['n1 net'] > 0)][mg['n net'] > 0][mg['times_jan'] > 0][
              mg['times_mar'] > 0].loc[:,
          ['name', '2016times', '201701times', 'times_jan', 'times_mar', 'n1 net', 'n net', '201701net', '2016net']]
    # 将Dataframe保存到桌面excel
    mg1.to_csv('C:\\Users\\Administrator\\Desktop\\result.csv', mode='w', encoding='utf-8')

    '''
	#on ricequant, choose stock_list from list
	stock_list=all_instruments()
	stock_list.loc[stock_list['order_book_id'].apply(lambda x:x[-5:])=='.XSHE']
	#pure tushare -用于获股票列表，以及单笔走势验证
	ts.get_h_data(code='601318',start='2007-01-01', end='2015-03-16')
	ts.get_report_data(2016,3)
	a=ts.get_hist_data('600848',ktype='W')
	#上证综指
	sh = pd.read_csv('e:\stock\SH#999999.txt',delimiter='\t',encoding='utf-8')
	sh['收盘']
    # 测试平安业绩 与 股价
    mg1[mg1.code=='601318']
    price[price.code=='601318']
    rpt00[rpt00.code=='002594']
    '''
