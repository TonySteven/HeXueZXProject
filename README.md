# 和学在线自动刷课项目

## 简介

> 时间: 2022/04/20 项目版本,如果和学在线后台系统更新需重新设计.

### 内容简介

```

需求背景
1. 实现网页版自动刷课功能

设计思路

1、通过seleniumn模拟点击动作.(简单安全)

2、研究接口请求流程,直接模拟接口请求

```

### 接口请求流程图(暂时没用此方案,seleniumn模拟点击动作即可实现.)

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h1fzozyl57j21ct0u0dkq.jpg)

### 使用

#### 1. 安装webdriver (win/linux) 自行百度

mac: 执行 `brew install chromedriver` 即可

#### 2. 安装 python3环境(自行百度)

##### 2.1 安装selenium

执行 `pip install selenium`

#### 3.配置并选择文件运行即可.

##### 3.1 配置

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h1gcbsd0xyj21210u041x.jpg)

##### 3.2 运行

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h1gc4gbbjuj20u01nnadb.jpg)

##### 3.3 运行后注意点

需要把浏览器放到激活桌面上,pyCharm可以放到后台.

建议放到桌面并实时查看运行日志(如下图所示),如果发送报错异常,重新运行即可.

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h1kkhejutwj21d40u0n1z.jpg)



