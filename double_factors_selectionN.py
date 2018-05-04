# encoding: UTF-8
import os
import pandas as pd
#升序前N个
print('''务必将市值作为最后一列。''')

#------------------------------------------------------
def gotoStrategy(rootdir, saveP, topnlevelone,topnleveltwo, sortn):
    '''遍历文件夹执行
    topn  输入每个行业选择几支股票
    sortn 降序排序的列号（数字）
    value factors ascending
    growth factors descending
    '''
    for parent,dirnames,filenames in os.walk(rootdir):
        for fileName in filenames:
            if ".xlsx" in fileName:
                #文件路径
                filePath = os.path.join(parent, fileName)
                #保存文件的路径
                tempList = fileName.split('.')
                temp = 'R_' + '.'.join(tempList[:-1]) + '.xlsx'
                saveFile = os.path.join(saveP, temp)            
                #数据处理
                #print filePath
                data = pd.read_excel(filePath, skip_footer=2)
                data = data.dropna(axis=0, how='any')
                data = data.sort_values([data.columns[sortn], data.columns[-1]], ascending=[True, False])    
                #data = data.sort_values(data.columns[sortn], ascending=[True])         
                
                #data.columns.values[4]='industry'
                a = data.groupby(data.columns.values[4])
                #a = data.groupby(u'所属申万行业名称\r\n[行业级别] 一级行业  ')

                #data=data.set_index(u'所属申万行业名称\n\n[行业级别] 一级行业')

                #print data.columns
                
                result = None
                #result = None
                for i in range(topnlevelone):
                    if result is None:
                        result = a.nth(i)
                    else:
                        result = result.append(a.nth(i))

                tempFile=saveFile.replace('.xlsx','_temp.xlsx')

                #for test only
                result.to_excel(tempFile)


                newData=pd.read_excel(tempFile)

                #print result.columns
                #column name should be carfully checked as they may appear in a weird way
                #ascending is also weird: if we set true, it actually pick in descending order 
                #update: industry column gets disappeared in the new series result, so the first column becomes net income
                newData = newData.sort_values([result.columns[0], result.columns[2]], ascending=[False, False])
                #newData = newData.sort_values(result.columns[0], ascending=[False])
                
                #print newData.columns
                #output with issue

                #result.columns=['industry','code','factor1','factor2','marketcap']
                
                b = newData.groupby(newData.columns[0])
                

                finalResult=None

                for j in range(topnleveltwo):
                    if finalResult is None:
                        finalResult = b.nth(j)
                    else:
                        finalResult = finalResult.append(b.nth(j))
                    

                finalResult.to_excel(saveFile) 

                #os.remove(tempFile)       
            
#------------------------------------------------------

#参数顺序:1原始文件的路径，2保存数据的路径，3每个行业选择股票个数，4升序排序的列号
#gotoStrategy('A', 'B', 3, 2)
if __name__=='__main__':
    #print 'main'
    gotoStrategy('/Users/xinyuan/Desktop/codeForPaper/raw_data_and_codes_PB/data_test', '/Users/xinyuan/Desktop/codeForPaper/raw_data_and_codes_PB/pool_double_level', 6, 3, 2)




