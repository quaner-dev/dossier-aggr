1. 如果要保证 model 和 schema 相互结合，就需要保证两个模块之间没有关联关系存在，也就是 relation 存在，当前的情况是 model 是基础类，schema 来引用 model 中的类
2. 可以使用apirouter来分离路由
3. 使用service分离业务代码