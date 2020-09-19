# cookies_pool
简单粗暴的方式的实现自动化登录及Cookies管理， 通过`pyppeteer`模拟登录过程并提取登陆成功后的Cookies信息。


为什么说简单粗暴呢?

原因是实现的方式是非常直接的根据页面标签元素特征定位后模拟点击或者输入文本操作来实现这些功能。


## 使用前说明

依赖环境:
- 编程语言: `Python3`
- 数据存储: `redis`
- 支持平台: 全平台

## 使用前需要做的工作

1. 安装依赖包: `pip install -r requirements.txt`
2. 安装redis: 访问[redis官网](https://redis.io)了解安装方法


## 功能使用说明

支持功能说明：
1. 账号信息管理
2. cookies信息管理
3. 博客文章自动发布(暂时不完善,因为不同平台发布方式有些不同,暂时无法统一实现，而使用API接口似乎更合理一些,所以此功能似乎有些鸡肋)

### 账号信息管理
> 就是用户名和密码信息管理，用于登录输入了。

使用方法：
```sh
./cookies_pool.py -m csdn -s "username|password"    # 设置CSDN的用户名和密码(用竖线分割)
./cookies_pool.py -m csdn -l csdn.txt               # 设置CSDN的用户名和密码文件(文件中每行一个账号,格式:"username|password")
./cookies_pool.py -m csdn -g                        # 查看CSDN的用户名和密码
```

### Cookies信息管理
> 此部分包括`模拟登录功能`和`提取Cookies信息功能`两部分.

使用方法:
```sh
./cookies_pool.py -c            # 检查Cookies是否有效, 无效时会模拟登录操作(如果有验证码会暂定30秒等待手工输入验证码)
```

# 说明

暂时实现功能如上所述,如果你喜欢或者想要修改此代码，可以`star`和`fork`此项目。


