import json
import os
import zipfile
import datetime

def packer():
    if os.path.exists('./emojis') is False:
        os.mkdir('./emojis')
        input("Please put all the emojis in the 'emojis' folder and press Enter to continue")
    if os.path.exists('./output') is False:
        os.mkdir('./output')
    host = input("Enter the metadata host (your instance name): ")
    category = input("Enter the category name (the emoji collection name): ")
    images = os.listdir('./emojis')
    jsondata = {
        "metaVersion": 2,
        "host": host,
        "exportedAt": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds") + "Z",
        "emojis": []
    }
    for filename in images:
        emojiname = filename.split('.')
        emoji = {
            "downloaded": True,
            "fileName": filename,
            "emoji": {
                "name": emojiname[0],
                "category": category,
                "aliases": [],
            }
        }
        jsondata["emojis"].append(emoji)
    with open('./output/meta.json', 'w') as jsonfile:
        json.dump(jsondata, jsonfile, indent=4)
    with zipfile.ZipFile('./output/' + category + '.zip', 'w') as zipf:
        for image in images:
            zipf.write(os.path.join('./emojis', image), image)
        zipf.write('./output/meta.json', 'meta.json')
    keepmeta = input("Do you want to keep the meta.json file? (Y/n): ")
    if keepmeta.lower() != 'y' and keepmeta.lower() != 'yes' and keepmeta.lower() != 'true' and keepmeta.lower() != '1' and keepmeta.lower() != '':
        os.remove('./output/meta.json')
    else:
        os.rename('./output/meta.json', './output/' + category + '_meta.json')
    print("Packing for collection " + category + " completed")
    exit(0)

if __name__ == "__main__":
    packer()