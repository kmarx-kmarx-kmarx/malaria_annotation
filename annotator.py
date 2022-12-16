# tool for quickly annotating an image as positive/negative
# appends _p at end of filename for positive, _n for negative
# press 'q' to quit and save, a' to go back, 's' for negative, 'd' for positive, 'f' for unsure


import os
import pygame
import glob
import pandas as pd
import random
import os

path_to_images = "./output"
image_type = "png"
path_to_spot_list_csv = "./spot_list_ilastik_U3D.csv"
path_to_out_csv = "./annotated_spot_list_ilastik_U3D.csv"

fix_number = True # set True if the view numbers are offset by 100

random_order = False
random.seed(1)
sz = 512
save_interval = 10 # write the CSV every 10 annotations

pygame.init()
scrn = pygame.display.set_mode((sz*3,sz))

# Load spot list CSVg
spotlist = pd.read_csv(path_to_spot_list_csv)
n_imgs = spotlist.shape[0]
print(n_imgs)

indices = list(range(n_imgs))
if random_order:
    random.shuffle(indices)

index = 0
column_names = ["annotation"] + list(spotlist.columns)
classifications = pd.DataFrame(columns = column_names)
# write headers, create CSV
classifications.to_csv(path_to_out_csv, mode='w', index=False)

# loop over images
i = 0
j = 0
while i < n_imgs:
    index = indices[i]
    # get the image path
    if fix_number:
        img_name = str(int(spotlist["FOV_row"][index])-100)  + "_" + str(int(spotlist["FOV_col"][index])-100) + "_" + str(spotlist["x"][index]) + "_" + str(spotlist["y"][index])
    else:
        img_name = str(spotlist["FOV_row"][index])  + "_" + str(spotlist["FOV_col"][index]) + "_" + str(spotlist["x"][index]) + "_" + str(spotlist["y"][index])

    target_path = os.path.join(path_to_images, img_name + "." + image_type)
    print(target_path)
    # set window name
    pygame.display.set_caption(img_name)
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
    status = -1
    if key_pressed == 'a':
        # case a - go back to the previous image
        # and delete the previous row
        i -= 1
        try:
            classifications.drop(classifications.index[[len(classifications)-1]], inplace=True)
        except:
            # If we can't drop, it's because there's nothing left to drop. We can't go back!
            print("Already at end!")
            i += 1
            pass
        i = max(0, i)
    # if key_pressed == 'g':
    #     # case g - go to next image
    #     i += 1
    #     i = min(n_imgs, i)
    if key_pressed == 's':
        # case s: mark as positive and go to next
        status = 1
        i += 1
    if key_pressed == 'd':
        # case d: mark as negative and go to next
        status = 0
        i += 1
    if key_pressed == 'f':
        # case f: mark as unsure and go to next
        status = 9
        i += 1

    # append row to dataframe
    if status != -1:
        classifications.loc[len(classifications)] = [str(status)] + list(spotlist.iloc[index])
    print(classifications)
    # save the CSV
    if (len(classifications) % save_interval) == 0 or key_pressed == 'q':
        classifications.to_csv(path_to_out_csv, mode='a', index=False, header=False)
        # reset classifications
        classifications = pd.DataFrame(columns = column_names)

    if key_pressed == 'q':
        break

pygame.quit()