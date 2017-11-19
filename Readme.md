# <center>UnCannyEdges</center>
## <center>Logo Detection and Identification</center>

**UnCannyEdges** is a tools that allows to detect and identify the logos of several TV stations on video frames.

This functionality can be used to fight against product piracy or to remove videos containing illegal symbols from on-line platforms, like YouTube.
In addition, it is possible to detect if there is no logo of a TV station which is the case during commercial brakes.
Therefore, **UnCannyEdges** could also be used to remove commercial brakes from recordings.

Training of Logos
-----------------

The *Rohde & Schwarz GmbH & Co. KG.* provided us ~50.000 video frames which were labeled with the name of the sending TV station.

We used this data and custom-generated frames containing the logos utilizing the (*scripts/generate/insert_logos.py*) to train a neural network. The neural network was based on the *inceptionv3* precomputed **Tensorflow** network provided by Google and was retrained for this task.

We used the following command to train our model:

    python -m scripts.retrain \
    --bottleneck_dir=tf_files/bottlenecks \
    --how_many_training_steps=700 \
    --model_dir=tf_files/models/ \
    --summaries_dir=tf_files/training_summaries/incept_double/0.01 \
    --output_graph=tf_files/retrained_graph.pb \
    --output_labels=tf_files/retrained_labels.txt \
    --image_dir=<data> \
    --learning_rate=0.01 \
    --validation_batch_size=1000 \
    --train_batch_size=1000


To use the neural network for detection and identification of logos, please stick to the description in the scripts subdirectory.


Detection and Identification
----------------------------

To detect and identify the logos we provide GUI and console based solutions.
The Python scripts for this tasks are contained in the scripts directory of this repository.

The neural network returns the accuracy and a identification decision for new video frames with a test set accuracy of ~90%.


Dependencies
------------

Python: We used Python2 during development.
* Pillow
* scipy
* tkinter
* tensorflow
* numpy
