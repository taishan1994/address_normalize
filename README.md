# address_normalize
根据地址提取省、市、区/县、街道，并进行标准化

# 目录结构
data：存放数据
--city.txt：城市
--province.txt：省
--county.txt：区、县
--street.txt：街道
--nor_city_to_city.json：城市-城市映射标准化
--nor_city_to_prov.json：根据城市获得省
--nor_county_to_city.json：根据区获得市
--nor_prov_to_prov.json：省-省标准化
--province_city.json：省-城市信息
--province_city_county.json：省-城市-区/县信息
--province_city_county_street.json：省-城市-区/县-街道信息
--process.py：得到上述文件的代码
trie.py：构建省字典树、市字典树、区字典树、街道字典树
address_normalize.py：主运行程序

# 使用方法
```python
from address_normalize import AddressParser
trie_processor = addressParser.build_trie()
sens = [
	'通辽市 > 通辽经济技术开发区',
	'南京市江宁区秣陵街道胜太东路9号(江宁开发区)',
	'扬州市维扬路107号',
	'南京市江宁经济技术开发区将军大道139号',
	'内蒙古自治区呼和浩特市金山开发区金山大街1号',
	'武汉市洪山区邮科院路88号',
	'北京市海淀区北三环西路25号27号楼五层5002室',
	'广州市天河区中山大道西109号大院自编1号楼14楼(仅限办公用途)',
	'上海市吴中路578号',
	'深圳市龙华新区大浪街道华宁路8号明君工业区C栋6楼',
	'上海市青浦区赵巷镇嘉松中路5399号3幢4楼E区499室',
	'佛山市文沙路16号',
	]
for sen in sens:
	province, city, county, street, other = addressParser.parse(sen, trie_processor)
	province, city, county, street, other = addressParser.post_process(
		province, city, county, street, other
	)
	print('===========================')
	print('省：', province)
	print('市：', city)
	print('区：', county)
	print('街道：', street)
	print('地址：', other)
	print('===========================')
```
结果：
```python
===========================
text= 通辽市 > 通辽经济技术开发区
省： 内蒙古自治区
市： 通辽市
区： 通辽经济技术开发区
街道： 
地址： 
===========================
[[0, 3, '秣陵街道']]
===========================
text= 南京市江宁区秣陵街道胜太东路9号(江宁开发区)
省： 江苏省
市： 南京市
区： 江宁区
街道： 秣陵街道
地址： 胜太东路9号(江宁开发区)
===========================
===========================
text= 扬州市维扬路107号
省： 江苏省
市： 扬州市
区： 
街道： 
地址： 维扬路107号
===========================
===========================
text= 南京市江宁经济技术开发区将军大道139号
省： 江苏省
市： 南京市
区： 
街道： 
地址： 江宁经济技术开发区将军大道139号
===========================
===========================
text= 内蒙古自治区呼和浩特市金山开发区金山大街1号
省： 内蒙古自治区
市： 呼和浩特市
区： 
街道： 
地址： 金山开发区金山大街1号
===========================
===========================
text= 武汉市洪山区邮科院路88号
省： 湖北省
市： 武汉市
区： 洪山区
街道： 
地址： 邮科院路88号
===========================
===========================
text= 北京市海淀区北三环西路25号27号楼五层5002室
省： 北京市
市： 海淀区
区： 
街道： 
地址： 北三环西路25号27号楼五层5002室
===========================
===========================
text= 广州市天河区中山大道西109号大院自编1号楼14楼(仅限办公用途)
省： 广东省
市： 广州市
区： 天河区
街道： 
地址： 中山大道西109号大院自编1号楼14楼(仅限办公用途)
===========================
===========================
text= 上海市吴中路578号
省： 上海市
市： 
区： 
街道： 
地址： 吴中路578号
===========================
[[4, 7, '大浪街道']]
===========================
text= 深圳市龙华新区大浪街道华宁路8号明君工业区C栋6楼
省： 广东省
市： 深圳市
区： 龙华区
街道： 大浪街道
地址： 道华宁路8号明君工业区C栋6楼
===========================
===========================
text= 上海市青浦区赵巷镇嘉松中路5399号3幢4楼E区499室
省： 上海市
市： 上海市
区： 上海市,市辖区
街道： 赵巷镇
地址： 嘉松中路5399号3幢4楼E区499室
===========================
===========================
text= 佛山市文沙路16号
省： 广东省
市： 佛山市
区： 
街道： 
地址： 文沙路16号
===========================
```
# 讲在最后
对于省、市而言，即使是江苏、南京这种也能提取出来并进行标准化，而对于赤壁这种区/县不是完整的，就不能够识别出来，你可以通过修改not_county_to_city里面添加{'赤壁':'市'}的映射来解决这种问题，对于区等都可以利用这种方式来解决。