import json

def convert(json_file):
    with open(json_file, encoding='utf8') as f:
        json_data = json.load(f)
    
    label2id = json_data['label2id']
    label2id_convert = {}
    for k in label2id.keys():
        label2id_convert[f'{label2id[k]}'] = k

    json_data['id2label'] = label2id_convert
    
    json_object = json.dumps(json_data, indent=4, ensure_ascii=False)
        
    # Writing
    with open(json_file, "w", encoding='utf8') as outfile:
        outfile.write(json_object)

file = "weights/ndcv_200/config.json"
print(convert(file))