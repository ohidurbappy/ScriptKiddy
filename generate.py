import os
import urllib.parse

def get_category_slug(category):
    return category.lower().replace(' ','-')
 

GITHUB_REPO_URL="https://www.github.com/ohidurbappy/ScriptKiddy"


fp=open('README.md','w',encoding='utf-8')
fp.write("# ScriptKiddy\n\n")

categories=[x for x in os.listdir('.') if os.path.isdir(x) and x.startswith('.')==False]

# write list of categories
categories=sorted(categories)
fp.write("### List of Categories\n\n")
for category in categories:
    category_slug=get_category_slug(category)
    fp.write(f"- [{category.upper()}](#{category_slug})\n")


for category in categories:
    category_slug=get_category_slug(category)
    fp.write(f"#### {category.upper()}\n\n")
    list_of_files=os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),category))
    list_of_files.sort()
    for filename in list_of_files:
        title=(filename.replace('-',' ').replace('_',' ')).title()
        if '.' in title:
            title=title.split('.')[0]
        print(title)
        filename=urllib.parse.quote(filename)
        
        if os.path.isdir(os.path.join(category,filename)):
            link_to_file=f"{GITHUB_REPO_URL}/tree/main/{category}/{filename}"
        else:
            link_to_file=f"{GITHUB_REPO_URL}/blob/main/{category}/{filename}"
    
        fp.write(f"- [{title}]({link_to_file})\n")
    fp.write("\n\n")

fp.close()