import requests
import json
from datetime import datetime, timedelta
import os  # 添加这行导入

def fetch_and_analyze_data():
    base_url = "https://thegreenscentennial.com/CmsSiteManager/callback.aspx?act=Proxy/GetUnits&available=true&honordisplayorder=true&bestprice=true&leaseterm=12"
    start_date = datetime.strptime("2025-05-11", "%Y-%m-%d")
    end_date = datetime.strptime("2025-07-11", "%Y-%m-%d")
    
    # floorplanPartnerId映射
    floorplan_map = {
        "1": "studio",
        "2": "A0",
        "3": "A1",
        "4": "A2",
        "5": "B1",
        "6": "B2",
        "7": "B3"
    }
    
    unique_units = {}  # 使用字典来存储唯一unit，以unit id为key
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"{base_url}&dateneeded={date_str}"
        
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                for unit in data.get("units", []):
                    unit_id = unit.get("id")
                    floorplan_id = str(unit.get("floorplanPartnerId"))
                    rent = unit.get("rent")
                    
                    # 添加筛选条件
                    if floorplan_id in ["2", "3", "4"]:
                        if unit_id not in unique_units:
                            unique_units[unit_id] = {
                                "name": unit.get("name"),
                                "buildingName": unit.get("buildingName"),
                                "floorplan": floorplan_map.get(floorplan_id, "Unknown"),
                                "internalAvailableDate": unit.get("internalAvailableDate"),
                                "vacantDate": unit.get("vacantDate"),
                                "rent": rent
                            }
            except json.JSONDecodeError:
                print(f"Invalid JSON response from {url}")
                print(f"Response content: {response.text}")
                continue
        
        current_date += timedelta(weeks=2)
    
    # 将字典值转换为列表并打印
    unique_units_list = list(unique_units.values())
    print(json.dumps(unique_units_list, indent=2))
    
    # 添加邮件发送功能
    send_email(unique_units_list)

def analyze_data(data):
    # 提取并打印关心的字段
    for unit in data.get("units", []):
        unit_info = {
            "name": unit.get("name"),
            "buildingName": unit.get("buildingName"),
            "floorplanPartnerId": unit.get("floorplanPartnerId"),
            "internalAvailableDate": unit.get("internalAvailableDate"),
            "vacantDate": unit.get("vacantDate"),
            "rent": unit.get("rent")
        }
        print(json.dumps(unit_info, indent=2))

def send_email(data):
    # 如果data为空，则不发送邮件
    if not data:
        print("没有数据，邮件未发送")
        return
    
    # 从环境变量获取配置
    api_key = os.environ.get('SENDGRIDAPIKEY')
    receiver_email = os.environ.get('MYEMAIL')
    
    if not api_key or not receiver_email:
        print("缺少必要的环境变量配置")
        return
    
    # SendGrid配置
    url = "https://api.sendgrid.com/v3/mail/send"
    
    # 邮件内容
    email_data = {
        "personalizations": [
            {
                "to": [{"email": receiver_email}],
                "subject": "Greens Crawl Results"
            }
        ],
        "from": {"email": receiver_email},
        "content": [
            {
                "type": "text/plain",
                "value": f"最新房价信息：\n{json.dumps(data, indent=2)}"
            }
        ]
    }
    
    # 发送请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=email_data, headers=headers)
        if response.status_code == 202:
            print("邮件发送成功！")
        else:
            print(f"邮件发送失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    fetch_and_analyze_data()