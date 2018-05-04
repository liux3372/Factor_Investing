# encoding: UTF-8
import os
import pandas as pd
#降序前N个
print('''成长因子降序排列价值因子升序排列''')

#------------------------------------------------------
def gotoStrategy(rootdir, saveP, topn, sortn):
    '''遍历文件夹执行
    topn  输入每个行业选择几支股票
    sortn 降序排序的列号（数字）
    '''
    for parent,dirnames,filenames in os.walk(rootdir):
        for fileName in filenames:
            #文件路径
            filePath = os.path.join(parent, fileName)
            #保存文件的路径
            tempList = fileName.split('.')
            temp = 'R_' + '.'.join(tempList[:-1]) + '.xlsx'
            saveFile = os.path.join(saveP, temp)            
            #数据处理
            data = pd.read_excel(filePath, skip_footer=2)
            data = data.dropna(axis=0, how='any')
            data = data.sort_values([data.columns[sortn], data.columns[-1]], ascending=[True, False])            
            
            a = data.groupby(data.columns.values[3])
            
            result = None
            for i in range(topn):
                if result is None:
                    result = a.nth(i)
                else:
                    result = result.append(a.nth(i))
                    
            result.to_excel(saveFile)
#------------------------------------------------------

#参数顺序:1原始文件的路径，2保存数据的路径，3每个行业选择股票个数，4降序排序的列号
#gotoStrategy('A', 'B', 3, 2)
if __name__=='__main__':
    #print 'main'
    gotoStrategy('/Users/xinyuan/Desktop/codeForPaper/raw_data/PEG/data', '/Users/xinyuan/Desktop/codeForPaper/raw_data/PEG/pool', 3, 2)




