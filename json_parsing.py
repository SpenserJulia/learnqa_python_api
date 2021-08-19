import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

obj = json.loads(json_text)
# короткий вариант, но без обработки исключений
# print(obj['messages'][1]['message'])

key = "messages"
key_last = 'message'

if key in obj:
    var = obj[key][1]
    #print(var)
    if key_last in var:
        print(var[key_last])
    else:
        print(f"Ключа {key_last} в JSON не оказалось")
else:
    print(f"Ключа {key} в JSON не оказалось ")