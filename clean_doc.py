import re

new = ""
with open("graffiti2.txt", "r+", encoding='utf8') as f:
   old = f.read()  # read everything in the file
   #delete all none uppercase words
   old = re.sub(r'\b\w*[a-z]+\w*\b','',old)
   old = re.sub(r'[“.!?,~()"â€¢;<:”\\-]','',old)
   old = re.sub(r"\b'\b",'',old)
   old = re.sub(r"\b/\b",' ',old)
   old_arr = old.split(" ")
   for word in old_arr:
      if word == "":
         print("espacio", word)
      elif word.isspace():
         print("isspace",word)
      elif word.isdigit():
         print("isdigit",word)
      elif "[" in word:
         print("[")
      else:
         word= " ".join(word.split())
         if len(word) > 1:
            #print(word)
            new+=word.lower() + " "
# open text file

out = []
seen = set()
for word in new.split(" "):
   if word not in seen and len(word) > 1:
      if word == "":
         print("espacio", word)
      elif word.isspace():
         print("isspace", word)
      elif word.isdigit():
         print("isdigit", word)
      elif "[" in word:
         print("[")
      else:
         word = " ".join(word.split())
         if len(word) > 1:
            out.append(word)
            seen.add(word)
    # now out has "unique" tokens

unique_list_str = ""
for word in out:
   #print(word)
   unique_list_str += word+ "\n"

text_file = open("2new-clean-graffiti.txt", "w", encoding='utf8')

# write string to file
text_file.write(unique_list_str)

# close file
text_file.close()