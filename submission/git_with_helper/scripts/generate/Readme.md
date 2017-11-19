In this document we describe the functionality provided by some scripts we used during development.

Generate additional Training Data
---------------------------------

This script can be used to generate additional training data using a transparent image of a logo and a bunch of video frames without any logo.

    Usage: python2 insert_logs.py --frames <frames_dir> --outdir <frames_output> --logometa <additional_cfg_data> --samples <number_of_samples>

This script will load video frames from the <frames_dir> and will print the logos (named: <label_in_logos>.png) on these frames. The output of the newly generated <number_of_samples> frames are printed to the <frames_output>. We assume that the *.png* files are in the same directory where we start the script from.

the *logos.json* file is an example of the logos metadata we need to have access to. We procide the *logos.json* file as an result for the images.
In addition to the new samples we provide *metadata.txt* files as metadata for the new samples.

Apply Canny Edge Detection Algorithm on Data
--------------------------------------------
The *cannyOnImages.py* script allows to calculate the Canny edge prediction metric on video frames:

    python2 cannyOnImages.pu <frames_dir> <output_dir>

The blank frames are contained in the frames directory.


Perfect Logo Extraction from Metadata
-------------------------------------

The script *extract_logo.py* provides functionality to extract the logo contained on video frames exactly based on the metadata. This is quite helpful during model training:

    python2 extract_logo.py <frames_dir> <output_dir>

During processing we cut-out the logo from the frames contained n the <frames_dir> directory.
We assume that a *metadata.txt* file is contained in every subdirectory (the script works recursively) that contains frames to convert.

After this procedure we copy the extracted iformation to the <output_dir>.

Example of the metadata.txt:

    <label>,<x>,<y>,<width>,<height>


imageSource.py
--------------

Just a library used by many of our scripts and the GUI.
