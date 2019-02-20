#Importing modules from packages
import csv
import re
from collections import defaultdict

#Defining removal function to strip excess characters away from names
def removal(name):
    return name.replace('BIS', '').strip().strip("'")

#Removing "FW", "RE" & "Fwd" prefixes from email subjects using regex metacharacters:
r = re.compile('([\[\(] *)?.*(RE?S?|FW?|Fwd?|re\[\d+\]?) *([-:;)\]][ :;\])-]*)|\]+ *$', re.IGNORECASE)

#Creating columns for the output:
columns = ["From", "To", "CC", "BCC"]

# Creating a dictionary for the subjects list: 
conv = {element: defaultdict(list) for element in columns} #Specifying "From","To","CC","BCC" as the dictionary keys
importance_conv = defaultdict(list) #Initializing lists for the key values 
with open('220.csv', "r+") as f: #Creating text object from input file and naming it 'f'
    f_reader = csv.DictReader(f) #Creating dictionary from 'f' with columns headers as keys and rows as values
        subject = r.sub("", row['Subject'])
        importance = row['Importance']
        
        
        for element in columns: 
            for name in row[element+': (Name)'].split(';'):  
                name = removal(name) 
                if name:    
                    conv[element][name].append(subject)
                    importance_conv[name].append(importance)

#Getting rid of duplicate entries
all_names = list(importance_conv.keys())
for name in all_names:
    for val in all_names:
        if name != val and name in val:
            importance_conv[val].extend(importance_conv[name])
            del importance_conv[name]
            for element in columns:
                conv[element][val].extend(conv[element][name])
                del conv[element][name]


#Defining fields for csv output
fields = ['Name', 'Total','Conversations', 'From', 'To', 'CC', 'BCC', 'Importance'] #column headers for output
data = []

#Counting each each unique name
for name in sorted(importance_conv.keys()):
    importance = 'High' if 'High' in importance_conv[name] else 'Normal'
    conversations = len(set(subject for element in columns for subject in conv[element][name]))
    total = sum(len(conv[element][name]) for element in columns)
    load = {'Name': name,'Total':total, 'Conversations': conversations, 'Importance': importance}
    for element in columns:
        load[element] = len(conv[element][name])
    data.append(load)
     
#Saving the output file
with open("emailconversation_Output.csv", "w", newline='') as f:
    f_writer = csv.DictWriter(f, fields)
    f_writer.writeheader()
    f_writer.writerows(data)
