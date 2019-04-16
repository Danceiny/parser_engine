# parser_engine changelog


### v0.1.4
>Date: 2019-04-16

**DONE**:

- [x] `ItemClassloader`的相关优化：
    - 增加`load`方法，支持绝对路径的类加载
    - `PEParser`实例化的时候即加载`itemname`参数对应的类
- [x] `TaskRequest`增加了`url`有效性检查。
- [x] `utils`增加了以下方法：
    - `is_url(url)`
    - `item2dict(item)`
    
### < v0.1.4

抱歉，以前忘记写了。