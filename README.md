## 洗浴、住宿、娱乐中心系统
### 包含手牌发放、房间住宿和其他消费等
### 以可视化的方式计算每日收入，每月收入
### 后台管理包含rbac权限、pop组件使用、stark组件应用
# CRM后台管理系统
> 基于Django：包含可拆卸 权限组件rbac 与 stark插件 可以单独取出代码并运用到任意后端开发项目中。 该套CRM系统就是用rbac组件+stark组件开发的《洗浴管理系统》业务
**权限菜单**

**权限分配**

**用户管理**


# 环境
- Django 2.
- Python 3.5
- Bootstrap v3

# 包含
- Rbac 权限组件
- Stark 路由与数据库操作组件
- crm 业务板块

    
# 开发概述
1. **基础业务处理**
    

2. **住宿管理**
    

3. **洗浴管理**
    
    
4. **应用rbac组件**


# 准备流程
> 流程:先通过stark组件完成业务开发，再套上rbac权限（stark放在rbac的app上）因为2个组件都有样式！可分离

> 准备：创建项目>数据库迁移

# 开发
1. 洗浴管理
2. 住宿管理
3. 用户管理
    - 用户基本操作
    - 添加页面 增加确认密码字段并未密码形式，编辑页面删除密码字段
    - 重置密码

4. 权限组件应用
        - 应用
        - 粒度控制


5.数据可视化（echart+python）
![Image](https://github.com/HQCfly/SpringCenter/blob/master/imageFile/1.png)
![Image](https://github.com/HQCfly/SpringCenter/blob/master/imageFile/2.png)