import requests
import json
import re
import random
import execjs


with open('cb.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx=execjs.compile(js_code)


import ddddocr

def get_real_slide_distance(bg_path='bg.jpg', front_path='front.png', slider_width=60):
    det = ddddocr.DdddOcr(det=True, show_ad=False)
    
    with open(bg_path, 'rb') as f:
        bg_bytes = f.read()
    with open(front_path, 'rb') as f:
        front_bytes = f.read()
    
    result = det.slide_match(front_bytes, bg_bytes, simple_target=True)
    x1, y1, x2, y2 = result['target']
    gap_center = (x1 + x2) // 2
    
    # 实际滑动距离 = 缺口中心 - 滑块宽度的一半
    # 因为滑块的中心要对准缺口中心
    real_distance = gap_center - slider_width // 2
    
    return {
        'gap_center': gap_center,      # 缺口中心（从0开始）
        'slide_distance': real_distance, # 实际要滑动的距离
        'x1': x1,  # 缺口左边界
        'x2': x2   # 缺口右边界
    }



# # 使用
# distance = get_slide_distance()
# print(f"缺口距离: {distance}px")

class YiDunSlide():
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://dun.163.com',
            'Pragma': 'no-cache',
            'Referer': 'https://dun.163.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'content-type': 'text/plain',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.dt="FO1sTcv4Ox5BElFARAaTw/+q8eafizxs"
    @property
    def uuid(self):
        template="xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx"
        def replace_func(match):
            char = match.group(0)
            t = int(16 * random.random())  # 0-15随机数
            if char == 'x':
                val = t
            else:  # y
                val = 3 & t | 8  # 位运算确保8-11
            return format(val, 'x')
        
        return re.sub(r'[xy]', replace_func, template)

    @property
    def cb(self):
        return ctx.call('getcb')
    
    @property
    def fp(self):
        return ctx.call('getfp')

    def getconf(self):
        url = "https://c.dun.163.com/api/v2/getconf"
        params = {
            "referer": "https://dun.163.com/trial/jigsaw",
            "zoneId": "",
            "id": "07e2387ab53a4d6f930b8d9a9be71bdf",
            "ipv6": "false",
            "runEnv": "10",
            "iv": "5",
            "type": "2",
            "loadVersion": "2.5.4",
            "callback": "__JSONP_3qa4w9i_0"
        }
        response = requests.get(url, headers=self.headers, params=params)
        res=response.text[18:-2]
        res=json.loads(res)
        print(res)
        self.dt= res['data']['dt']
    def up(self):
        url = "https://ir-sdk.dun.163.com/v4/j/up"
        data = {
            "p": "YD00192283058223",# appid
            "v": "2.0.13_yanzhengma",# sdkVersion
            "vk": "d44593ca",# versionKey
            "n": self.uuid, # uuid
            "d": "InTNMazmeiQOhWt0q.KX92mK559UBTpiXLpiDurZNubFY4J/vznCD/lE9/IAmQWE/xGB.l82I64/IJtXTKw1f3UsZgI6QDzT4YQblLyStgU/CSEYcrYUEYu.TVCB/bdI5mQlD18.xQdIAgJfZFV/jMBeRPQC3x8fVJpDJCI.fgu+sbKw+bWHDZZfTX6GT6TzTJBr+ZtqlRWgEEIxl2S6JQfgZSkazXNW8pbEnQzdxqvsAJHK4GiRfEglPDar5rxfz5YNTJ90Mh.AufOCjmzdIdm9hq2xTlyiIMylGLxwVfyQuKtxEYswYC+ca5ATD.E/nTPTwPWR0lLWpiv.c2KPdZb1Kp6NMtqj.GLCGxhO.Tsw/khh5lcN2blo526JNm9YyDAs3SAVMDlVEG9YSHNZnb.P9NtvsC1lJknbL+tc9rW/fb/UxtF8ocnC4ax1A14glXmZwoXrHu+l2VsGt1vTFnK3kKcXSR4I2BPDOTcQHZSrLLphTkJFpiPlz+PsLXESDpxldvTSx8qzhRXGKjfIIoeze5tRG50e8f8QAn1IGNrMb0nqhAumnk2hwJV05KlKyrJBLDrtB8tRBl+4AsLpRuR93BjzOHeL.hk/VSHUx3Y5j/4WwwfXuBG3EE1kk6ki0.POja3kcncoyLm4JtEYN.GUs1FSgkNplu4XK34nyhfPq+iRVlO9dADlVOAQPdqdaL3bnSgXKCDPjdE4RJLQb.EHdFqqPUKJG5E4cISeA8f1lnVUXjFkLgBSOHlPpmooKgI48N8.i4oLnr9q+egwkubIPAFNfwJYqj9FOq9YtVMZWFMHVQUtByugnrrZ1FXDE2UaBFxeLL1fqROQ+2AHtQWKK1KnbqBVl6iA3xtt2lYZJh1FON5Q5nvMoBJBjnvgCtgWG.jV2i3Y8oztKHeb8OwFbypZqyaS9WDNf64P+MslV/SFTYEs5z/0uU52dHRYdYxK/UnYIsHnC9idKAcrfy3HzFshDnOfS5y2wxMlpn6FTnpBAr/ut8OCprkewQtxsAE+Rl90xeOmwsmbwGDWH2tWL4iMSHA.0OZiBeuMfsFTn+bQ0wTMhvGHyz6c6VOWfrClIrAtAzUnjobDaCWrLKjAjVAQjOMGpzs+IeXAnauHdLKkmAOZH25VyfMTh1uQSG6zvDt.0DAd1wThAkfFH4HlcwEbQY36RkJVcD/w4GNXE31SoqkiX5/4DlOpvXZVc0FDUpwmOAHZUqhHof5K8idU3Mxv5IIs.uTPGKJahreefxBSmyjm+losOBFoTkjqNRCorxvG59jfaQ9Fok2yNkZy5z3KompaevriE0MfVAMS2nlvQ1vNOm.Y955ZWVfv2pxz+p82LY6w46KNwW89TBuufrmkjZawR1liOtWA.LcFyWvlXP+ThedB9MwXnJJnRz+2wDk4wg+XWCOlSOLq9YlwvbQCym2tx+q6iK.Ezf2vSME5h8sn29d+4DvZIRBTYH.23lQDFozXL80lO5tPfvRhCC5A5jcliyf94MzJIMilyG1AWDZ20Sj0PifXrBR.IbiwhfvMw9zUnvBlU.csyn.MAB5WT11JlQlinoh50tLBs/8ThjcEF4ncvy13mgW3DYLcIr5epamzVA1ehqK3ly1I6K13/qFVqzSyJT8KN+p3j.DHKkeuhmmGsX0nxFBpjacWp5GQjvPf98+KfcQ/nGlCZ9E.Wm2uny4cwF2TtlRF0Wntcp3Y6eR4g6TQNMEgIhpKhxpPGAAqr/mCHBpejqJrOnTl.tlYNuo98FZpHjXAkLPP/xSaspxtxCLV6jW.Q.HbyTHbGEUd1dTyIRrVgze4GgNIiM9hDhGe4bTHIjKl.LUnbZ3SUrThI9QlS4ebaeldSvZi6+ZKW.LNAzx9bQXgs3SJKsWmLJUhr3dnQsSx/IvXbbcpGDeQnh/EjKkQHCxzQIRYKVKambJZ866+kg08tCeRPz5OOsaGFB8WkafSi0TYILVIHxe.qunc+KeDByJnnxQN553TPRwkMxPoJuP0B8PohygQvcIzGBwI2lJcxgsunJvtF+4tPCjt/tfkcDYF1/4iyvJrwSIEFmLy6wKpe0gG8NnPWf2ugGhdHRsjiCCsz/nXi.sWBj0nnPgcw3SZWnIF4ztmFm0VfF+m69.svrmF+KqwNZs69Qttd4iP/U.wo.38zhg3EH1vfDmPiveDrVbSZkniGSG8NkFxwJpxlwRt.OqHT5UvRGGQBftMV/85lKeSWi.9VWOpU6QMeTUq1QGR11c8ReqWYhEA98i4ux9cHHqfQ6R4lUtIuOcWdEN8wjDr16MHbt9irzNAx5O9+.1wR.GGLd+ttw3HHqVPlGI+NWoDuwouGZTuY6yPRQn.TM8WvrPVTtPed2g/+YOln1byUxtaj1BLPANcPJ1npzt5VFBpdU5BB/2zEa3Zv0GkrGscWlrG1BkBm9tycl8JIFZq+5RHM5haACo+5wkKbMD8evs1rIsZ+AJzm5+tWriXXwSdlUIJEo0x+au/9lBYSf/p/9HZ/6a9b3OZNgvp.PqxUZ856m/FwVaDejsAs2+d06bPPlzPEnfam5u.GQHLmY77"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=self.headers, data=data)
        print(response.text)
        irToken = response.json()['data']['tk']
        
        return irToken
    
    def get(self,irToken):
        url = "https://c.dun.163.com/api/v3/get"
        params = {
            "referer": "https://dun.163.com/trial/jigsaw",
            "zoneId": "CN31",
            "dt": self.dt,# getconf接口返回
            "irToken": irToken, # tk
            "id": "07e2387ab53a4d6f930b8d9a9be71bdf",# captchaId
            "fp": self.fp,
            "https": "true",
            "type": "2",
            "version": "2.28.5",
            "dpr": "1.5",
            "dev": "1",
            "cb": self.cb,
            "ipv6": "false",
            "runEnv": "10",
            "group": "",
            "scene": "",
            "lang": "zh-CN",
            "sdkVersion": "",
            "loadVersion": "2.5.4",
            "iv": "4",
            "user": "",
            "width": "320",
            "audio": "false",
            "sizeType": "10",
            "smsVersion": "v3",
            "token": "",# 初始没有
            "callback": "__JSONP_ucjswdi_1"
        }
        response = requests.get(url, headers=self.headers, params=params)
        res=json.loads(response.text[18:-2])
        with open('bg.jpg', 'wb') as f:
            f.write(requests.get(res['data']['bg'][0]).content)
        with open('front.png', 'wb') as f:
            f.write(requests.get(res['data']['front'][0]).content)
        
        token=res['data']['token']

        print(res)
        return token
        # print(response)
    

    def check(self,token,slide_distance):
        url = "https://c.dun.163.com/api/v3/check"
        params = {
            "referer": "https://dun.163.com/trial/jigsaw",
            "zoneId": "CN31",
            "dt": self.dt,
            "id": "07e2387ab53a4d6f930b8d9a9be71bdf",
            "token": token,
            "data":ctx.call('getdata',token,int(slide_distance)) ,
            "width": "320",
            "type": "2",
            "version": "2.28.5",
            "cb": self.cb,
            "user": "",
            "extraData": "",
            "bf": "0",
            "runEnv": "10",
            "sdkVersion": "",
            "loadVersion": "2.5.4",
            "iv": "4",
            "callback": "__JSONP_v92ataq_2"
        }
        response = requests.get(url, headers=self.headers, params=params)

        print(response.text)
        print(response)
        return response.text



if __name__ == "__main__":
    slide=YiDunSlide()
    slide.getconf()
    irToken=slide.up()
    token=slide.get(irToken)
    res = get_real_slide_distance(slider_width=60)
    # print(f"缺口中心: {res['gap_center']}px")
    slide_distance=res['slide_distance']
    print(f"实际滑动: {res['slide_distance']}px")  # 用这个值
    slide.check(token,slide_distance)

# import time

# if __name__ == "__main__":
#     slide = YiDunSlide()
    
#     total_count = 50  # 测试总次数
#     success_count = 0 # 成功计数
    
#     print(f"🚀 开始正确率测试，总计 {total_count} 次...")
#     print("-" * 50)

#     for i in range(1, total_count + 1):
#         try:
#             # 1. 获取 irToken (up 接口)
#             irToken = slide.up()
            
#             # 2. 获取验证码图片和 token (get 接口)
#             token = slide.get(irToken)
            
#             # 3. 识别距离
#             # 注意：ddddocr 识别前建议清理旧图片，或者在 get 逻辑里确保覆盖
#             res = get_real_slide_distance(slider_width=60)
#             slide_distance = res['slide_distance']
            
#             # 4. 提交验证 (check 接口)
#             # 假设你已经按照之前的建议，在 check 内部实现了轨迹生成和加密
#             check_res_text = slide.check(token, slide_distance)
            
#             # 5. 解析结果
#             # 使用正则提取 JSONP 里面的 json 对象
#             import re
#             match = re.search(r'__JSONP_.*?\((.*)\)', check_res_text)
#             if match:
#                 res_json = json.loads(match.group(1))
#                 is_success = res_json['data']['result']
                
#                 if is_success:
#                     success_count += 1
#                     validate_token = res_json['data'].get('validate', '')[:20] + "..."
#                     print(f"[{i:02d}] ✅ 验证成功! 距离: {slide_distance}px, Validate: {validate_token}")
#                 else:
#                     print(f"[{i:02d}] ❌ 验证失败. 距离: {slide_distance}px")
#             else:
#                 print(f"[{i:02d}] ⚠️ 响应格式异常")

#         except Exception as e:
#             print(f"[{i:02d}] 💥 发生错误: {e}")

#         # 随机等待 2-4 秒，模拟真人行为并防止封禁
#         time.sleep(random.uniform(2, 4))

#     # 统计结果
#     accuracy = (success_count / total_count) * 100
#     print("-" * 50)
#     print(f"📊 测试结束!")
#     print(f"✅ 成功次数: {success_count}")
#     print(f"❌ 失败次数: {total_count - success_count}")
#     print(f"🎯 最终正确率: {accuracy:.2f}%")


