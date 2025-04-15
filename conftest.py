import pytest
import yaml
import yaml_package
import requests


@pytest.fixture (scope="function",autouse= "True")
def pro_post_output():
    print("测试用例执行")
    yield
    print("end of the test process")

@pytest.fixture(scope="session",autouse= "True")
def get_token():
    print("获取token")
    yaml_data = yaml_package.load_yaml("login.yaml")
    url = yaml_data["url"]
    json_data = yaml_data["data"]
    headers = yaml_data["header"]

    result = requests.post(url, json=json_data, headers=headers)
    response = result.json()
    print(response)
    token = response["token"]  # 提取 token
    print("token:", token)
    Authorization = f"Authorization: Bearer  {token}"
    yaml_package.append_yaml("add.yaml",Authorization,"header")
    yaml_package.append_yaml("revise.yaml",Authorization,"header")
    yield token
    print("测试用例结束")
