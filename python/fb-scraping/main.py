from facebook_scraper import get_posts
import requests
import os



PAGE_NAME='knowhistorylive'
OUTPUT_DIR=f"./{PAGE_NAME}/"

if not os.path.exists(f"./{PAGE_NAME}"):
    os.mkdir(PAGE_NAME)


for post_index,post in enumerate(get_posts(PAGE_NAME, pages=120,options={"posts_per_page": 4})):
    post_text=post['text']
    post_id=post['post_id']
   
    post_filename=f"{post_id}.txt"

    if os.path.exists(OUTPUT_DIR + post_filename):
        print(f"SKIPPING : {post_id}")
    else:
        if post_text:
            with open(OUTPUT_DIR + post_filename,'w',encoding='utf-8') as fp:
                fp.write(post_text)

        images=post['images']
        for image_index,image in enumerate(images):

            ext='png' if '.png' in image else 'jpg'
            image_title=f"{post_id}-{image_index}.{ext}"

            response=requests.get(image)
            if response.status_code == 200:
                with open(OUTPUT_DIR + image_title, 'wb') as f:
                    f.write(response.content)
