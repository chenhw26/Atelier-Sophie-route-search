'''
cyowahinn["中和剂·红"] = {
  map_lv: 2
  map_catagory: ["中和剂·红", "中和剂", "燃料"]
  map_source: ["火药", "水"]
} ["中和剂·红", "中和剂", "燃料"] -> ["火药", "水"]

transfer["中和剂"] = {}
  "火药": ["中和剂·红"]
  "水": ["中和剂·红"]
}
'''
import pandas as pd
import re

max_lv = 60 # 最大炼金等级，超过此等级的调和品不会出现在计算结果中
max_step = 4 # 合成路线的长度限制
cannot_cyowa = ['暮色水滴'] # 不能合成的调和品，此处指定的调和品不会出现在计算结果中
target = '絲薇麗銀' # 合成目标
source = ['雲杉木', '木材'] # 素材本身+素材種類

def buildMap():
  cyowahinn, transfer = {}, {}

  df = pd.read_excel('合成表.xlsx')
  for _, item in df.iterrows():
    item_name = item['中文名稱'].strip()
    if int(item['Lv']) > max_lv or item_name in cannot_cyowa: continue
    cyowahinn[item_name] = {}
    cyowahinn[item_name]['map_lv'] = int(item['Lv'])
    cyowahinn[item_name]['map_catagory'] = item['類別'].split('\n')
    cyowahinn[item_name]['map_catagory'].append(item_name)
    cyowahinn[item_name]['map_source'] = []
    for i in range(1, 5):
      if not pd.isna(item['材料%d' % (i)]):
        source = re.sub(r'[^\u4e00-\u9fa5]', '', item['材料%d' % (i)])
        cyowahinn[item_name]['map_source'].append(source)
  
  for cyowahinn_name, cyowa in cyowahinn.items():
    for item in cyowa['map_catagory']:
      if item not in transfer.keys(): transfer[item] = {}
      for source in cyowa['map_source']:
        if source not in transfer[item].keys(): transfer[item][source] = []
        transfer[item][source].append(cyowahinn_name)
    
    for source in cyowa["map_source"]:
      if source not in transfer.keys(): transfer[source] = {}
  
  return cyowahinn, transfer

def dfs(cyowahinn, transfer, target, source, visited, route, depth):
  if target in source:
    print(*reversed(route), sep = '->', end='\n\n')
    return
  if depth == max_step: return

  for cur_source, cyowahinn_names in transfer[target].items():
    if not visited[cur_source]:
      visited[cur_source] = True
      route.append(cyowahinn_names)
      dfs(cyowahinn, transfer, cur_source, source, visited, route, depth+1)
      route.pop()
      visited[cur_source] = False

cyowahinn, transfer = buildMap()
visited = {}
for key in transfer.keys():
  visited[key] = False
dfs(cyowahinn, transfer, target, source, visited, [], 0)