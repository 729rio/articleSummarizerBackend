import http.client

conn = http.client.HTTPSConnection("api.apyhub.com")

# 이 토큰은 내 계정으로 연결돼있는데 너랑 같이 써도 작동될진 모르겠음
headers = { 'apy-token': "APY0eTrkxF7MVDENMjL1RTdCykektXhj697DjD5OCQM8ObOrpie9VuYrpZyYrE3wCslHZoHEs8"}

# to test, insert desired url after 'url=' 
conn.request("GET", "/extract/text/webpage?url=https://www.cnn.com/politics/live-news/hunter-biden-trial-06-03-24/index.html", headers=headers)

res = conn.getresponse()
data = res.read()

# prints all text from the website
print(data.decode("utf-8"))
