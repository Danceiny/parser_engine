# parser_engine changelog
### v0.1.6
>Data: 2019-05-17
**DONE**
- [x] `ItemClassLoader`的settings使用普通`get`方法获取具体配置项，以支持`dict`类型的settings参数

### v0.1.5
>Date: 2019-05-09

**DONE**:
- [x] 新增`extract_all_keys`参数，为真值时可直接提取JSON响应的所有字段（可以理解为，`extract_keys=*`）
- [x] 修复`PEParser._parse_text`bug：在没有`parent`参数且响应的json不是JSONArray状况下，支持的解析参数与API标准不一致
- [x] 修复context参数为空时crawled_time字段缺失
- [x] `_parse_start_url`调用时传入不存在的`tpl_index_or_id`时抛出异常，而非静默返回None

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