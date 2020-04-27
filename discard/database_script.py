# # 控制台
# show DATABASES ;
# use ui
# show tables;
# show columns from material;
# create table material (
#   id int not null auto_increment,
#   qiniu_key varchar(200) not null COMMENT '七牛key',
#   main_img_flag BOOLEAN DEFAULT FALSE COMMENT '是否主图',
#   category VARCHAR(50) COMMENT '大分类',
#   folder VARCHAR(100) COMMENT '文件夹名',
#   title VARCHAR(200) COMMENT '单文件名',
#   postfix VARCHAR(10) COMMENT '文件后缀',
#   size float UNSIGNED COMMENT '文件大小',
#   views INTEGER COMMENT '浏览数',
#   downloads INTEGER COMMENT '下载数',
#   hash VARCHAR(100) COMMENT '七牛文件hash值',
#   create_time datetime,
#
#   primary key (id)
# );
# drop table material; # 完全删除表数据和结构
# # 查找所有数据
# select * from material where category="mobile_kit" and main_img_flag=True order by downloads desc,views desc;
# select * from ( select * from material where category="mobile_kit" and main_img_flag=True order by downloads desc,views desc ) as t limit 0,20;
# SELECT * from material where category="mobile_interface"; # 某一目录下素材
# select * from material where category="mobile_interface" and main_img_flag=True limit 120,20;#分页
# select * from material where category="mobile_kit" and main_img_flag=True limit 20,20;#分页
# select DISTINCT folder from material;
# # 浏览量
#
# update material set views=views+1 where folder="手机 套件 tab metro 磨砂 透明 暖色" and material.main_img_flag=True;
# select views from material where folder="手机 套件 tab metro 磨砂 透明 暖色"  and material.main_img_flag=True;
# select * from material where views>0;
# # 下载量
# select * from material where folder="手机 个人页 多彩 聊天"