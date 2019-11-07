# 开发注意事项

## windows环境下pip包的升级
1、进入虚拟环境，执行命令(pip install -U pip)进行升级。

2、如果1中升级操作失败，则结合项目下的get-pip.py进行升级(python get-pip.py)

## windows环境下ldap依赖包的安装问题
python-ldap由以前的旧版本升级到3.2.0版本，windows环境下安装步骤如下：

1、在python控制台执行如下语句：

import pip._internal

print(pip._internal.pep425tags.get_supported())

2、控制台会输出下面的内容(不同的环境输出的结果不同)

[('cp36', 'cp36m', 'win32'), ('cp36', 'none', 'win32'),

('py3', 'none', 'win32'), ('cp36', 'none', 'any'),

('cp3', 'none', 'any'), ('py36', 'none', 'any'),

('py3', 'none', 'any'), ('py35', 'none', 'any'),

('py34', 'none', 'any'), ('py33', 'none', 'any'),

('py32', 'none', 'any'), ('py31', 'none', 'any'),

('py30', 'none', 'any')]

3、进入网址https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap找到对应的安装包

python_ldap‑2.5.2‑cp27‑cp27m‑win32.whl

python_ldap‑2.5.2‑cp27‑cp27m‑win_amd64.whl

python_ldap‑3.2.0‑cp27‑cp27m‑win32.whl

python_ldap‑3.2.0‑cp27‑cp27m‑win_amd64.whl

python_ldap‑3.2.0‑cp35‑cp35m‑win32.whl

python_ldap‑3.2.0‑cp35‑cp35m‑win_amd64.whl

python_ldap‑3.2.0‑cp36‑cp36m‑win32.whl

python_ldap‑3.2.0‑cp36‑cp36m‑win_amd64.whl

python_ldap‑3.2.0‑cp37‑cp37m‑win32.whl

python_ldap‑3.2.0‑cp37‑cp37m‑win_amd64.whl

python_ldap‑3.2.0‑cp38‑cp38m‑win32.whl

python_ldap‑3.2.0‑cp38‑cp38m‑win_amd64.whl

匹配规则：以2中的('cp36', 'cp36m', 'win32')为例，则对应上述列表中的python_ldap‑3.2.0‑cp36‑cp36m‑win32.whl


4、结合2中的适应调价在3中的下载文件列表下载文件，执行命令pip install *.whl即可。

## gitignore相关配置
1、在Pycharm插件中找到.ignore插件，并安装

2、安装完成后在项目下的.ignore文件中填写要忽略文件的路径名称即可。

## swagger api文档访问地址
浏览器访问 http://{ip}:{port}/api/docs 即可。

## 基于flask框架开发可以参考demo模块

1、路由的定义统一在模块下的__init__.py文件中。

2、路由统一都对应视图类（CBV模式），动作都通过HTTP Method区分。

3、路由模块中命名都统一遵循如下样例规范

bp_demo = Blueprint('demo', __name__, url_prefix='/api/v1')

api = Api(bp_demo)

api.add_resource(DemoOneListResource, '/demo-ones')

api.add_resource(DemoOneResource, '/demo-ones/<demo_one_id>')


### 路由的命名统一遵循bp_{模块名}
视图类的命名统一以Resource结尾，如DemoOneListResource、DemoOneResource

创建、查询列表方法尽量放在{module}ListResource中，其余单个实体的处理放在{module}Resource中

## 统一标准返回样式

| 字段名称  |是否必须|备注信息|样例|
| --- | --- |--- |---|
| status |是|状态码|200|
|  msg |是|提示信息|success|
|  data |否|返回数据|{name: "user01", id: "0001"}|


## 统一信息常量定义
场景：在后端接口中抛出异常的时候往往需要返给前端提示文字（比如：查询的应用已删除、参数输入有误等等）

建议：将这些文字性的提示语统一归类到common/message.py文件中统一管理，按照模块分类。

msg_const.SYSTEM_CONFIG_404 = "未找到系统配置"

msg_const.APPLICATION_404 = "项目找不到了"

msg_const.LDAP_CONNECTION_500 = "LDAP服务器连接异常"

msg_const.USER_INPUT_500 = "用户名或密码为空"

常量定义原则：<模块名称大写>_<错误类型>_<状态码>


## 统一接口返回
Response

    {
        "status": 状态码,
        "msg": 信息,
        "data": {object对象dict}
    }
    {
        "status": 状态码,
        "msg": 信息,
        "data": {
            "total": 结果总数，
            "result": [结果列表]
        }   
    }
    {
        "status": 状态码,
        "msg": 信息,
        "data": [结果列表，不需要分页]
    }

## 分页查询入参
|参数名称|参数类型|是否必须|备注|
| --- | --- |--- |---|
|page|	Integer|是|	页码，从1开始|
|limit|	Integer|是|	每页条数，-1：表示查询全部数据，pageNo无效|
|sort|	String|否|	排序, 例：name asc 和 name desc|


## 测试类的编写
采用统一继承apis.base.base_test.BaseTest的方式，然后在测试类中实现父类的setUp方法即可。


```
class TestApplication(BaseTest):
    def setUp(self):
        super(TestApplication, self).setUp()
        self.app_tool = ApplicationTool()

    def test_get_app(self):
        query = Application.query.all()
        res = Serializer.as_dict(query)
        print(res)
```

## 线上项目的启动与停止
### 启动项目
1、进入虚拟环境（启动项目一定要在虚拟环境中进行）
2、运行项目目录下的start.sh脚本文件即可。项目启动的过程中默认会kill掉占用5002端口的服务，所以这里需要注意。

### 停止项目
直接运行stop.sh文件即可，不需要进入虚拟环境。

