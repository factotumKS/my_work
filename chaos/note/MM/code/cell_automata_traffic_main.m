% 车流密度不变下的双向两车道仿真（T 字形路口）
 
% nc:双向车道数目 2，nl:车道长度（偶数）
 
% v:平均速度，d:换道次数（1000 次）p:车流密度
 
% dt:仿真步长时间，nt:仿真步长数目
 
% fp:车道入口处新进入车辆的概率（列向量）
 
 
 
nl = 40 ;nc = 2;
 
dt=0.75;nt=500;
 
fp = 5;
 
chance=0.5;
 
chance1=0.5;
 
 
 
[ v, d, p ] = multi_driveway_with_crossroad_exit ( nl,nc,dt,fp,nt,chance,chance1);
 