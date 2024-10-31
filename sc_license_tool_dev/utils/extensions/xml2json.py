import xml.etree.ElementTree as ET
import json


def convert_cvat_xml_to_labelme_json(xml_file_path, json_file_path):
    # 解析 XML 文件
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # 准备 LabelMe 格式的 JSON 数据结构
    labelme_data = {
        "shapes": [],
        "imagePath": "",
        "imageData": None,
        "imageHeight": 0,
        "imageWidth": 0
    }

    # 假设 CVAT XML 有一个 'image' 标签，包含所有的标注信息
    for image in root.findall('image'):
        labelme_data["imagePath"] = image.get('name')
        labelme_data["imageHeight"] = int(image.get('height'))
        labelme_data["imageWidth"] = int(image.get('width'))

        # 遍历所有的 'box' 标签来获取标注
        for box in image.findall('box'):
            label = box.get('label')
            # 假设 box 标签有 'xtl', 'ytl', 'xbr', 'ybr' 属性来表示边界框
            points = [
                [float(box.get('xtl')), float(box.get('ytl'))],
                [float(box.get('xbr')), float(box.get('ybr'))]
            ]

            shape = {
                "label": label,
                "points": points,
                "shape_type": "rectangle",  # 或根据需要修改为其他形状
            }
            labelme_data["shapes"].append(shape)

    # 写入 JSON 文件
    with open(json_file_path, 'w') as json_file:
        json.dump(labelme_data, json_file, indent=2)


# 使用函数
convert_cvat_xml_to_labelme_json(r'C:\Users\yifeiwang\Desktop\14514d0b8ba92b48d704ec3e3909561.xml', r'C:\Users'
                                                                                                    r'\yifeiwang\Desktop\14514d0b8ba92b48d704ec3e3909561.json')
