import json
import csv

# input: json file of specific image, imageID
# output: list of {box_id, box_text, label}
def flattenCordDataset(id):
    print("JSON file of", id)
    output_dict = []
    with open('./json/receipt_'+str(id).zfill(5)+'.json') as f:
        data = json.load(f)
        cnt = 0
        for group in data["valid_line"]:
            for word in group["words"]:
                #print(word["text"], group["category"], cnt)
                output_dict.append({"box_id": cnt, "box_text": word["text"], "label": group["category"]})
                cnt+=1
    return output_dict
        

# input: csv file of the database, imageID
# output: list of {box_id, label}
def flattenMTurkDataset(id):
    print("CSV file of", id)
    init_dict = []
    output_dict = []
    # specify path of the csv file here
    with open('samplecsv.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',', fieldnames=('id', 'imageID', 'groupID', 'boxIDs', 'label', 'user_id'))
        for row in reader:
            if (row["imageID"] == str(id)):
                row["boxIDs"] = row["boxIDs"][1:-1].split(",")
                init_dict.append(row)
    
    for group in init_dict:
        for box in group["boxIDs"]:
            output_dict.append({"box_id": int(box), "label": group["label"]})
    return output_dict


# Convert MTurk labels into original data in CORD
def convertLabel(label):
    if (label == "menu - name"): return "menu.nm"
    if (label == "menu - unit price"): return "menu.unitprice"
    if (label == "menu - count"): return "menu.cnt"
    if (label == "menu - price"): return "menu.price"
    if (label == "subtotal - subtotal price"): return "subtotal.subtotal_price"
    if (label == "subtotal - tax price"): return "subtotal.tax_price"
    if (label == "total - total price"): return "total.total_price"
    if (label == "payment - cash price"): return "total.cashprice"
    if (label == "payment - credit card price"): return "total.creditcardprice"
    if (label == "payment - change price"): return "total.changeprice"
    if (label == "N/A - N/A (Not Applicable)"): return "N/A"
    else:
        return label

# Convert 'sub_total' to 'subtotal' in original label 
def convertSubtotal(label):
    if (label[:9] == "sub_total"):
        return 'subtotal' + label[9:]
    return label

# Input: Polished CORD & MTurk data, imageID
# Output: list of {image_id, box_id, label1, label2, label3, label4, major label, original label}
def majorityVoting(id):
    original_dataset = flattenCordDataset(id)
    mturk_output = flattenMTurkDataset(id)
    print(mturk_output)

    final_output = []

    num_cord_boxes = len(list(set(list(map(lambda x: x['box_id'], original_dataset)))))
    num_mturk_boxes = len(list(set(list(map(lambda x: x['box_id'], mturk_output)))))
    if (not num_cord_boxes == num_mturk_boxes):
        return "Number of boxes is different. May be there is an error in the MTurk data?"

    for box_id in range(len(original_dataset)):
        filter_cord = list(filter(lambda x: x['box_id'] == box_id, original_dataset))
        filter_mturk = list(filter(lambda x: x['box_id'] == box_id, mturk_output))

        #print(filter_cord)
        #print(filter_mturk)
        voting = dict()
        for box in filter_mturk:
            voting[box["label"]] = voting.get(box["label"], 0) + 1

        # When we have four labels
        if (len(filter_mturk) == 4):
            # If max vote is >= 3
            if (voting[max(voting.keys(), key=voting.get)] >= 3):
                major_label = max(voting.keys(), key=voting.get)
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": convertLabel(filter_mturk[3]["label"]),
                    "major_label": convertLabel(major_label),
                    "original_label": filter_cord[0]["label"],
                })
            # If number of labels is 2 & max vote is 2
            elif (len(voting.keys()) == 2 and voting[max(voting.keys(), key=voting.get)] == 2):
                major_label = max(voting.keys(), key=voting.get)
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": convertLabel(filter_mturk[3]["label"]),
                    "major_label": "tie",
                    "original_label": filter_cord[0]["label"],
                })
            # If number of labels is 3 & max vote is 2
            elif (len(voting.keys()) >= 3 and voting[max(voting.keys(), key=voting.get)] == 2):
                major_label = max(voting.keys(), key=voting.get)
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": convertLabel(filter_mturk[3]["label"]),
                    "major_label": convertLabel(major_label),
                    "original_label": convertSubtotal(filter_cord[0]["label"]),
                })
            # If there is no majority label
            else:
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": convertLabel(filter_mturk[3]["label"]),
                    "major_label": 'all_diff',
                    "original_label": convertSubtotal(filter_cord[0]["label"]),
                })   
        
        # When we have three labels
        elif (len(filter_mturk) == 3):
            # If max vote is >= 2
            if (voting[max(voting.keys(), key=voting.get)] >= 2):
                major_label = max(voting.keys(), key=voting.get)
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": None,
                    "major_label": convertLabel(major_label),
                    "original_label": convertSubtotal(filter_cord[0]["label"]),
                })
            # If there is no majority label
            else:
                final_output.append({
                    "image_id": id, 
                    "box_id": box_id, 
                    "label1": convertLabel(filter_mturk[0]["label"]),
                    "label2": convertLabel(filter_mturk[1]["label"]),
                    "label3": convertLabel(filter_mturk[2]["label"]),
                    "label4": None,
                    "major_label": 'all_diff',
                    "original_label": convertSubtotal(filter_cord[0]["label"]),
                })
    return final_output

        


# Argument = image id
final_output = majorityVoting(0)
print(final_output)

with open('result.csv', 'w') as csv_file:  
    writer = csv.DictWriter(csv_file, fieldnames=final_output[0].keys())
    writer.writeheader()
    for i in range(100):
        writer.writerows(majorityVoting(i))
    # for row in final_output:
    #     for key, value in final_output.items():
    #     writer.writerow([key, value])