import os
import pydot
import shutil
import argparse
from subprocess import check_call

parser = argparse.ArgumentParser()
# input
parser.add_argument("--input_folder", default='input')
parser.add_argument("--legend_full", default='legend_full.txt')
parser.add_argument("--legend_brief", default='legend_brief.txt')
parser.add_argument("--endnote", default='endnote.txt')
parser.add_argument("--graph_origin", default='graph.dot')
# output
parser.add_argument("--output_folder", default='output')
parser.add_argument("--graph_update", default='graph_update.dot')
parser.add_argument("--svg_origin", default='svg_origin.svg')
parser.add_argument("--svg_update", default='svg_update.svg')
# param
parser.add_argument("--node_circle_scale", type=int, default=3)
args = parser.parse_args()

# 参数设置
input_folder = args.input_folder
legend_full_txt = os.path.join(input_folder, args.legend_full)
legend_brief_txt = os.path.join(input_folder, args.legend_brief)
endnote_txt = os.path.join(input_folder, args.endnote)
graph_origin_file = os.path.join(input_folder, args.graph_origin)

output_folder = args.output_folder
graph_update_file = os.path.join(output_folder, args.graph_update)
svg_origin_file = os.path.join(output_folder, args.svg_origin)
svg_update_file = os.path.join(output_folder, args.svg_update)
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

'''Step1. 读取HistCite导出的完整文献信息，获得标题和索引'''
with open(legend_full_txt) as f:
    info = f.readlines()
info = [ele.strip() for ele in info]
titles = info[1::5]
ids = info[0::5]
ids = [int(ele.split(' ')[1]) for ele in ids]
print(titles[:5])


'''Step2. 读取HistCite导出的简略文献信息，获得文章缩写'''
with open(legend_brief_txt) as f:
    brief_infos = f.readlines()
brief_infos = [' '.join(ele.strip().split(' ')[3:]) for ele in brief_infos]
print(brief_infos[:5])

'''Step3. 读取Endnote标注后导出的信息，获得关键词'''
with open(endnote_txt, encoding='UTF-8') as f:
    info_endnote = f.readlines()
    
# Each element in this list contains: Title;Year;Author;Keywords;Abstract
info_endnote = [ele.strip().split('\t') for ele in info_endnote] 
print(info_endnote[0])

'''Step4. 修改Dot文件中的label值'''
with open(graph_origin_file, encoding='UTF-8') as f:
    dot_info = f.readlines()
print(dot_info)

node_circle_scale = args.node_circle_scale
for idx, line in enumerate(dot_info):
    # if idx ==2:
    #     dot_info[idx] = line.replace("]", ", fontname=SimHei]")
    if idx == 3:
        edge_property = line.split('[')[1]
        dot_info[idx] = line.replace(edge_property, 'dir=back, style=dashed];')
    if 'label=' in line:
        if line.find('URL=') > 0:
            print('Original info:', line)
            # change node size
            original_h =line.split('"')[3]
            original_w = line.split('"')[11]
            new_h, new_w =  float(original_h) * node_circle_scale, float(original_w) * node_circle_scale 
            line = line.replace(str(original_h), str(new_h))
            line = line.replace(str(original_w), str(new_w))
            # add key
            histcite_id = int(line.split('"')[1]) + 1
            txt_idx = ids.index(histcite_id)
            title = titles[txt_idx] # title
            for ele in info_endnote:
                if title in ele: # find endnote information
                    keyword = ele[3]
                    # write information
                    with open('%s/%d' % (output_folder, histcite_id-1), 'w') as f:
                        f.write('\n'.join(ele))
            author = ''.join(brief_infos[txt_idx].split(',')[:2])
            new_info = ','.join([str(histcite_id), author])
            new_info = '\n'.join([new_info, keyword])
            new_line = line.replace(str(histcite_id), new_info)
            print('Update info:', new_line)
            # udpate infomation
            dot_info[idx] = new_line

# 保存更新后的文件
with open(graph_update_file, 'w', encoding='UTF-8') as f:
    f.writelines(dot_info)

'''Step5. Generate Dot File and SVG File'''
check_call(['dot', '-Tsvg', graph_update_file, '-o', svg_update_file])
check_call(['dot', '-Tsvg', graph_origin_file, '-o', svg_origin_file])

# (graph, ) = pydot.graph_from_dot_file(graph_origin_file, encoding='UTF-8')
# graph.write_svg(svg_origin_file)
# (graph, ) = pydot.graph_from_dot_file(graph_update_file, encoding='UTF-8')
# graph.write_svg(svg_update_file)
 