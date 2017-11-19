Usage of the Neural Network via CLI
--------------------------------

The fastest way to use our tool is to use the trained neural network via CLI.

Please see *git_with_helper* for more documentation on our scripts we used for preparing the frames and how to use them.


The file *label_image.py* in the *network* directory can be used to label images. It prints the TensorFlow output as well as a prediction with a certainty by the likes of:

    ('br', 0.92061515152454376)

As one could provide labels for several sub-stations of one TV station, we provide the prediction primarily for the superior station and the subordinary ones in a larger dictionary in the end.

Example:
    prosieben : {
        "percentage" : 0.90,
        "elements" : [
            (prosiebenmaxx : 0.60),
            (prosiebenmaxx-newstime : 0.30)
        ]
    }

To use the script, please specify the directory with your .jpgs like:

    python2 label_image.py <path_to_files>

As a result of this command you get the same dictionary as described above printed on stdout.

If you are using this approach it is in your responsibility which frames shall be classified. We trained the neural network to work on frames prepocessed using the Canny edge prediction algorithm.
However, you can also provide normal/colored frames in the input directory.

**As the GUI based solution is currently not ready, the command line interface also includes the Canny algorithm, to preprocess the file with 'canny edge detection', change the command line call to:**

    python2 label_image.py <path_to_files> canny

