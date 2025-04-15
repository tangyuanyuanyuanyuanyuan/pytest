import pytest
import yaml_package
import requests
import random
import string
#静言可以不用self
class TestAPI:
    @pytest.mark.skip(reason="无效用例")
    def test_token(self):
        x = 200
        assert x == 200

    # 生成随机测试数据
    def generate_users(n):
        return [
            {
                "userName": ''.join(random.choices(string.ascii_letters + string.digits, k=6)),
                "nickName": ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            }
            for _ in range(n)
        ]

    @pytest.mark.parametrize("user", generate_users(5))  # 生成 5 个用例
    def test_add(self,user):
        yaml_data=yaml_package.load_yaml("add.yaml")
        url = yaml_data["url"]
        datas = yaml_data["data"]
        datas["userName"] = user["userName"]
        datas["nickName"] = user["nickName"]
        print(datas)

        head = yaml_data["header"]
        print(head)
        result =requests.post(url,json=datas,headers=head )
        resp=result.json()
        print(resp)

        assert  resp["code"] == 200

    @pytest.mark.parametrize("user", generate_users(10))  # 生成 5 个用例
    def test_refix(self,user):#进行修改

        yaml_data = yaml_package.load_yaml("add.yaml")

        num = random.randint(189, 250)
        user = f"http://62.234.166.117/prod-api/system/user/{num}"
        result = requests.get(url=user,headers=yaml_data["header"])
        resp =result.json()

        datas=resp["data"]

        nick_name="".join(random.choices(string.ascii_letters + string.digits, k=6))
        datas["nickName"]=nick_name
        yaml_data1=yaml_package.load_yaml("revise.yaml")
        head = yaml_data1["header"]
        url=yaml_data["url"]

        print(datas)
        result =requests.put(url,json=datas,headers=head )
        resp=result.json()
        print(resp)
        assert resp["code"] == 200

    def test_del(self):

        num = random.randint(189, 250)
        yaml_data = yaml_package.load_yaml("add.yaml")
        user = f"http://62.234.166.117/prod-api/system/user/{num}"
        result=requests.delete(user,headers=yaml_data["header"])
        resp=result.json()
        print(resp)
        assert resp["code"] == 200















