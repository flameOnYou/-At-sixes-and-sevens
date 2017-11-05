### 主要入库说明
#### 表结构说明
- makret[市场表]  

value | content
---|---
id| 自增长唯一id
name | 市场
updateTime | 更新时间
abbreviate | 市场缩写+id


- symbol[商品表]  

value | content
---|---
id| 自增长唯一id
name | 商品名称
updateTime | 更新时间
unit_level|能获取到的最小时间级别
belong_market | 所属市场id
get_price_unit| 爬取时间间隔
contant_lv|所含有的时间周期数据,1,5,10分钟...

- 表名:市场缩写_id_商品唯一id
    tip:该表由时间级别触发

value | content
---|---
id | 自增长id
name|商品名称
isTick | 是否tick级别
timestamp|时间戳
price|当前价格

- 表名:市场缩写_id_商品唯一id_时间级别 [价格表] 
    tip:该表由时间级别触发

value | content
---|---
id | 自增长id
name|商品名称
timestamp|时间戳
open|开盘价
high|最高价
close|收盘价
low|最低价
vol|成交量

#### 爬虫架构说明
- 定时器时间级别  **[由我提供] **
     - 每日更新市场表和商品列表表格  
     - 0.5毫秒为基本时间单位一帧更新所有价格表**[并发策略由开发者提供]**
     - 提供数据修复脚本,命令需求,输入价格表的唯一id,时间段,可以价格表
     - 分布式ip分布进行脚本启动，设置浏览器各项参数，防止反爬虫策略
     - 录入数据的时候根据最小级别生成更高级别的价格数据,例如AAA股票录入一分钟数据的时候,如果到达五分钟的节点，在"市场缩写_id_商品唯一id_5"表中插入一条数据
     - 每日市场结束时清空 :市场缩写_id_商品唯一id表
     - 定时备份数据到mysql
- 数据库  
     - 直接入库,数据库使用mongodb
     - 备份数据库采用mysql+缓存层**[缓存层策略由我提供]**
    
#### 数据API参考
##### market表: 
    market表需要根据下面的额symbols表生成，来源自寻，脚本自建

##### symbols表:
    
    期货市场
    - address:http://quote.hexun.com/futures/newfutures.aspx  
    - param:market
    
param| content
---|---
1 | 上海
2 | 大连
3|郑州
4|全部主力 
9|全部股指期货
    股票市场  
        address:https://hq.gucheng.com/gpdmylb.html
        
##### 价格表:
address:http://quote.hexun.com/stock/stock.aspx  
param:type,market

type:
param | content
---|---
2 | A股
3 | B股

market:

param | content
---|---
0 | 全部
1 | 沪市
2 |深市







    

    


    

