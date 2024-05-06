import json
import re


def due(configpath):
    data = json.load(open(configpath))
    #分割符
    separator = data['separator']
    #注释符
    commentor = data['commentor']
    with open(data['filepath']) as file:
        line_list = file.readlines()
        for key in data['scitems'].keys():
            pattern = f"^{key}\s*{separator}|{commentor}\s*{key}\s*{separator}"
            for line in line_list:
                if re.match(pattern, line):
                    index = line_list.index(line)
                    if len(separator) > 0:
                        value = line.split(separator)[1].strip()
                    else:
                        value = line.split()[1].strip()
                    if value != data['scitems'][key]:
                        print(f"{index}行 {key} {value} 不安全，建议修改为{data['scitems'][key]}")
                        user_input = input("是否按照配置文件修复：y/n")
                        if user_input == "y":
                            for key in data['scitems'].keys():
                                pattern = f"^{key}\s*{separator}|{commentor}\s*{key}\s*{separator}"
                                for line in line_list:
                                    if re.match(pattern, line):
                                        if len(separator) > 0:
                                            value = line.split(separator)[1].strip()
                                        else:
                                            value = line.split()[1].strip()
                                        if value != data['scitems'][key]:
                                            index = line_list.index(line)
                                            line_list[index] = f"{key}{separator}{data['scitems'][key]}\n"
                                            content = ''.join(line_list)
                                            with open(data['filepath'], 'w') as f:
                                                f.writelines(line_list)
                                            print(f"{index}行{key}{value}已修改为{data['scitems'][key]}")
                        elif user_input != "y":
                            print("用户跳过，流程结束")
                    else:
                        print(f"{index}行 {key} {value} 对比检查通过")


due('./php.json')
