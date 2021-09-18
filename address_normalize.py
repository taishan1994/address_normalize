import json
import trie


class AddressParser:
    def __init__(self):
        self.data = self.load_everything()

    def load_everything(self):
        """
        加载相关的字典
        :return:
        """
        with open('./data/nor_prov_to_prov.json','r') as fp:
            prov_to_prov = json.loads(fp.read())
        with open('./data/nor_city_to_prov.json','r') as fp:
            city_to_prov = json.loads(fp.read())
        with open('./data/nor_county_to_city.json','r') as fp:
            county_to_city = json.loads(fp.read())
        with open('./data/nor_street_to_county.json','r') as fp:
            street_to_county = eval(fp.read())
        with open('./data/nor_city_to_city.json','r') as fp:
            city_to_city =  eval(fp.read())
        data = {
            'prov_to_prov':prov_to_prov,
            'city_to_prov':city_to_prov,
            'county_to_city':county_to_city,
            'street_to_county':street_to_county,
            'city_to_city':city_to_city,
        }
        return data

    def build_trie(self):
        """
        构造前缀树
        :return:
        """
        prov_trie = trie.Trie()
        city_trie = trie.Trie()
        county_trie = trie.Trie()
        street_trie = trie.Trie()
        with open('./data/province.txt','r') as fp:
            province = fp.read().strip().split('\n')
        with open('./data/city.txt','r') as fp:
            city = fp.read().strip().split('\n')
        with open('./data/county.txt','r') as fp:
            county = fp.read().strip().split('\n')
        with open('./data/street.txt','r') as fp:
            street = fp.read().strip().split('\n')
        for prov in province:
            prov_trie.insert(prov)
        for cy in city:
            city_trie.insert(cy)
        for coun in county:
            county_trie.insert(coun)
        for stre in street:
            street_trie.insert(stre)
        trie_data = {
            'province_trie':prov_trie,
            'city_trie':city_trie,
            'county_trie':county_trie,
            'street_trie':street_trie,
        }
        return trie_data

    def distinct(self, data):
        """
        :param data: [[0, 1, '徐州'], [0, 2, '徐州市']]
        :return: [0, 2, '徐州市']
        """
        tmp_data = [i for i in data if '街道' in i[2]]
        if len(tmp_data) == 0:
            data = sorted(data, key=lambda x:len(x[2]), reverse=True)
        else:
            print(tmp_data)
            data = sorted(tmp_data, key=lambda x:len(x[2]), reverse=True)
        return data[0]

    def post_process(self, province, city, county, street, other):
        """
        后处理操作，进行补全
        :param province:
        :param city:
        :param county:
        :param street:
        :return:
        """
        if street != '':
            county_tmp = self.data['street_to_county'][street]
            if len(county_tmp) == 1 and county == '':
                county = county_tmp[0]
        if county != '':
            if ',' in county:
                city = county.split(',')[0]
            else:
                city_tmp = self.data['county_to_city'][county]
                if len(city_tmp) == 1 and city == '':
                    city = city_tmp[0]
        if city != '':
            city = self.data['city_to_city'][city]
            province_tmp = self.data['city_to_prov'][city]
            if province == '':
                province = province_tmp
        if province != '':
            province = self.data['prov_to_prov'][province]
        return province, city, county, street, other

    def parse2(self, addr, trie_processor):
        prov_trie = trie_processor['province_trie']
        city_trie = trie_processor['city_trie']
        county_trie = trie_processor['county_trie']
        street_trie = trie_processor['street_trie']
        province = ''
        city = ''
        county = ''
        street = ''
        other = ''
        province_tmp = prov_trie.get_lexicon(addr)
        tmp_addr = addr
        city_tmp = city_trie.get_lexicon(tmp_addr)
        street_tmp = street_trie.get_lexicon(tmp_addr)
        county_tmp = county_trie.get_lexicon(tmp_addr)
        if len(province_tmp) != 0:
            province_tmp = self.distinct(province_tmp)
        if len(city_tmp) != 0:
            city_tmp = self.distinct(city_tmp)
        if len(county_tmp) != 0:
            county_tmp = self.distinct(county_tmp)
        if len(street_tmp) != 0:
            print('输入street_tmp：', street_tmp)
            street_tmp = self.distinct(street_tmp)
        print(province_tmp)
        print(city_tmp)
        print(county_tmp)
        print(street_tmp)


    def parse(self, addr, trie_processor):
        prov_trie = trie_processor['province_trie']
        city_trie = trie_processor['city_trie']
        county_trie = trie_processor['county_trie']
        street_trie = trie_processor['street_trie']
        province = ''
        city = ''
        county = ''
        street = ''
        other = ''
        province_tmp = prov_trie.get_lexicon(addr)
        tmp_addr = addr
        if len(province_tmp) != 0:
            province_tmp = self.distinct(province_tmp)
            province = province_tmp[2]
            tmp_addr = tmp_addr[int(province_tmp[1])+1:]
            city_tmp = city_trie.get_lexicon(tmp_addr)
            if len(city_tmp) != 0:
                city_tmp = self.distinct(city_tmp)
                city = city_tmp[2]
                tmp_addr = tmp_addr[int(city_tmp[1])+1:]
                county_tmp = county_trie.get_lexicon(tmp_addr)
                if len(county_tmp) != 0:
                    county_tmp = self.distinct(county_tmp)
                    county = county_tmp[2]
                    tmp_addr = tmp_addr[int(county_tmp[1])+1:]
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
                else:
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
            else:
                county_tmp = county_trie.get_lexicon(tmp_addr)
                if len(county_tmp) != 0:
                    county_tmp = self.distinct(county_tmp)
                    county = county_tmp[2]
                    tmp_addr = tmp_addr[int(county_tmp[1])+1:]
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
                else:
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
        else:
            city_tmp = city_trie.get_lexicon(tmp_addr)
            if len(city_tmp) != 0:
                city_tmp = self.distinct(city_tmp)
                city = city_tmp[2]
                tmp_addr = tmp_addr[int(city_tmp[1])+1:]
                county_tmp = county_trie.get_lexicon(tmp_addr)
                if len(county_tmp) != 0:
                    county_tmp = self.distinct(county_tmp)
                    county = county_tmp[2]
                    tmp_addr = tmp_addr[int(county_tmp[1])+1:]
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:

                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
                else:
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1]):]
                    else:
                        other = tmp_addr
            else:
                county_tmp = county_trie.get_lexicon(tmp_addr)
                if len(county_tmp) != 0:
                    county_tmp = self.distinct(county_tmp)
                    county = county_tmp[2]
                    tmp_addr = tmp_addr[int(county_tmp[1])+1:]
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
                else:
                    street_tmp = street_trie.get_lexicon(tmp_addr)
                    if len(street_tmp) != 0:
                        street_tmp = self.distinct(street_tmp)
                        street = street_tmp[2]
                        other = tmp_addr[int(street_tmp[1])+1:]
                    else:
                        other = tmp_addr
        return province, city, county, street, other



if __name__ == '__main__':
    addressParser = AddressParser()
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
        # addressParser.parse2(sen, trie_processor)
        province, city, county, street, other = addressParser.parse(sen, trie_processor)
        province, city, county, street, other = addressParser.post_process(
            province, city, county, street, other
        )
        print('===========================')
        print('text=', sen)
        print('省：', province)
        print('市：', city)
        print('区：', county)
        print('街道：', street)
        print('地址：', other)
        print('===========================')

