# tool for quickly annotating an image as positive/negative
# appends _p at end of filename for positive, _n for negative
# press 'q' to quit and save, 'a' to go back, 'g' to go forward, 
# 's' for positive, 'd' for negative, 'f' for unsure
# 'h' to skip to next unsure
# 'j' to skip to next unlabeled


import os
import pygame
import glob
import pandas as pd
import random
import os

path_to_images = "./output"
image_type = "png"
path_to_spot_list_csv = "./spot_list_ilastik_U3D.csv"
path_to_out_csv = "./new_annotated_spot_list_ilastik_U3D.csv"

overwrite_pre = False # set True to overwrite the previous path_to_out
fix_number = True # set True if the view numbers are offset by 100

random_order = False
random.seed(1)
sz = 512
save_interval = 10 # write the CSV every 10 annotations

POS_CODE     = 1
NEG_CODE     = 0
UNKNOWN_CODE = 9
INIT_CODE    = -1

pygame.init()
scrn = pygame.display.set_mode((sz*3,sz))

# Load spot list CSV
# if it already exists and we don't want to overwrite, load it
if os.path.exists(path_to_out_csv) and not overwrite_pre:
    spotlist = pd.read_csv(path_to_out_csv)
# otherwise, remake it.
else:
    spotlist = pd.read_csv(path_to_spot_list_csv)
    n_imgs = spotlist.shape[0]
    # add annotations column, assign default value
    spotlist["annotations"] = str(INIT_CODE)
    # fix numbering
    if fix_number:
        spotlist["FOV_row"] = spotlist["FOV_row"]  - 100
        spotlist["FOV_col"] = spotlist["FOV_col"]  - 100
    spotlist.to_csv(path_to_out_csv, mode='w', index=False)

n_imgs = spotlist.shape[0]
# randomize order
indices = list(range(n_imgs))
if random_order:
    random.shuffle(indices)

# loop over images
i = 0
while i < n_imgs:
    index = indices[i]
    # get the image path
    img_name = str(int(spotlist["FOV_row"][index]))  + "_" + str(int(spotlist["FOV_col"][index])) + "_" + str(int(spotlist["x"][index])) + "_" + str(int(spotlist["y"][index]))
    target_path = os.path.join(path_to_images, img_name + "." + image_type)
    print(target_path)
    # set window name
    caption = img_name + ": "
    tag = str(spotlist["annotations"][index])
    if tag == str(POS_CODE):
        caption += "Positive"
    elif tag == str(NEG_CODE):
        caption += "Negative"
    elif tag == str(UNKNOWN_CODE):
        caption += "Unsure"
    elif tag == str(INIT_CODE):
        caption += "Not Annotated"
    pygame.display.set_caption(caption)
    # open the image and resize it
    imp = pygame.image.load(target_path).convert()
    imp = pygame.transform.scale(imp, (sz*3,sz))
    # display the image
    scrn.blit(imp,(0,0))
    pygame.display.flip()

    # check for key presses
    key_pressed = 'q'
    while True:
        break_flag = False
        for event in pygame.event.get():
            # handle quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                break_flag = True
            # process keypress
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                break_flag = True

        if break_flag:
            break
    # handle key press
    print(key_pressed)
    status = INIT_CODE
    if key_pressed == 'a':
        # case a - go back to the previous image without modifying current annotation
        i -= 1
        status = spotlist["annotations"][index]
        i = max(0, i)
    elif key_pressed == 'g':
        # case g - go to next image without modifying current annotation
        i += 1
        status = spotlist["annotations"][index]
        i = min(n_imgs, i)
    elif key_pressed == 's':
        # case s: mark as positive and go to next
        status = POS_CODE
        i += 1
    elif key_pressed == 'd':
        # case d: mark as negative and go to next
        status = NEG_CODE
        i += 1
    elif key_pressed == 'f':
        # case f: mark as unsure and go to next
        status = UNKNOWN_CODE
        i += 1
    elif key_pressed == 'h':
        # case h: skip to next unsure
        i += 1
        index = indices[i]
        status = spotlist["annotations"][index]
        while str(status) != str(UNKNOWN_CODE):
            i += 1
            index = indices[i]
            status = spotlist["annotations"][index]
    elif key_pressed == 'j':
        # case j: skip to next unlabeled
        i += 1
        index = indices[i]
        status = spotlist["annotations"][index]
        while str(status) != str(INIT_CODE):
            i += 1
            index = indices[i]
            status = spotlist["annotations"][index]
    # for any other key press, do nothing 
    else:
        status = spotlist["annotations"][index]

    # add data to dataframe
    if key_pressed != 'q':
        spotlist.loc[index, 'annotations'] = str(status)
        tag = str(status)
        label = "Index: " + str(index) + ", "
        if tag == str(POS_CODE):
            label += "Positive"
        elif tag == str(NEG_CODE):
            label += "Negative"
        elif tag == str(UNKNOWN_CODE):
            label += "Unsure"
        elif tag == str(INIT_CODE):
            label += "Not Annotated"
        print(label)
    # save the CSV
    if ((i+1)% save_interval) == 0 or key_pressed == 'q':
        spotlist.to_csv(path_to_out_csv, mode='w', index=False)

    if key_pressed == 'q':
        break

    print("~~~~~~~~~~")

pygame.quit()