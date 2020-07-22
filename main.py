# -*- coding: UTF-8 -*-
import argparse
import requests
import re


def input():
    """
       Enter a product name from the keyboard
       @:param a product name by argparse
       @:return a product name
    """
    parser = argparse.ArgumentParser(description="your script description")
    parser.add_argument('-n', '--trade_name', type=str, help="Please enter a product name！", required=True)
    args = parser.parse_args()
    trade_name = args.trade_name
    return trade_name


def request(trade_name, page, search_url, headers):
    """
       Initiate an HTTP request
       @:param trade_name, page, search_url, headers
       @:return a text about html
    """
    params = {
        "q": trade_name,
        "ie": "utf8",
        "s": (page - 1) * 44
    }
    html = requests.get(url=search_url, params=params, headers=headers)
    html.raise_for_status
    html.encoding = html.apparent_encoding
    return html.text

def getData(data_list, html_text):
    """
       Analyze the text file and summarize the sales volume according to the merchant name
       @:param data_list, html_text
    """
    Store = re.findall(r'\"nick\"\:\".*?\"', html_text)
    Sales = re.findall(r'\"view_sales\"\:\".*?\"', html_text)
    for i in range(len(Sales)):
        sales_count_str = Sales[i].encode("UTF-8").split(':')[1].replace("\"", "")
        sales_count_str = sales_count_str.replace("+", "").replace("人付款", "")
        if "万" in sales_count_str:
            sales_count_str = sales_count_str.replace("万", "")
            sales = float(sales_count_str) * 10000
        else:
            sales = int(sales_count_str)
        store = Store[i].encode("UTF-8").split(':')[1].replace("\"", "")
        if store in data_list:
            data_list[store] += sales
        else:
            data_list[store] = sales


def output(items):
    for store, sales in items:
        print "%s, %s" % (store, sales)


def main():
    """
        main method
        run
    """
    trade_name = input()
    search_url = 'https://s.taobao.com/search'
    headers = {
        "cookie": "t=42917e81b529ef3624449c8d3e029409; "
                  "cna=VT93Fz0cyHECATr6soFGMMty; "
                  "lgc=%5Cu9EA6%5Cu5730%5Cu4E00%5Cu5E86; "
                  "tracknick=%5Cu9EA6%5Cu5730%5Cu4E00%5Cu5E86; "
                  "thw=cn; "
                  "enc=GIhHm0yzREUd21%2FZT76%2B1MnoFJgG3oPJC67znxVMcFOZUH5fT4oaWeO3WDhYREHyseLxZCOTzs0NZjSIiHIRMg%3D%3D; "
                  "hng=CN%7Czh-CN%7CCNY%7C156; "
                  "v=0; "
                  "cookie2=101d9e6dd251d8f784916771e8522d8e; "
                  "_tb_token_=77d97ae7383e5; "
                  "alitrackid=www.taobao.com; "
                  "lastalitrackid=www.taobao.com; "
                  "JSESSIONID=04E0DF54DC87FBF38F54F65A3971C8F9; "
                  "_samesite_flag_=true; "
                  "sgcookie=EmtAqt8JVg5wUYMXICJOs; "
                  "uc3=id2=UoexMyViCzR6CA%3D%3D&vt3=F8dBxGJvSrJ5l0NpKRg%3D&nk2=oc0jGbSozBk%3D&lg2=URm48syIIVrSKA%3D%3D; "
                  "csg=9f30508b; dnk=%5Cu9EA6%5Cu5730%5Cu4E00%5Cu5E86; "
                  "skt=35d223150e9a27d7; "
                  "existShop=MTU5Mzc1NzEyOQ%3D%3D; "
                  "uc4=nk4=0%40o4VmAxp90Mh9Gk5Y8Dv7mXd9UA%3D%3D&id4=0%40UO%2B3%2BrAg2ee%2B%2FaFL8qCiCWqAHlf%2F; "
                  "_cc_=W5iHLLyFfA%3D%3D; "
                  "tfstk=cI8ABujyfbFAuKCJTnnlCtx6TpSAaMFAFS6aWfxknL27kJ4T5sV9-eHU7m1THahR.; "
                  "mt=ci=92_1; "
                  "uc1=pas=0&cookie14=UoTV6OOIRgVrIQ%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&existShop=false&cart_m=0&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D; "
                  "l=eBEKHk7IQt_rgma6KO5Churza77TVIObzsPzaNbMiInca6ihK_z4SNQqNapWjdtjgtfXdFxzdtnJ9RhDW8ULStiVBdeKgnspBxv9-; "
                  "isg=BDY2QYLrdYRNUgAViNPRUqt2h2o4V3qR7Fa9XqAeepmh49R9D-U2oS5V_7-Py3Kp"
    }

    data = {}
    for page in range(1, 11):
        html_text = request(trade_name, page, search_url, headers)
        # print html_text
        getData(data, html_text)
    # sort desc get top 10 sales
    result = sorted(data.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result_sorted_10 = list(result)[:10]
    output(result_sorted_10)


main()