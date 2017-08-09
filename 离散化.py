#-*- coding: utf-8 -*-  
#���ݹ淶��  
import pandas as pd  
  
datafile = 'data/discretization_data.xls' #������ʼ��  
data = pd.read_excel(datafile) #��ȡ����  
data = data[u'��������֤��ϵ��'].copy()  
k = 4  
  
d1 = pd.cut(data, k, labels = range(k)) #�ȿ���ɢ�������������������Ϊ0,1,2,3  
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html pd.cut  
  
#��Ƶ����ɢ��  
w = [1.0*i/k for i in range(k+1)]  
w = data.describe(percentiles = w)[4:4+k+1] #ʹ��describe�����Զ������λ��  
w[0] = w[0]*(1-1e-10)  
d2 = pd.cut(data, w, labels = range(k))  
  
from sklearn.cluster import KMeans #����KMeans  
kmodel = KMeans(n_clusters = k, n_jobs = 4) #����ģ�ͣ�n_jobs�ǲ�������һ�����CPU���Ϻ�  
kmodel.fit(data.reshape((len(data), 1))) #ѵ��ģ��  
c = pd.DataFrame(kmodel.cluster_centers_).sort(0) #����������ģ���������Ĭ���������ģ�  
w = pd.rolling_mean(c, 2).iloc[1:] #�����������е㣬��Ϊ�߽��  
w = [0] + list(w[0]) + [data.max()] #����ĩ�߽�����  
d3 = pd.cut(data, w, labels = range(k))  
  
def cluster_plot(d, k): #�Զ�����ͼ��������ʾ������  
  import matplotlib.pyplot as plt  
  plt.rcParams['font.sans-serif'] = ['SimHei'] #����������ʾ���ı�ǩ  
  plt.rcParams['axes.unicode_minus'] = False #����������ʾ����  
    
  plt.figure(figsize = (8, 3))  
  for j in range(0, k):  
    plt.plot(data[d==j], [j for i in d[d==j]], 'o')  
    
  plt.ylim(-0.5, k-0.5)  
  return plt  
  
cluster_plot(d1, k).show()  
  
cluster_plot(d2, k).show()  
cluster_plot(d3, k).show() 