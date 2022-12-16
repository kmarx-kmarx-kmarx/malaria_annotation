# malaria_annotation
Tool used to annotate malaria image data.

Usage:

Set `path_to_images` to the path to the folder containing the cropped images. Set `image_type` to the file type. Set `path_to_spot_list_csv` to the path to the spot list csv. Set `path_to_out_csv` to the path to the output csv. If the view numbers are offset by 100, set `fix_number` to True. If you want to see the images in a random order, set `random_order` to True. 

`annotator.py` will open a pygame window with the first image view. Press `q` or press the x in the window to quit and save the current annotations. Press `a` to delete the previous annotation and go back. Note that `annotator.py` writes the annotations to disc every 10 annotations; pressing the `a` button cannot bring you back to overwrite an annotation saved to disc, only the ones in the buffer. Press `d` to mark the view as positive, `s` for negative, and `f` for unsure.

The output csv is identical to the path spot list csv but with an extra column indicating what the annotation was. A `0` indicates unsure, `1` indicates positive, and `2` indicates negative.

The output csv is overwritten each time the code runs, change the name of the output csv to prevent this.
