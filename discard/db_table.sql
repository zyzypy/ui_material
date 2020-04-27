# ###### 素材主表 #########



# create table material (
#   id int not null auto_increment,
#   qiniu_key varchar(100) not null COMMENT '七牛key',
#   main_img_flag BOOLEAN DEFAULT FALSE COMMENT '是否主图',
#   category VARCHAR(50) COMMENT '大分类',
#   folder VARCHAR(50) COMMENT '文件夹名',
#   title VARCHAR(50) COMMENT '单文件名',
#   postfix VARCHAR(10) COMMENT '文件后缀',
#   size float UNSIGNED COMMENT '文件大小',
#   views INTEGER COMMENT '浏览数',
#   downloads INTEGER COMMENT '下载数',
#   hash VARCHAR(100) COMMENT '七牛文件hash值',
#   created_time datetime,
#
#   primary key (id)
# );