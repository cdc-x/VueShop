import logging
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import datetime
from utils.common import make_hash

logger = logging.getLogger("log")


class UserLoginView(APIView):
    authentication_classes = []

    @staticmethod
    def post(request):

        # 返回响应数据
        ret_data = {"data": {}, "meta": {"status": 400, "msg": "登录失败"}}

        try:
            data = request.data
            username = data.get("username", "")
            password = data.get("password", "")

            obj = UserManage.objects.filter(username=username, password=password).first()
            if obj:
                # 更新数据
                obj.token = make_hash(key=str(time.time()))
                obj.login_time = datetime.datetime.now().replace(microsecond=0)
                obj.save()

                # 构造数据返回
                user_obj = UserManage.objects.filter(username=username, password=password).first()
                serializer = UserManageSerializer(user_obj)
                data = serializer.data
                data.pop("password")
                ret_data["data"] = data
                ret_data["meta"]["status"] = 200
                ret_data["meta"]["msg"] = "登录成功"
        except Exception as e:
            logger.error(str(e))
            ret_data["meta"]["msg"] = str(e)

        return Response(ret_data)


class GetMenusView(APIView):

    @staticmethod
    def get(request):
        try:
            menus_list = [
                {
                    "id": 125,
                    "authName": "用户管理",
                    "path": "users",
                    "order": 1,
                    "children": [
                        {
                            "id": 110,
                            "authName": "用户列表",
                            "path": "users",
                            "children": [],
                            "order": None
                        }
                    ],
                },
                {
                    "id": 103,
                    "authName": "权限管理",
                    "path": "rights",
                    "children": [
                        {
                            "id": 111,
                            "authName": "角色列表",
                            "path": "roles",
                            "children": [],
                            "order": None
                        },
                        {
                            "id": 112,
                            "authName": "权限列表",
                            "path": "rights",
                            "children": [],
                            "order": None
                        }
                    ],
                    "order": 2
                },
                {
                    "id": 101,
                    "authName": "商品管理",
                    "path": "goods",
                    "children": [
                        {
                            "id": 104,
                            "authName": "商品列表",
                            "path": "goods",
                            "children": [],
                            "order": 1
                        },
                        {
                            "id": 115,
                            "authName": "分类参数",
                            "path": "params",
                            "children": [],
                            "order": 2
                        },
                        {
                            "id": 121,
                            "authName": "商品分类",
                            "path": "categories",
                            "children": [],
                            "order": 3
                        }
                    ],
                    "order": 3
                },
                {"id": 102,
                 "authName": "订单管理",
                 "path": "orders",
                 "children": [
                     {
                         "id": 107,
                         "authName": "订单列表",
                         "path": "orders",
                         "children": [],
                         "order": None
                     }
                 ],
                 "order": 4
                 },
                {
                    "id": 145,
                    "authName": "数据统计",
                    "path": "reports",
                    "children": [
                        {
                            "id": 146,
                            "authName": "数据报表",
                            "path": "reports",
                            "children": [],
                            "order": None
                        }
                    ],
                    "order": 5
                }
            ]

            ret_data = {
                "data": menus_list,
                "meta": {"status": 200, "msg": "获取菜列表成功"}
            }
        except Exception as e:
            logger.error(str(e))
            ret_data = {
                "data": [],
                "meta": {"status": 400, "msg": "获取菜列表失败"}
            }

        return Response(ret_data)
