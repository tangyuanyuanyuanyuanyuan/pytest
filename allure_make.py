import pytest
import subprocess
import sys
import os
# 添加 Allure 所在目录到 PATH
os.environ["PATH"] += os.pathsep + r"C:\Users\86188\scoop\apps\allure\current\bin"
def run_pytest_and_generate_report():
    retcode=pytest.main([".","--alluredir=allure-results"])#执行test_*.py
    print(retcode)
    if retcode!=0:
        print(f"pytest运行失败，退出码：{retcode}")
        sys.exit(retcode)
# 2. 生成allure报告（确保allure命令可用）
    generate_cmd = ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"]
    #allure generate allure-results -o allure-report --clean

    open_cmd = ["allure", "serve", "allure-results"]

    print("正在生成Allure报告...")
    subprocess.run(generate_cmd, check=True)# 同步执行，失败抛异常
    print("报告生成成功，正在打开报告...")

    subprocess.Popen(open_cmd, check=True)
if __name__ == '__main__':
    run_pytest_and_generate_report()

