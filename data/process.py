import json
from collections import defaultdict

def get_prov_to_prov(in_path, out_path):
    # out_file = open(out_path,'w',encoding='utf-8')
    tmp = {}
    with open(in_path,'r') as fp:
        lines = fp.read().strip().split('\n')
        for line in lines:
            tmp[line] = line
            if '市' in line:
                tmp[line[:-1]] = line
            elif '省' in line:
                tmp[line[:-1]] = line
            else:
                if '内蒙古' in line:
                    tmp['内蒙古'] = line
                elif '广西' in line:
                    tmp['广西'] = line
                elif '西藏' in line:
                    tmp['西藏'] = line
                elif '宁夏' in line:
                    tmp['宁夏'] = line
                elif '新疆' in line:
                    tmp['新疆'] = line
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(json.dumps(tmp, ensure_ascii=False))
    # out_file.close()

def get_city_to_prov(in_path, out_path):
    tmp = {}
    with open(in_path,'r') as fp:
        data = json.loads(fp.read())
        provs = data.keys()
        for prov in provs:
            cities = data[prov]
            for city in cities:
                tmp[city] = prov
                if '市' == city[-1]:
                    tmp[city[:-1]] = prov
                elif '区' == city[-1]:
                    tmp[city[:-1]] = prov
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(json.dumps(tmp, ensure_ascii=False))

def get_county_to_city(in_path ,out_path):
    tmp = defaultdict(list)
    with open(in_path,'r') as fp:
        data = json.loads(fp.read())
        province = data.keys()
        for prov in province:
            cities = data[prov].keys()
            for city in cities:
                print(city)
                if city == '市辖区':
                    counties = data[prov][city]
                    for county in counties:
                        tmp[county].append(prov + ',' + '市辖区')
                elif '省直辖' in city:
                    counties = data[prov][city]
                    for county in counties:
                        tmp[county].append(prov + ',' + '省直辖')
                elif '自治区直辖' in city:
                    counties = data[prov][city]
                    for county in counties:
                        tmp[county].append(prov + ',' + '自治区直辖')
                else:
                    counties = data[prov][city]
                    for county in counties:
                        tmp[county].append(city)
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(json.dumps(tmp, ensure_ascii=False))

def get_street_to_county(in_path ,out_path):
    tmp = defaultdict(list)
    with open(in_path,'r') as fp:
        data = json.loads(fp.read())
        province = data.keys()
        for prov in province:
            cities = data[prov].keys()
            for city in cities:
                print(city)
                if city == '市辖区':
                    counties = data[prov][city]
                    for county in counties:
                        streets = data[prov][city][county]
                        for street in streets:
                            tmp[street].append(prov + ',' + '市辖区')
                elif city == '县':
                    counties = data[prov][city]
                    for county in counties:
                        streets = data[prov][city][county]
                        for street in streets:
                            tmp[street].append(prov + ',' + '县')
                else:
                    counties = data[prov][city]
                    for county in counties:
                        streets = data[prov][city][county]
                        for street in streets:
                            tmp[street].append(county)
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(json.dumps(tmp, ensure_ascii=False))


def get_city_to_city(in_path, out_path):
    tmp = {}
    with open(in_path,'r') as fp:
        data = json.loads(fp.read())
        provs = data.keys()
        for prov in provs:
            cities = data[prov]
            for city in cities:
                if '市' == city[-1]:
                    tmp[city] = city
                    tmp[city[:-1]] = city
                elif '区' == city[-1]:
                    tmp[city] = city
                    tmp[city[:-1]] = city
                else:
                    tmp[city] = city
    with open(out_path, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(tmp, ensure_ascii=False))

def get_city(in_path ,out_path):
    with open(in_path,'r') as fp:
        lines = eval(fp.read())
        tmp = lines.keys()
        tmp = "\n".join(tmp)
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(tmp)

def get_county(in_path ,out_path):
    with open(in_path,'r') as fp:
        lines = eval(fp.read())
        tmp = lines.keys()
        tmp = "\n".join(tmp)
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(tmp)

def get_street(in_path ,out_path):
    with open(in_path,'r') as fp:
        lines = eval(fp.read())
        tmp = lines.keys()
        tmp = "\n".join(tmp)
    with open(out_path,'w',encoding='utf-8') as fp:
        fp.write(tmp)

if __name__ == '__main__':
    # get_prov_to_prov('province.txt','nor_prov_to_prov.json')
    # get_city_to_prov('province_city.json','nor_city_to_prov.json')
    # get_county_to_city('province_city_county.json','nor_county_to_city.json')
    # get_street_to_county('province_city_county_street.json', 'nor_street_to_county.json')
    # get_city('nor_city_to_prov.json', 'city.txt')
    # get_county('nor_county_to_city.json', 'county.txt')
    # get_street('nor_street_to_county.json', 'street.txt')
    get_city_to_city('province_city.json','nor_city_to_city.json')