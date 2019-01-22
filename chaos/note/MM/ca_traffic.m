function [ v d p ] = multi_driveway( nl,nc,fp,dt,nt )
%  在某一特定车流密度下的（车流密度由fp决定）单、双车道仿真模型
%  nc:车道数目（1或2），nl:车道长度——输入参数
%  v:平均速度，d:换道次数（1000次）p:车流密度——输出参数
%  dt:仿真步长时间，nt:仿真步长数目——输入参数
%  fp:车道入口处新进入车辆的概率——输入参数
%  test:
%  nl = 400;fp = 0.5;
%  nc = 2;dt=0.01;nt=500;
   %构造元胞矩阵
   B=ones(2*nc+1,nl+2);
   %奇数行为不可行车道
   B(1:2:(2*nc+1),:)=1.2;
   %初始化仿真元胞状态（1为无车，0为有车）
   bb=B(2:2:2*nc,:);bb(bb~=0)=1;B(2:2:2*nc,:)=bb;B(2:2:2*nc,end)=0;
   %显示初始交通流图
   figure(1);
   H=imshow(B,[]);
   set(gcf,'position',[241 132 560 420]) ;%241 132 560 420
   set(gcf,'doublebuffer','on');  %241
   title('cellular-automation to traffic modeling','color','b');
   %初始化化存储元胞上车辆状态的矩阵
   S(1:nc,nl) = 0;
   Q(1:nc,1:2) = 0;
   Acc(1:nc,1:(nl+2))=0;
   %初始化换道频率、平均速度、车流密度相关变量
   ad = 0;
   av(1:nt) = 0;
   ap(1:nt) = 0;
   c = 1;
   for n = 1:nt
      A=B(2:2:2*nc,:);
      %确定前n-2个车辆的状态
      S(:,:) = 0;
      S(A(:,1:end-2)==0&A(:,2:end-1)==1&A(:,3:end)==1)=2;%加速的车
      S(A(:,1:end-2)==0&A(:,2:end-1)==0)=3;%停车的车
      S(A(:,1:end-2)==0&A(:,2:end-1)==1&A(:,3:end)==0)=1;%减速行驶的车
      %确定最后2两个元胞的状态
      Q(:,:) = 0;
      Q(A(:,end-1)==0&A(:,end)==0) = 1;
      Q(A(:,end-1)==0&A(:,end)==1) = 2;
      Q(A(:,end-1)==1&A(:,end)==0) = 2;
      Q(:,end) = 1;
      %获得所有元胞上车辆的状态
      Acc = [ S Q ];
      %换路规则
      if(nc>1&&n>nl/2)
          %遍历每一个元胞
          for g = 1:length(Acc(1,:))
              %停车状态车辆如另一条路有2空位则换路
              if( Acc(1,g)==3&&Acc(2,g)==0&&Acc(2,g+1)==0)
                  A(1,g)=1;
                  A(2,g)=0;
                  ad=ad+1;
              elseif( Acc(2,g)==3&&Acc(1,g)==0&&Acc(1,g+1)==0 )
                  A(1,g)=0;
                  A(2,g)=1;
                  ad=ad+1;
              %均速行驶车辆如另一条路有3空位则换路
              elseif( Acc(1,g)==1&&Acc(2,g)==0&&Acc(2,g+1)==0&&Acc(2,g+1)==0 )
                  A(1,g)=1;
                  A(2,g)=0; 
                  ad =ad+1;
              elseif( Acc(2,g)==1&&Acc(1,g)==0&&Acc(1,g+1)==0&&Acc(1,g+1)==0 )
                  A(1,g)=0;
                  A(2,g)=1;
                  ad=ad+1;
              end
          end
          %换路后重新设置元胞上的车辆状态
          S(:,1:end) = 0;
          S(A(:,1:end-2)==0&A(:,2:end-1)==1&A(:,3:end)==1)=2;%寻找加速的车
          S(A(:,1:end-2)==0&A(:,2:end-1)==0)=3;%寻找停车的车
          S(A(:,1:end-2)==0&A(:,2:end-1)==1&A(:,3:end)==0)=1;%寻找减速行驶的车
          %确定最后2两个元胞的状态
          Q(:,1:end) = 0;
          Q(A(:,end-1)==0&A(:,end)==0) = 1;%
          Q(A(:,end-1)==0&A(:,end)==1) = 2;
          Q(A(:,end-1)==1&A(:,end)==0) = 2;
          Q(:,end) = 1;
          %获得所有元胞状态
          Acc = [ S Q ];
      end
      %根据当前状态改变元胞位置
      %匀速运行车辆向前走1格
      A( Acc(:,1:end)==1 ) = 1;
      A( [ zeros(nc,1) Acc(:,1:end-1)]==1 ) = 0;
      %高速运行车辆向前走2格
      A( Acc(:,1:end)==2) = 1;
      A( [ zeros(nc,2) Acc(:,1:end-2)]==2) = 0;
      %计算平均速度、换道频率、车流密度等参数
      %获得运行中的车辆数目N
      matN = A<1;
      N = sum(sum(matN));
      %获得运行中的车辆速度之和V
      E = S((S==1)|(S==2));
      V = sum(E);
      %计算此时刻的车流密度并保存
      ap(n) = N/( nc*(nl+2) );
      %计算此时刻的平均速率并保存
      if(N~=0&&n>nl/2)
          av(c) = V/N;
          c = c+1;
      end
      %在车道入口处随机引入新的车辆
      A = [ round(fp*rand(nc,1))&A(1:nc,1) A(:,2:end)];
      A(A~=0)=1;
      %将新的车辆加入元胞矩阵中
      B(2:2:2*nc,:)=A;
      %显示交通流图
      set(H,'CData',B);
      %仿真步长
      pause(dt);
   end
   %仿真结束，计算结果
   d = ad;
   p = mean(ap);
   v = sum(av)/c;
end