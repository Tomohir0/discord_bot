# test2.py
import json
import boto3
 
bucket_name = "tomo-discord"
json_key = "test.json"
s3 = boto3.resource('s3')
obj = s3.Object(bucket_name,json_key)

a = "cont"
test_json = {'1': a}
r = obj.put(Body = json.dumps(test_json))
 
# get json data
print(obj.get()['Body'].read())

'''
f_name2 = "/tmp/storage_" + ctx.message.author.server.id + ".pkl"  # いろいろstorageに入れる
       if not os.path.isfile(f_name2):  # 存在しないときの処理
            storage = {}
        else:
            with open(f_name, 'rb') as f:
                storage = pickle.load(f)
'''