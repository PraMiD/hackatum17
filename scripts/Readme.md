Usage of the Neural Network
---------------------------

The file *label_image.py* can be used to label images.
This file can be imported in our own Python project to identify logos on video frames. However, you have to adapt the paths to the files of the neuronal network in the  *label_image.py*

    from label_image import classify

    frames = <list_of_jpg_frame_paths>
    results = classify(frames)

*Result* is a dictionary containing the results of the identification and classification.
In the following our can see the format of this dictionary:

    {
        "prediction" : (predicted_label>, <accuracy>)/<no_label>,
        <prefix_label> : {
            "percentage" : <percentage>,
            "elements" : [
                ("<exact_label>" : <percentage>),
                ("<excat_label2>" ...)
            ]
        },
        <prefix_label2> : {...}
    }

As one could provide labels for several sub-stations of one TV station, we provide the prediction primarily for the superior station and the subordinary ones.

Example:
    prosieben : {
        "percentage" : 0.90,
        "elements" : [
            (prosiebenmaxx : 0.60),
            (prosiebenmaxx-newstime : 0.30)
        ]
    }

In addition, you can provide a path to a directory containing *.jpg* files to classify on the command line:

    python2 label_image.py <path_to_files>

As a result of this command you get the same dictionary as described above printed on stdout.

If you are using this approach it is in your responibility which frames shall be classified. We trained the neural network to work on frames prepocessed using the Cenny edge prediction algorithm.
However, you can also provide normal/colored frames in the input directory.

(As the GUI based solution is currently not ready, the command line interface also includes the Cenny algorithm.)


GUI-based Solution
------------------

We started to program a GUI-based solution and the basic Python scripts are also contained in the repository.

Due to lack of time, it was not possible to provide a 100% operatable frontend.
Nevertheless, it is possible to detect and identify logos using the command line interface.

Additional Scripts
------------------

A description of the additionally provided scripts is contained in their subdirectory.