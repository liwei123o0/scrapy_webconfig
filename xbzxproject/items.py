# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


# 行政执行信息字段
class XingZhengXKItem(Item):
    # URL
    crl_30101001 = Field()
    # 网站来源
    crl_30101003 = Field()
    # 网站类型
    crl_30101004 = Field()
    # 行政相对人名称
    crl_10101001 = Field()
    # 行政许可决定书文号
    crl_10401001 = Field()
    # 项目名称(双公示)
    crl_10401002 = Field()
    # 审批类别
    crl_10401003 = Field()
    # 许可内容
    crl_10401004 = Field()
    # 统一社会信用代码
    crl_10101002 = Field()
    # 组织机构代码
    crl_10101004 = Field()
    # 工商登记码
    crl_10101003 = Field()
    # 税务登记号
    crl_10101005 = Field()
    # 法定代表人姓名
    crl_10101007 = Field()
    # 许可决定日期
    crl_10401005 = Field()
    # 许可截止期
    crl_10401006 = Field()
    # 许可机关
    crl_10401007 = Field()
    # 当前状态
    crl_10401009 = Field()
    # 地方编码
    crl_10401008 = Field()


# 行政处罚信息字段
class XingZhengCFItem(Item):
    # URL
    crl_30101001 = Field()
    # 网站来源
    crl_30101003 = Field()
    # 网站类型
    crl_30101004 = Field()
    # 行政相对人名称
    crl_10101001 = Field()
    # 行政处罚决定书文号
    crl_20201001 = Field()
    # 处罚名称
    crl_20201002 = Field()
    # 处罚类别
    crl_20201003 = Field()
    # 处罚事由
    crl_20201004 = Field()
    # 处罚依据
    crl_20201005 = Field()
    # 统一社会信用代码
    crl_10101002 = Field()
    # 组织机构代码
    crl_10101004 = Field()
    # 工商登记码
    crl_10101003 = Field()
    # 税务登记号
    crl_10101005 = Field()
    # 法定代表人姓名
    crl_10101007 = Field()
    # 处罚结果
    crl_20201007 = Field()
    # 处罚决定日期
    crl_20201006 = Field()
    # 处罚机关
    crl_20201008 = Field()
    # 当前状态
    crl_20201009 = Field()
    # 地方编码
    crl_20201010 = Field()


# 招投标字段
class zhaotou_zhaobItem(Item):
    # URL
    crl_30101001 = Field()
    # 公告原文
    crl_30101002 = Field()
    # 网站来源
    crl_30101003 = Field()
    # 网站类型
    crl_30101004 = Field()
    # 项目名称
    crl_10416001 = Field()
    # 项目编号
    crl_10416007 = Field()
    # 项目种类
    crl_10416008 = Field()
    # 行政区域
    crl_10416002 = Field()
    # 公告时间
    crl_10416003 = Field()
    # 报名起始时间
    crl_10416010 = Field()
    # 报名终止时间
    crl_10416011 = Field()
    # 投标起始时间
    crl_10416012 = Field()
    # 投标截至时间
    crl_10416013 = Field()
    # 开标时间
    crl_10416014 = Field()
    # 项目估算
    crl_10416015 = Field()
    # 投标保证金
    crl_10416016 = Field()
    # 公告类型
    crl_10416017 = Field()
    # 招标单位
    crl_10416018 = Field()
    # 招标单位联系地址
    crl_10416019 = Field()
    # 招标单位负责人
    crl_10416020 = Field()
    # 招标单位联系方式
    crl_10416021 = Field()
    # 代理机构
    crl_10416022 = Field()
    # 代理机构联系地址
    crl_10416023 = Field()
    # 代理机构负责人
    crl_10416024 = Field()
    # 代理机构联系方式
    crl_10416025 = Field()


# 工商基本信息
class GsbasicItem(Item):
    """基本信息
    """
    # 企业名称
    name = Field()
    # 主体识别码
    XY10101001 = Field()
    # 联系电话
    XY10102014 = Field()
    # 电子邮箱
    XY10111006 = Field()
    # 网站地址
    XY10405003 = Field()
    # 法定代表人（负责人）姓名
    XY10101007 = Field()
    # 注册资本（万元）
    XY10102001 = Field()
    # 成立日期
    XY10102004 = Field()
    # 信用主体状态
    XY10101013 = Field()
    # 所属行业
    XY10101014 = Field()
    # 登记证号
    XY10101003 = Field()
    # 企业类型
    XY10101012 = Field()
    # 组织机构代码
    XY10101004 = Field()
    # 经营期限起
    XY10102005 = Field()
    # 经营期限止
    XY10102006 = Field()
    # 登记机关
    XY10102008 = Field()
    # 核准日期
    XY10102009 = Field()
    # 统一社会信用代码
    XY10101002 = Field()
    # 住所
    XY10101010 = Field()
    # 经营范围
    XY10102003 = Field()
    """股东信息
    """
    # 投资人名称
    XY10110001 = Field()
    # 认缴出资额（万元）
    XY10110005 = Field()
    """高管信息
    """
    # 姓名
    XY10109001 = Field()
    # 职务
    XY10109004 = Field()
    """对外投资
    """
    # 融资人
    XY10113001 = Field()
    # 融资数额
    XY10113002 = Field()
    """法律诉讼
    """
    # 判决书名称
    XY20301004 = Field()
    # 判决书编号
    XY20301005 = Field()
    # 文书正文
    XY20301007 = Field()
    """变更信息
    """
    # 变更日期
    XY10105004 = Field()
    # 变更类型
    XY10105005 = Field()
    # 变更前内容
    XY10105006 = Field()
    # 变更后内容
    XY10105007 = Field()
    """商标信息
    """
    # 商标名称
    XY10406005 = Field()
    # 注册号
    XY10406001 = Field()
    # 国际分类号
    XY10406003 = Field()
    # 状态
    XY10406011 = Field()
    # 注册日期
    XY10406002 = Field()
    # 图样
    XY10406004 = Field()
    """网站备案
    """
    # 网站（网店）名称
    LS10101001 = Field()
    # 网站（网店）网址
    LS10405002 = Field()
    # 备案号
    XY10405004 = Field()
    # 状态
    XY10405005 = Field()
    # 审核时间
    XY10405006 = Field()
    # 主办单位性质
    XY10405007 = Field()
    """著作权
    """
    # 软件全称
    XY10419001 = Field()
    # 软件简称
    XY10419013 = Field()
    # 软件登记号
    XY10419003 = Field()
    # 软件分类号
    XY10419002 = Field()
    # 软件版本号
    XY10419004 = Field()
    # 软件首次发表日期
    XY10419006 = Field()
    # 软件登记日期
    XY10419005 = Field()
    """招聘信息
    """
    # 职位名称
    XY10417001 = Field()
    # 工作地点
    XY10417002 = Field()
    # 薪资
    XY10417003 = Field()
    # 发布时间
    XY10417004 = Field()
    #招聘人数
    XY10417005 = Field()


    # URL
    XY30101001 = Field()
    # 网站来源
    XY30101003 = Field()
    # 网站类型
    XY30101004 = Field()
