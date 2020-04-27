# # 未使用orm，具体字段以数据库为准

# class Material(object):
#     """
#     本地素材库主表 。 由QiniuRaw数据加工而来，包含额外数据如访问统计
#     """
#     qiniu_key = models.CharField(verbose_name='七牛key', max_length=200)
#     main_img_flag = models.BooleanField(verbose_name='是否主图', default=False)
#
#     category = models.CharField(verbose_name='一/类别', max_length=50)
#     folder = models.CharField(verbose_name='二/文件夹', max_length=50)
#     title = models.CharField(verbose_name='三/文件名', max_length=200, blank=True)
#     postfix = models.CharField(verbose_name='文件后缀', max_length=20, blank=True)
#     size = models.CharField(verbose_name='文件名', max_length=20, blank=True)
#     views = models.IntegerField(verbose_name='浏览量', default=0)
#     downloads = models.IntegerField(verbose_name='下载量', default=0)
#
#     hash = models.CharField(verbose_name='文件哈希值', max_length=200)
#     created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
#     last_modified_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
#
#
#     # Tag
#     tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
#
#     def __str__(self):
#         return self.title
#
#     # 数据库取出时排序
#     class Meta:
#         ordering = ['-last_modified_time']
#
#
# class Tag(models.Model):
#     """
#     标签。 跟文章多对多
#     """
#     name = models.CharField('标签名', max_length=20)
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     last_modified_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = '标签'
#
#
# # 七牛api 资源列举 http://developer.qiniu.com/code/v6/api/kodo-api/rs/list.html
# # 返回格式
# # {
# #     "marker": "<marker string>",
# #     "commonPrefixes": [
# #         "xxx",
# #         "yyy"
# #     ],
# #     "items": [
# #         {
# #             "key"：     "<key           string>",
# #             "putTime":   <filePutTime   int64>,
# #             "hash":     "<fileETag      string>",
# #             "fsize":     <fileSize      int64>,
# #             "mimeType": "<mimeType      string>",
# #             "customer": "<endUserId     string>"
# #         },
# #         ...
# #     ]
# # }
#
#
# # #接口规格
# # bucket=qiniu-ts-demo&prefix=00&limit=2&delimiter=%2F