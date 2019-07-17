# _*_ coding: utf8 _*_
import sys
import os
import yaml
import re


def check_yml():
    """检查yml文件是格式是否符合yml规范"""

    # 配置yml文件所在路径
    target_file = '/jenkins/hudson/jenkins/slave/workspace/deploy_yml_scripts/vars.yml'

    # 打开yml文件对象
    target_file_object = open(target_file, 'r')

    # 尝试用yml 模块加载解析yml文件对象
    try:
        yaml_file_object = yaml.load(target_file_object)

    #异常退出提示，不再进行进一步实例化
    except Exception:
        print('Please chech "%s" ,Format error, Not yml format!!' % target_file)
        sys.exit()

    # 打开正常则返回字典对象
    else:
        return yaml_file_object

    # 无论打开文件是否异常，都会关闭文件流
    finally:
        target_file_object.close()


class Check_path():
    """该类用来具体处理多层字典"""
    #
    def __init__(self, yaml_obj):
        # 用来保存键为字典值的列表，并初始化为空列表，
        self.__list = []

        # 从函数外部获得yml字典对象
        self.__yaml_obj = yaml_obj

    def handle_dict(self, var='', up_key=''):
        # 处理多层字典循环
        # 当首次执行时，函数参数为self.__yaml_obj
        if var == '':
            var = self.__yaml_obj

        # 遍历
        for key, value in var.items():
            # 非首次执行初始化up_key
            if up_key != '':
                con_key = up_key + '.' + key

            # 首次执行up_key == key
            else:
                con_key = key

            # 当value 为字典时，调用函数自己，递归处理
            if type(value) is dict:
                self.handle_dict(value, con_key)
            else:
                # 当匹配到以_src_path结尾，并且排除 #注释的路径
                if re.search(r'^[^#]\w+_src_path\b', key):
                    # print(con_key, '#######', value)
                    dic_obj_char = "{'%s': '%s'}" % (con_key, value)

                    # 只把路径添加进对象__list属性
                    self.__list.append(eval(dic_obj_char))

    def test_path(self):
        # print(self.__list)
        # 定义display 初始化为 True
        display = True
        for p in self.__list:
            for k in p:
                if not os.path.exists(p[k]):
                    print('!!!Not found <<%s : %s>>' % (k, p[k]))
                    # 当找不到路径时，把 display = False
                    display = False
        # 若display为真，说明所有路径都是存在的
        if display:
            print('Congratulation, everything is OK!')


def main():
    yaml_obj = check_yml()
    check_path = Check_path(yaml_obj)
    check_path.handle_dict()
    check_path.test_path()


if __name__ == '__main__':
    main()

