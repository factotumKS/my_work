%R聚类
clc, clear
%格式要求为:“对象*属性”的矩阵
a=load('gj.txt'); %把原始数据保存在纯文本文件gj.txt中
b=zscore(a); %数据标准化
r=corrcoef(b) %计算相关系数矩阵
%d=tril(1-r); d=nonzeros(d)'; %另外一种计算距离方法
d=pdist(b','correlation'); %计算相关系数导出的距离
z=linkage(d,'average');  %按类平均法聚类
h=dendrogram(z);  %画聚类图
set(h,'Color','k','LineWidth',1.3)  %把聚类图线的颜色改成黑色，线宽加粗
T=cluster(z,'maxclust',6)  %把变量划分成6类
for i=1:6
    tm=find(T==i);  %求第i类的对象
    tm=reshape(tm,1,length(tm)); %变成行向量
    fprintf('the %d(th) kind cinlude: %s\n',i,int2str(tm)); %显示分类结果
end
